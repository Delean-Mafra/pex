"""
Exclusão de Arquivos Duplicados v3.0
Copyright © 2025 Delean Mafra - Todos os direitos reservados
"""

import os
import hashlib
import datetime
import threading
import time
import webbrowser
import logging
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify
from PIL import Image
import io
from pypdf import PdfReader

app = Flask(__name__)

def validar_caminho_seguro(caminho, safe_root=SAFE_ROOT_PATH):
    """
    Valida e sanitiza um caminho de arquivo para prevenir path injection e garante que o caminho esteja dentro do diretório seguro.
    
    Args:
        caminho (str): Caminho a ser validado
        safe_root (Path): Diretório seguro
    Returns:
        tuple: (bool, str) - (é_seguro, caminho_normalizado)
    """
    try:
        # Validações preliminares ANTES de usar Path()
        if not isinstance(caminho, str) or not caminho.strip():
            return False, "Caminho deve ser uma string não vazia"
            
        # Verificar comprimento máximo
        if len(caminho) > 500:
            return False, "Caminho muito longo"
            
        # Bloquear caracteres perigosos ANTES de usar Path()
        caracteres_perigosos = ['..', '~', '\0', '\r', '\n']
        for char in caracteres_perigosos:
            if char in caminho:
                return False, "Caminho contém sequências não permitidas"
        
        # No Windows, bloquear caminhos UNC remotos ANTES de usar Path()
        if os.name == 'nt':
            if caminho.startswith('\\\\') and not (
                caminho.startswith('\\\\localhost\\') or 
                caminho.startswith('\\\\127.0.0.1\\')
            ):
                return False, "Caminhos UNC remotos não são permitidos"
        
        # Monta caminho absoluto relativo ao diretório seguro
        try:
            caminho_path = (safe_root / caminho).resolve()
        # Garante que o caminho está dentro do root seguro
        try:
            if not str(caminho_path).startswith(str(safe_root)):
                return False, "Caminho fora do diretório permitido"
        except Exception:
            return False, "Erro ao verificar diretório seguro"
            
        except (OSError, ValueError) as path_error:
            return False, "Formato de caminho inválido"
        
        # Verificar se o caminho existe
        try:
            if not caminho_path.exists():
                return False, "Caminho não existe"
        except (OSError, PermissionError):
            return False, "Acesso negado ao caminho"
        
        # Verificar se é um diretório
        try:
            if not caminho_path.is_dir():
                return False, "Caminho deve ser um diretório"
        except (OSError, PermissionError):
            return False, "Não foi possível verificar se é diretório"
        
        return True, str(caminho_path)
        
    except Exception as e:
        return False, "Erro na validação do caminho"

def validar_arquivo_seguro(caminho_arquivo, pasta_base):
    """
    Valida se um arquivo está dentro da pasta base permitida.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo
        pasta_base (str): Pasta base permitida
        
    Returns:
        tuple: (bool, str) - (é_seguro, motivo)
    """
    try:
        # Validar entradas ANTES de usar Path()
        if not isinstance(caminho_arquivo, str) or not caminho_arquivo.strip():
            return False, "Caminho do arquivo inválido"
        
        if not isinstance(pasta_base, str) or not pasta_base.strip():
            return False, "Pasta base inválida"
        
        # Verificar caracteres perigosos ANTES de usar Path()
        for caminho in [caminho_arquivo, pasta_base]:
            if any(char in caminho for char in ['..', '~', '\0', '\r', '\n']):
                return False, "Caminho contém sequências não permitidas"
        
        # Agora é seguro usar Path() com dados validados
        try:
            arquivo_path = Path(caminho_arquivo).resolve()
        except (OSError, ValueError):
            return False, "Formato de caminho de arquivo inválido"
            
        try:
            base_path = Path(pasta_base).resolve()
        except (OSError, ValueError):
            return False, "Formato de pasta base inválido"
        
        # Verificar se o arquivo está dentro da pasta base
        if not str(arquivo_path).startswith(str(base_path)):
            return False, "Arquivo fora da pasta permitida"
            
        # Verificar se o arquivo existe
        if not arquivo_path.exists():
            return False, "Arquivo não existe"
            
        # Verificar se é realmente um arquivo
        if not arquivo_path.is_file():
            return False, "Não é um arquivo válido"
            
        return True, "Arquivo válido"
        
    except (OSError, ValueError, RuntimeError):
        return False, "Caminho de arquivo inválido"

def sanitizar_mensagem_erro(erro):
    """
    Sanitiza mensagens de erro para não expor informações sensíveis.
    
    Args:
        erro (Exception): Exceção capturada
        
    Returns:
        str: Mensagem de erro segura
    """
    # Mapear tipos de erro para mensagens genéricas
    if isinstance(erro, PermissionError):
        return "Acesso negado ao recurso solicitado"
    elif isinstance(erro, FileNotFoundError):
        return "Recurso não encontrado"
    elif isinstance(erro, OSError):
        return "Erro no sistema de arquivos"
    elif isinstance(erro, ValueError):
        return "Valor ou parâmetro inválido"
    elif isinstance(erro, RuntimeError):
        return "Erro durante a execução"
    else:
        return "Erro interno da aplicação"

# HTML da página principal
INDEX_HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exclusão de Arquivos Duplicados v3.0</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .tab-button.active { background-color: #10b981; color: white; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg">
            <div class="bg-emerald-600 text-white p-6 rounded-t-lg">
                <h1 class="text-3xl font-bold text-center">Exclusão de Arquivos Duplicados v3.0</h1>
                <p class="text-center mt-2">Remove arquivos duplicados (PDF, PNG, JPEG) baseado no conteúdo</p>
            </div>
            
            <!-- Tabs -->
            <div class="flex border-b">
                <button class="tab-button px-6 py-3 border-b-2 border-transparent hover:border-emerald-500 active" onclick="showTab('main')">
                    Principal
                </button>
                <button class="tab-button px-6 py-3 border-b-2 border-transparent hover:border-emerald-500" onclick="showTab('rights')">
                    Direitos Autorais
                </button>
            </div>

            <!-- Main Tab -->
            <div id="main" class="tab-content active p-6">
                <form id="duplicateForm" class="space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">
                            Caminho da Pasta:
                        </label>
                        <div class="flex gap-2">
                            <input type="text" 
                                   id="pathInput" 
                                   name="path" 
                                   placeholder="C:\\caminho\\para\\sua\\pasta"
                                   required
                                   class="flex-1 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-emerald-500 focus:border-emerald-500">
                            <button type="button" 
                                    onclick="selectFolderPath()"
                                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-200">
                                📁 Selecionar Pasta
                            </button>
                            <button type="button" 
                                    onclick="clearSelection()"
                                    class="px-3 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition duration-200"
                                    title="Limpar seleção">
                                🗑️
                            </button>
                        </div>
                        <input type="file" 
                               id="folderSelector" 
                               style="display: none;">
                        <p class="mt-2 text-sm text-gray-500">
                            <strong>Como usar:</strong><br>
                            • Clique em "📁 Selecionar Pasta" para escolher uma pasta (Chrome, Edge 86+)<br>
                            • Ou digite o caminho completo da pasta (ex: C:\\MinhasPastas\\Documentos)<br>
                            • A pasta deve conter arquivos PDF, PNG ou JPEG para verificar duplicatas<br>
                            <span class="text-xs text-gray-400">💡 A seleção de pasta funciona melhor no Chrome ou Edge</span>
                        </p>
                    </div>

                    <button type="submit" 
                            class="w-full bg-emerald-600 text-white py-3 px-4 rounded-md hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 transition duration-200">
                        🗑️ Excluir Arquivos Duplicados
                    </button>
                </form>

                <div id="loading" class="hidden mt-6 text-center">
                    <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
                    <p class="mt-2 text-gray-600">Processando arquivos...</p>
                </div>

                <div id="result" class="mt-6 p-4 rounded-lg hidden">
                    <h3 class="font-bold text-lg mb-2">Resultado:</h3>
                    <div id="resultContent"></div>
                </div>
            </div>

            <!-- Rights Tab -->
            <div id="rights" class="tab-content p-6">
                <div class="h-96">
                    <iframe src="https://delean-mafra.github.io/pex/direitos_autorais" 
                            class="w-full h-full border rounded-lg"
                            frameborder="0">
                        <p>Seu navegador não suporta iframes. 
                           <a href="https://delean-mafra.github.io/pex/direitos_autorais" target="_blank">
                               Clique aqui para ver os direitos autorais
                           </a>
                        </p>
                    </iframe>
                </div>
            </div>

            <!-- Footer -->
            <div class="bg-gray-50 p-4 rounded-b-lg text-center text-sm">
                <p class="text-emerald-400">
                    <a href="https://delean-mafra.github.io/pex/">CDADOS PROJETO DE EXTENSÃO I</a> 
                    Copyright © 2025 
                    <a href="https://delean-mafra.github.io/Delean-Mafra/"> DELEAN MAFRA</a> 
                    Todos os direitos reservados 
                    <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>
                    <img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;" alt="CC">
                    <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;" alt="BY">
                    <img src="https://mirrors.creativecommons.org/presskit/icons/nc.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;" alt="NC">
                    <img src="https://mirrors.creativecommons.org/presskit/icons/sa.svg" style="max-width: 1em;max-height:1em;margin-left: .2em;" alt="SA">
                </p>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab-button').forEach(button => {
                button.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }

        async function selectFolderPath() {
            try {
                const btn = event.target;
                btn.disabled = true;
                btn.textContent = '⏳ Abrindo...';
                const response = await fetch('/select_folder');
                const data = await response.json();
                btn.disabled = false;
                btn.textContent = '📁 Selecionar Pasta';
                if (data.success) {
                    const pathInput = document.getElementById('pathInput');
                    pathInput.value = data.path;
                    pathInput.title = `Pasta selecionada: ${data.path}`;
                    pathInput.classList.add('bg-green-50','border-green-300');
                    showMessage(`Pasta selecionada: ${data.path}`,'success');
                } else if (data.message) {
                    showMessage(data.message,'error');
                }
            } catch (e) {
                showMessage('Falha ao selecionar pasta: '+ e.message,'error');
            }
        }

        function clearSelection() {
            const pathInput = document.getElementById('pathInput');
            const folderSelector = document.getElementById('folderSelector');
            
            pathInput.value = '';
            pathInput.title = '';
            pathInput.classList.remove('bg-green-50', 'border-green-300');
            folderSelector.value = '';
            
            // Remove mensagens existentes
            const existingMessages = document.querySelectorAll('.message-alert');
            existingMessages.forEach(msg => msg.remove());
            
            pathInput.focus();
        }

        function showMessage(message, type) {
            // Remove mensagens anteriores
            const existingMessages = document.querySelectorAll('.message-alert');
            existingMessages.forEach(msg => msg.remove());
            
            // Cria nova mensagem
            const messageDiv = document.createElement('div');
            let bgClass, textClass, borderClass;
            
            switch(type) {
                case 'success':
                    bgClass = 'bg-green-100';
                    textClass = 'text-green-700';
                    borderClass = 'border-green-300';
                    break;
                case 'error':
                    bgClass = 'bg-red-100';
                    textClass = 'text-red-700';
                    borderClass = 'border-red-300';
                    break;
                case 'info':
                    bgClass = 'bg-blue-100';
                    textClass = 'text-blue-700';
                    borderClass = 'border-blue-300';
                    break;
                default:
                    bgClass = 'bg-gray-100';
                    textClass = 'text-gray-700';
                    borderClass = 'border-gray-300';
            }
            
            messageDiv.className = `message-alert mt-2 p-2 rounded text-sm ${bgClass} ${textClass} border ${borderClass}`;
            messageDiv.textContent = message;
            
            // Adiciona após o container dos botões
            const pathContainer = document.getElementById('pathInput').parentNode.parentNode;
            pathContainer.appendChild(messageDiv);
            
            // Remove a mensagem após 5 segundos
            setTimeout(() => {
                if (messageDiv.parentNode) {
                    messageDiv.remove();
                }
            }, 5000);
        }

        document.getElementById('duplicateForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const resultContent = document.getElementById('resultContent');
            const pathInput = document.getElementById('pathInput');
            
            if (!pathInput.value.trim()) {
                showMessage('Por favor, selecione uma pasta ou digite o caminho da pasta.', 'error');
                pathInput.focus();
                return;
            }
            
            loading.classList.remove('hidden');
            result.classList.add('hidden');
            
            const formData = new FormData();
            formData.append('path', pathInput.value.trim());
            
            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                loading.classList.add('hidden');
                result.classList.remove('hidden');
                
                if (data.success) {
                    resultContent.innerHTML = `
                        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">
                            <p><strong>✅ Sucesso!</strong></p>
                            <p>${data.message}</p>
                            ${data.log_path ? `<p><small>Log salvo em: ${data.log_path}</small></p>` : ''}
                        </div>
                    `;
                } else {
                    resultContent.innerHTML = `
                        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                            <p><strong>❌ Erro!</strong></p>
                            <p>${data.message}</p>
                        </div>
                    `;
                }
            } catch (error) {
                loading.classList.add('hidden');
                result.classList.remove('hidden');
                resultContent.innerHTML = `
                    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                        <p><strong>❌ Erro de conexão!</strong></p>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        });
    </script>
</body>
</html>
"""

def calcular_hash(arquivo, pasta_base):
    """
    Calcula o hash do conteúdo do arquivo baseado no tipo com validação de segurança.
    
    Args:
        arquivo (str): Caminho do arquivo
        pasta_base (str): Pasta base permitida
        
    Returns:
        str: Hash SHA-256 do arquivo ou None se inválido
    """
    # Validar arquivo antes de processar
    is_safe, motivo = validar_arquivo_seguro(arquivo, pasta_base)
    if not is_safe:
        return None
    
    hash_sha256 = hashlib.sha256()
    
    try:
        # Usar Path para manipulação segura de caminhos
        arquivo_path = Path(arquivo).resolve()
        
        if arquivo.lower().endswith(('.png', '.jpeg', '.jpg')):
            # Processar imagens com validação adicional
            with open(arquivo_path, 'rb') as f:
                img = Image.open(f)
                # Verificar se a imagem não é muito grande (prevenção DoS)
                if img.size[0] * img.size[1] > 50000000:  # ~50MP
                    # Para imagens muito grandes, usar hash do arquivo
                    f.seek(0)
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                else:
                    with io.BytesIO() as img_bytes:
                        img.save(img_bytes, format='PNG')
                        hash_sha256.update(img_bytes.getvalue())
                        
        elif arquivo.lower().endswith('.pdf'):
            # Processar PDFs com validação de tamanho
            arquivo_size = arquivo_path.stat().st_size
            if arquivo_size > 100 * 1024 * 1024:  # 100MB
                # Para PDFs muito grandes, usar hash do arquivo
                with open(arquivo_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            else:
                with open(arquivo_path, 'rb') as f:
                    pdf = PdfReader(f)
                    for page in pdf.pages:
                        text = page.extract_text()
                        hash_sha256.update(text.encode('utf-8'))
        else:
            # Para outros tipos de arquivo, usar hash do arquivo completo
            with open(arquivo_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
                    
    except Exception as e:
        # Em caso de erro, tentar hash básico se arquivo ainda é válido
        try:
            arquivo_path = Path(arquivo).resolve()
            if arquivo_path.exists() and arquivo_path.is_file():
                with open(arquivo_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            else:
                return None
        except Exception:
            return None
    
    return hash_sha256.hexdigest()

def verificar_duplicados(caminho_pasta):
    """
    Verifica e remove arquivos duplicados na pasta especificada com validação de segurança.
    
    Args:
        caminho_pasta (str): Caminho da pasta a ser processada
        
    Returns:
        tuple: (sucesso, mensagem, caminho_log)
    """
    # Validar caminho de entrada
    is_safe, resultado = validar_caminho_seguro(caminho_pasta, SAFE_ROOT_PATH)
    if not is_safe:
        return False, f"Caminho inválido: {resultado}", None
    
    # Usar o caminho normalizado e seguro
    caminho_seguro = resultado
    arquivos_verificados = {}
    log_exclusao = []
    
    # Verificar se existem arquivos para processar
    arquivos_encontrados = False
    arquivos_processados = 0
    max_arquivos = 10000  # Limite para prevenir DoS
    
    try:
        # O caminho_seguro já foi validado pela função validar_caminho_seguro()
        # Portanto é seguro usar aqui
        pasta_base = Path(caminho_seguro)
        
        for arquivo_path in pasta_base.rglob('*'):
            # Verificar limite de arquivos processados
            if arquivos_processados >= max_arquivos:
                log_exclusao.append(f"Limite de {max_arquivos} arquivos atingido - processamento interrompido por segurança")
                break
                
            # Verificar se é arquivo e tem extensão válida
            if (arquivo_path.is_file() and 
                arquivo_path.suffix.lower() in ['.pdf', '.png', '.jpeg', '.jpg']):
                
                arquivos_encontrados = True
                arquivos_processados += 1
                caminho_completo = str(arquivo_path)
                
                try:
                    # Calcular hash com validação de segurança
                    hash_arquivo = calcular_hash(caminho_completo, caminho_seguro)
                    
                    if hash_arquivo is None:
                        log_exclusao.append(f"Erro: Arquivo inválido ou inseguro ignorado: {arquivo_path.name}")
                        continue
                    
                    if hash_arquivo in arquivos_verificados:
                        # Arquivo duplicado encontrado - validar antes de excluir
                        is_safe_delete, motivo = validar_arquivo_seguro(caminho_completo, caminho_seguro)
                        if is_safe_delete:
                            try:
                                arquivo_path.unlink()  # Método mais seguro que os.remove()
                                log_exclusao.append(f"Arquivo excluído: {arquivo_path.name}")
                            except PermissionError:
                                log_exclusao.append(f"Erro: Sem permissão para excluir {arquivo_path.name}")
                            except Exception as e:
                                erro_seguro = sanitizar_mensagem_erro(e)
                                log_exclusao.append(f"Erro ao excluir {arquivo_path.name}: {erro_seguro}")
                        else:
                            log_exclusao.append(f"Erro: Não foi possível validar arquivo para exclusão: {arquivo_path.name}")
                    else:
                        # Primeiro arquivo com este hash
                        arquivos_verificados[hash_arquivo] = caminho_completo
                        
                except Exception as e:
                    erro_seguro = sanitizar_mensagem_erro(e)
                    log_exclusao.append(f"Erro ao processar {arquivo_path.name}: {erro_seguro}")
                    
    except Exception as e:
        erro_seguro = sanitizar_mensagem_erro(e)
        return False, f"Erro ao acessar pasta: {erro_seguro}", None
    
    if not arquivos_encontrados:
        return False, "Nenhum arquivo compatível encontrado na pasta especificada.", None

    # Salvar log
    log_path = None
    try:
        # Tenta criar o log no mesmo diretório do script
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
        # Tenta criar o log na pasta Documents
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
    
    # Contar arquivos excluídos
    arquivos_excluidos = len([l for l in log_exclusao if 'excluído' in l])
    
    if arquivos_excluidos > 0:
        mensagem = f"Processo concluído! {arquivos_excluidos} arquivo(s) duplicado(s) foi(foram) excluído(s)."
    else:
        mensagem = "Processo concluído! Nenhum arquivo duplicado encontrado."
    
    return True, mensagem, log_path

@app.route('/')
def index():
    """Página principal."""
    return render_template_string(INDEX_HTML)

@app.route('/process', methods=['POST'])
def process():
    """Processa a exclusão de arquivos duplicados com validação de segurança."""
    try:
        caminho_pasta = request.form.get('path', '').strip()
        
        if not caminho_pasta:
            return jsonify({
                'success': False, 
                'message': 'Por favor, informe o caminho da pasta.'
            })
        
        # Validar tamanho da entrada
        if len(caminho_pasta) > 500:
            return jsonify({
                'success': False,
                'message': 'Caminho muito longo. Máximo 500 caracteres.'
            })
        
        # Processar arquivos com validação de segurança
        success, mensagem, log_path = verificar_duplicados(caminho_pasta)
        
        response = {
            'success': success,
            'message': mensagem
        }
        
        if log_path:
            # Não expor caminho completo do log por segurança
            response['log_path'] = "Log salvo com sucesso"
        
        return jsonify(response)
        
    except Exception as e:
        # Log interno para debug (não expor ao usuário)
        app.logger.error(f"Erro no processamento: {str(e)}")
        
        # Retornar mensagem genérica segura
        return jsonify({
            'success': False,
            'message': 'Erro interno da aplicação. Tente novamente.'
        })

@app.route('/select_folder')
def select_folder():
    """Abre um diálogo nativo para selecionar pasta com validação de segurança."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        # Configurar opções seguras para o diálogo
        folder = filedialog.askdirectory(
            title='Selecione a pasta com os arquivos',
            mustexist=True  # Garantir que a pasta existe
        )
        root.destroy()
        
        if not folder:
            return jsonify({'success': False, 'message': 'Seleção cancelada.'})
            
        # Validar pasta selecionada
        is_safe, resultado = validar_caminho_seguro(folder)
        if not is_safe:
            return jsonify({
                'success': False, 
                'message': f'Pasta selecionada não é segura: {resultado}'
            })
            
        return jsonify({'success': True, 'path': resultado})
        
    except ImportError:
        return jsonify({
            'success': False, 
            'message': 'Interface gráfica não disponível neste ambiente.'
        })
    except Exception as e:
        # Log interno para debug
        app.logger.error(f"Erro no seletor de pasta: {str(e)}")
        
        # Mensagem genérica segura
        erro_seguro = sanitizar_mensagem_erro(e)
        return jsonify({
            'success': False, 
            'message': f'Erro ao abrir seletor: {erro_seguro}'
        })

if __name__ == '__main__':
    # Configurações para evitar execução dupla e reduzir logs
    # Desabilita log verboso do Werkzeug
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.logger.disabled = True

    url = 'http://127.0.0.1:5000/'

    def abrir_navegador():
        # Espera o servidor subir
        time.sleep(0.8)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=abrir_navegador, daemon=True).start()

    print("=" * 60)
    print("Exclusão de Arquivos Duplicados v3.0")
    print("Copyright © 2025 Delean Mafra - Todos os direitos reservados")
    print("=" * 60)
    print(f"Abrindo navegador em: {url}")
    print("Pressione Ctrl+C para parar o servidor")
    print("=" * 60)

    # Executa sem reloader para evitar rodar duas vezes
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
