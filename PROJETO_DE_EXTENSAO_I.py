# Exclusão de Arquivos Duplicados v3.0
# Copyright © 2025 Delean Mafra - Todos os direitos reservados

import os
import hashlib
import datetime
import threading
import time
import webbrowser
import logging
from flask import Flask, render_template_string, request, jsonify
from PIL import Image
import io

from pypdf import PdfReader

# Diretório raiz permitido para todas as operações de arquivos.
_config_root = os.environ.get('PEX_ALLOWED_ROOT')
if _config_root:
    _config_root = os.path.realpath(os.path.abspath(os.path.normpath(_config_root)))
else:
    _config_root = os.path.realpath(os.path.expanduser('~'))

if not os.path.isdir(_config_root):
    _config_root = os.path.realpath(os.getcwd())

BASE_ALLOWED_ROOT = _config_root


def _normalize_to_abs(path: str) -> str:
    """Normaliza e converte um caminho para absoluto resolvendo links simbólicos."""
    return os.path.realpath(os.path.abspath(os.path.normpath(path)))


def _is_path_within(base: str, target: str) -> bool:
    """Verifica se target está contido dentro de base usando commonpath."""
    try:
        return os.path.commonpath([base, target]) == base
    except ValueError:
        return False

app = Flask(__name__)

def validar_caminho_seguro(caminho):
    """Valida e sanitiza um caminho de arquivo para prevenir path injection."""
    try:
        if not isinstance(caminho, str) or not caminho.strip():
            return False, "Caminho deve ser uma string não vazia"
            
        if len(caminho) > 500:
            return False, "Caminho muito longo"
            
        caracteres_perigosos = ['\0', '\r', '\n']
        for char in caracteres_perigosos:
            if char in caminho:
                return False, "Caminho contém sequências não permitidas"
        
        if '..' in caminho or '~' in caminho:
            return False, "Caminho contém sequências de escape"
        
        if os.name == 'nt':
            if caminho.startswith('\\\\') and not (
                caminho.startswith('\\\\localhost\\') or 
                caminho.startswith('\\\\127.0.0.1\\')
            ):
                return False, "Caminhos UNC remotos não são permitidos"
        
        normalized_path = os.path.normpath(caminho)

        if '..' in normalized_path or '~' in normalized_path:
            return False, "Caminho normalizado contém sequências perigosas"

        absolute_path = _normalize_to_abs(normalized_path)

        if not _is_path_within(BASE_ALLOWED_ROOT, absolute_path):
            return False, "Caminho fora da área permitida"

        # CORREÇÃO: Usar variável local intermediária
        validated_path = absolute_path
        try:
            if not os.path.exists(validated_path):
                return False, "Caminho não existe"

            if not os.path.isdir(validated_path):
                return False, "Caminho deve ser um diretório"

        except (OSError, PermissionError):
            return False, "Acesso negado ao caminho"

        return True, validated_path
        
    except Exception:
        return False, "Erro na validação do caminho"


def validar_arquivo_seguro(caminho_arquivo, pasta_base):
    """Valida se um arquivo está dentro da pasta base permitida."""
    try:
        if not isinstance(caminho_arquivo, str) or not caminho_arquivo.strip():
            return False, "Caminho do arquivo inválido"
        
        if not isinstance(pasta_base, str) or not pasta_base.strip():
            return False, "Pasta base inválida"
        
        for caminho in [caminho_arquivo, pasta_base]:
            if any(char in caminho for char in ['..', '~', '\0', '\r', '\n']):
                return False, "Caminho contém sequências não permitidas"
        
        try:
            arquivo_normalizado = os.path.normpath(caminho_arquivo)
            base_normalizada = os.path.normpath(pasta_base)
        except (OSError, ValueError):
            return False, "Formato de caminho inválido"
        
        for caminho in [arquivo_normalizado, base_normalizada]:
            if '..' in caminho or '~' in caminho:
                return False, "Caminho normalizado contém sequências perigosas"
        
        try:
            arquivo_absoluto = _normalize_to_abs(arquivo_normalizado)
            base_absoluta = _normalize_to_abs(base_normalizada)
        except (OSError, ValueError):
            return False, "Erro ao converter caminhos absolutos"

        if not _is_path_within(BASE_ALLOWED_ROOT, base_absoluta):
            return False, "Pasta base fora da área permitida"

        if not _is_path_within(base_absoluta, arquivo_absoluto):
            return False, "Arquivo fora da pasta permitida"
            
        # CORREÇÃO: Usar variável local intermediária
        validated_file = arquivo_absoluto
        try:
            if not os.path.exists(validated_file):
                return False, "Arquivo não existe"
                
            if not os.path.isfile(validated_file):
                return False, "Não é um arquivo válido"
        except (OSError, PermissionError):
            return False, "Acesso negado ao arquivo"
        
        return True, validated_file
        
    except Exception:
        return False, "Erro na validação do arquivo"


def calcular_hash(arquivo, pasta_base):
    """Calcula o hash do conteúdo do arquivo com validação de segurança."""
    is_safe, arquivo_validado = validar_arquivo_seguro(arquivo, pasta_base)
    if not is_safe:
        return None

    hash_sha256 = hashlib.sha256()
    # CORREÇÃO: Usar apenas o caminho validado
    validated_file_path = arquivo_validado
    arquivo_lower = validated_file_path.lower()

    try:
        if arquivo_lower.endswith(('.png', '.jpeg', '.jpg')):
            with open(validated_file_path, 'rb') as f:
                img = Image.open(f)
                if img.size[0] * img.size[1] > 50000000:
                    f.seek(0)
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                else:
                    with io.BytesIO() as img_bytes:
                        img.save(img_bytes, format='PNG')
                        hash_sha256.update(img_bytes.getvalue())
                        
        elif arquivo_lower.endswith('.pdf'):
            arquivo_size = os.path.getsize(validated_file_path)
            if arquivo_size > 100 * 1024 * 1024:
                with open(validated_file_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            else:
                with open(validated_file_path, 'rb') as f:
                    pdf = PdfReader(f)
                    for page in pdf.pages:
                        text = page.extract_text()
                        hash_sha256.update(text.encode('utf-8'))
        else:
            with open(validated_file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
                    
    except Exception:
        try:
            # CORREÇÃO: Reutilizar caminho já validado
            safe_path = validated_file_path
            if os.path.exists(safe_path) and os.path.isfile(safe_path):
                with open(safe_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            else:
                return None
        except Exception:
            return None
    
    return hash_sha256.hexdigest()


def verificar_duplicados(caminho_pasta):
    """Verifica e remove arquivos duplicados com validação de segurança."""
    is_safe, resultado = validar_caminho_seguro(caminho_pasta)
    if not is_safe:
        return False, f"Caminho inválido: {resultado}", None
    
    # CORREÇÃO: Armazenar em variável local
    validated_base_path = resultado
    arquivos_verificados = {}
    log_exclusao = []
    
    arquivos_encontrados = False
    arquivos_processados = 0
    max_arquivos = 10000
    
    try:
        for root, dirs, files in os.walk(validated_base_path):
            if arquivos_processados >= max_arquivos:
                log_exclusao.append(f"Limite de {max_arquivos} arquivos atingido")
                break
            
            for nome_arquivo in files:
                if arquivos_processados >= max_arquivos:
                    break
                
                if any(nome_arquivo.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpeg', '.jpg']):
                    arquivos_encontrados = True
                    arquivos_processados += 1
                    
                    caminho_completo = os.path.join(root, nome_arquivo)
                    
                    try:
                        hash_arquivo = calcular_hash(caminho_completo, validated_base_path)
                        
                        if hash_arquivo is None:
                            log_exclusao.append(f"Erro: Arquivo inválido ignorado: {nome_arquivo}")
                            continue
                        
                        if hash_arquivo in arquivos_verificados:
                            is_safe_delete, validated_delete_path = validar_arquivo_seguro(
                                caminho_completo, validated_base_path
                            )
                            if is_safe_delete:
                                try:
                                    # CORREÇÃO: Usar caminho validado retornado
                                    os.remove(validated_delete_path)
                                    log_exclusao.append(f"Arquivo excluído: {nome_arquivo}")
                                except PermissionError:
                                    log_exclusao.append(f"Erro: Sem permissão: {nome_arquivo}")
                                except Exception:
                                    log_exclusao.append(f"Erro ao excluir: {nome_arquivo}")
                            else:
                                log_exclusao.append(f"Erro: Validação falhou: {nome_arquivo}")
                        else:
                            arquivos_verificados[hash_arquivo] = caminho_completo
                            
                    except Exception:
                        log_exclusao.append(f"Erro ao processar: {nome_arquivo}")
                    
    except Exception:
        return False, "Erro ao acessar pasta", None
    
    if not arquivos_encontrados:
        return False, "Nenhum arquivo compatível encontrado.", None

    # Salvar log
    log_path = None
    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_exclusao.txt')
        
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("=== Log de Exclusão de Arquivos ===\n")
            log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log.write(f"Pasta analisada: {caminho_pasta}\n\n")
            
            if log_exclusao:
                for item in log_exclusao:
                    log.write(f"{item}\n")
            else:
                log.write("Nenhum arquivo duplicado encontrado.\n")
                
            log.write("\n=== Fim do Log ===")
    
    except PermissionError:
        try:
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            log_path = os.path.join(documents_path, 'log_exclusao.txt')
            
            with open(log_path, 'w', encoding='utf-8') as log:
                log.write("=== Log de Exclusão de Arquivos ===\n")
                log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                log.write(f"Pasta analisada: {caminho_pasta}\n\n")
                
                if log_exclusao:
                    for item in log_exclusao:
                        log.write(f"{item}\n")
                else:
                    log.write("Nenhum arquivo duplicado encontrado.\n")
                    
                log.write("\n=== Fim do Log ===")
        
        except Exception:
            log_path = None
    
    arquivos_excluidos = len([l for l in log_exclusao if 'excluído' in l])
    
    if arquivos_excluidos > 0:
        mensagem = f"Processo concluído! {arquivos_excluidos} arquivo(s) duplicado(s) excluído(s)."
    else:
        mensagem = "Processo concluído! Nenhum arquivo duplicado encontrado."
    
    return True, mensagem, log_path




@app.route('/')
def index():
    """Página principal."""
    return render_template_string(INDEX_HTML)

@app.route('/process', methods=['POST'])
def process():
    """Processa a exclusão de arquivos duplicados, recebendo o caminho do formulário."""
    caminho_pasta = request.form.get('path', '').strip()
    
    if not caminho_pasta:
        return jsonify({'success': False, 'message': 'Por favor, informe o caminho da pasta.'})
    
    # A função verificar_duplicados agora contém toda a lógica de validação.
    success, message, log_path = verificar_duplicados(caminho_pasta)
    
    response = {'success': success, 'message': message}
    if success and log_path:
        response['log_path'] = log_path

    return jsonify(response)

@app.route('/select_folder')
def select_folder():
    """Abre um diálogo nativo para selecionar pasta."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        folder = filedialog.askdirectory(mustexist=True, title='Selecione a pasta com os arquivos')
        root.destroy()
        
        if not folder:
            return jsonify({'success': False, 'message': 'Seleção cancelada.'})
            
        # A validação é feita aqui para dar feedback imediato ao usuário.
        is_safe, resultado = validar_caminho_seguro(folder)
        if not is_safe:
            return jsonify({'success': False, 'message': f'Pasta inválida: {resultado}'})
            
        return jsonify({'success': True, 'path': resultado})
        
    except ImportError:
        return jsonify({'success': False, 'message': 'Interface gráfica (Tkinter) não disponível.'})
    except Exception as e:
        app.logger.error(f"Erro no seletor de pasta: {str(e)}")
        return jsonify({'success': False, 'message': f'Erro ao abrir seletor: {sanitizar_mensagem_erro(e)}'})

if __name__ == '__main__':
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    
    url = 'http://127.0.0.1:5000/'
    print("=" * 60)
    print("Servidor de Exclusão de Arquivos Duplicados v3.0 iniciado.")
    print(f"Acesse a interface em: {url}")
    print("Pressione Ctrl+C para parar o servidor.")
    print("=" * 60)

    # Abrir navegador após um pequeno atraso
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    app.run(host='127.0.0.1', port=5000, debug=False)

