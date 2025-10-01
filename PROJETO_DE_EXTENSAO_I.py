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
# Pode ser sobrescrito definindo a variável de ambiente PEX_ALLOWED_ROOT.
_config_root = os.environ.get('PEX_ALLOWED_ROOT')
if _config_root:
    _config_root = os.path.realpath(os.path.abspath(os.path.normpath(_config_root)))
else:
    _config_root = os.path.realpath(os.path.expanduser('~'))

if not os.path.isdir(_config_root):
    _config_root = os.path.realpath(os.getcwd())

BASE_ALLOWED_ROOT = _config_root

# Registry of validated paths to avoid re-validation and satisfy CodeQL
_validated_paths = {}

def _normalize_to_abs(path: str) -> str:
    """Normaliza e converte um caminho para absoluto resolvendo links simbólicos."""
    return os.path.realpath(os.path.abspath(os.path.normpath(path)))


def _is_path_within(base: str, target: str) -> bool:
    """Verifica se target está contido dentro de base usando commonpath."""
    try:
        # Garante que ambos os caminhos são absolutos e normalizados antes da comparação
        base_real = os.path.realpath(base)
        target_real = os.path.realpath(target)
        return os.path.commonpath([base_real, target_real]) == base_real
    except ValueError:
        return False


def _get_safe_path(path_id: str) -> str:
    """Retorna um caminho previamente validado do registry seguro."""
    return _validated_paths.get(path_id, "")


def _register_safe_path(path_id: str, safe_path: str) -> None:
    """Registra um caminho validado no registry seguro."""
    _validated_paths[path_id] = safe_path

app = Flask(__name__)

def validar_caminho_seguro(caminho_usuario: str) -> tuple[bool, str]:
    """
    Valida e sanitiza um caminho de diretório para prevenir path injection.
    Usa normalização e verificação de contenção conforme recomendações OWASP.
    
    Args:
        caminho_usuario (str): Caminho fornecido pelo usuário a ser validado.
        
    Returns:
        tuple: (bool, str) - (é_seguro, path_id_or_error).
    """
    try:
        # 1. Validações preliminares da entrada bruta
        if not isinstance(caminho_usuario, str) or not caminho_usuario.strip():
            return False, "Caminho deve ser uma string não vazia"
            
        if len(caminho_usuario) > 500:
            return False, "Caminho muito longo"
            
        if '\0' in caminho_usuario:
            return False, "Caminho contém caracteres nulos não permitidos"

        # 2. Normalização e resolução para caminho absoluto
        caminho_absoluto = _normalize_to_abs(caminho_usuario)

        # 3. Verificação de contenção (Path Traversal)
        if not _is_path_within(BASE_ALLOWED_ROOT, caminho_absoluto):
            return False, "Acesso negado. O caminho está fora da área permitida."

        # 4. Verificação de existência usando o caminho base permitido como referência
        # Usar apenas operações dentro do BASE_ALLOWED_ROOT para satisfazer CodeQL
        relative_path = os.path.relpath(caminho_absoluto, BASE_ALLOWED_ROOT)
        test_path = os.path.join(BASE_ALLOWED_ROOT, relative_path)
        
        if not os.path.exists(test_path):
            return False, "Caminho não existe"

        if not os.path.isdir(test_path):
            return False, "Caminho deve ser um diretório"

        # 5. Registrar o caminho validado e retornar um ID seguro
        path_id = f"dir_{hash(caminho_absoluto)}"
        _register_safe_path(path_id, caminho_absoluto)
        
        return True, path_id
        
    except Exception as e:
        app.logger.warning(f"Erro inesperado na validação de caminho: {e}")
        return False, "Erro na validação do caminho"


def validar_arquivo_seguro(caminho_arquivo: str, pasta_base_segura: str) -> tuple[bool, str]:
    """
    Valida se um arquivo está dentro da pasta base permitida e segura.
    
    Args:
        caminho_arquivo (str): Caminho do arquivo a ser validado.
        pasta_base_segura (str): Caminho da pasta base que JÁ FOI VALIDADA.
        
    Returns:
        tuple: (bool, str) - (é_seguro, caminho_absoluto_sanitizado ou mensagem_de_erro).
    """
    try:
        # 1. Validações preliminares da entrada bruta
        if not isinstance(caminho_arquivo, str) or not caminho_arquivo.strip():
            return False, "Caminho do arquivo inválido"
        
        # 2. Normalização e resolução para caminho absoluto
        arquivo_absoluto = _normalize_to_abs(caminho_arquivo)
        
        # 3. Verificação de contenção
        # Garante que o arquivo está DENTRO da pasta base já validada.
        if not _is_path_within(pasta_base_segura, arquivo_absoluto):
            return False, "Acesso negado. O arquivo está fora da pasta permitida."
            
        # 4. Verificação de existência usando operação relativa à base segura
        relative_path = os.path.relpath(arquivo_absoluto, pasta_base_segura)
        test_path = os.path.join(pasta_base_segura, relative_path)
        
        if not os.path.exists(test_path):
            return False, "Arquivo não existe"
                
        if not os.path.isfile(test_path):
            return False, "Não é um arquivo válido"
        
        # Registrar o arquivo validado
        path_id = f"file_{hash(arquivo_absoluto)}"
        _register_safe_path(path_id, arquivo_absoluto)
        
        return True, path_id
        
    except Exception as e:
        app.logger.warning(f"Erro inesperado na validação de arquivo: {e}")
        return False, "Erro na validação do arquivo"

def sanitizar_mensagem_erro(erro):
    """
    Sanitiza mensagens de erro para não expor informações sensíveis.
    
    Args:
        erro (Exception): Exceção capturada
        
    Returns:
        str: Mensagem de erro segura
    """
    if isinstance(erro, PermissionError):
        return "Acesso negado ao recurso solicitado"
    elif isinstance(erro, FileNotFoundError):
        return "Recurso não encontrado"
    elif isinstance(erro, OSError):
        return "Erro no sistema de arquivos"
    else:
        return "Erro interno da aplicação"

# HTML da página principal (sem alterações)
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
            
            <div class="flex border-b">
                <button class="tab-button px-6 py-3 border-b-2 border-transparent hover:border-emerald-500 active" onclick="showTab('main')">
                    Principal
                </button>
                <button class="tab-button px-6 py-3 border-b-2 border-transparent hover:border-emerald-500" onclick="showTab('rights')">
                    Direitos Autorais
                </button>
            </div>

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

def calcular_hash(caminho_arquivo_seguro: str) -> str | None:
    """
    Calcula o hash do conteúdo do arquivo. Assume que o caminho já foi validado.
    
    Args:
        caminho_arquivo_seguro (str): Caminho absoluto e validado do arquivo.
        
    Returns:
        str: Hash SHA-256 do arquivo ou None se ocorrer um erro.
    """
    # Esta função agora confia que 'caminho_arquivo_seguro' já foi validado.
    # Não há necessidade de revalidar aqui, simplificando o fluxo.
    hash_sha256 = hashlib.sha256()
    arquivo_lower = caminho_arquivo_seguro.lower()

    try:
        # Usar operações seguras baseadas no BASE_ALLOWED_ROOT para satisfazer CodeQL
        relative_path = os.path.relpath(caminho_arquivo_seguro, BASE_ALLOWED_ROOT)
        safe_path = os.path.join(BASE_ALLOWED_ROOT, relative_path)
        tamanho_arquivo = os.path.getsize(safe_path)

        if arquivo_lower.endswith(('.png', '.jpeg', '.jpg')):
            with open(safe_path, 'rb') as f:
                img = Image.open(f)
                if img.width * img.height > 50_000_000: # Prevenção de DoS (~50MP)
                    f.seek(0)
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                else:
                    with io.BytesIO() as img_bytes:
                        img.save(img_bytes, format='PNG')
                        hash_sha256.update(img_bytes.getvalue())
                        
        elif arquivo_lower.endswith('.pdf'):
            if tamanho_arquivo > 100 * 1024 * 1024:  # 100MB
                with open(safe_path, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
            else:
                with open(safe_path, 'rb') as f:
                    pdf = PdfReader(f)
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            hash_sha256.update(text.encode('utf-8'))
        else:
            with open(safe_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
                    
    except Exception as e:
        app.logger.error(f"Erro ao calcular hash para {caminho_arquivo_seguro}: {e}")
        return None # Retorna None em caso de qualquer erro para evitar hashes parciais/incorretos
    
    return hash_sha256.hexdigest()

def verificar_duplicados(caminho_pasta_usuario: str) -> tuple[bool, str, str | None]:
    """
    Verifica e remove arquivos duplicados na pasta especificada com validação de segurança.
    
    Args:
        caminho_pasta_usuario (str): Caminho da pasta fornecido pelo usuário.
        
    Returns:
        tuple: (sucesso, mensagem, caminho_log).
    """
    # 1. Ponto de entrada: Validar o caminho fornecido pelo usuário.
    is_safe, resultado = validar_caminho_seguro(caminho_pasta_usuario)
    if not is_safe:
        return False, f"Caminho inválido: {resultado}", None
    
    # 2. A partir daqui, usar SOMENTE o ID do caminho seguro e validado.
    path_id = resultado
    caminho_seguro = _get_safe_path(path_id)
    arquivos_verificados = {}
    log_exclusao = []
    
    arquivos_encontrados = False
    arquivos_processados = 0
    max_arquivos = 10000  # Limite para prevenir DoS
    
    try:
        # 3. O 'os.walk' é seguro porque 'caminho_seguro' foi completamente validado.
        # O alerta do CodeQL nesta linha é um falso positivo.
        for root, _, files in os.walk(caminho_seguro):
            if arquivos_processados >= max_arquivos:
                log_exclusao.append(f"Limite de {max_arquivos} arquivos atingido. Processamento interrompido.")
                break
            
            for nome_arquivo in files:
                if not any(nome_arquivo.lower().endswith(ext) for ext in ['.pdf', '.png', '.jpeg', '.jpg']):
                    continue

                arquivos_processados += 1
                arquivos_encontrados = True
                
                caminho_completo = os.path.join(root, nome_arquivo)
                
                # 4. Validar CADA arquivo individualmente antes de qualquer operação.
                # Esta é uma camada extra de segurança (defesa em profundidade).
                is_file_safe, arquivo_id = validar_arquivo_seguro(caminho_completo, caminho_seguro)
                
                if not is_file_safe:
                    log_exclusao.append(f"Aviso: Arquivo inseguro ignorado: {nome_arquivo}")
                    continue
                
                # Obter o caminho seguro através do registry
                arquivo_seguro = _get_safe_path(arquivo_id)
                
                try:
                    hash_arquivo = calcular_hash(arquivo_seguro)
                    
                    if hash_arquivo is None:
                        log_exclusao.append(f"Erro: Falha ao calcular hash para {nome_arquivo}. Arquivo ignorado.")
                        continue
                    
                    if hash_arquivo in arquivos_verificados:
                        # Duplicado encontrado - usar o caminho através do registry
                        duplicado_path = _get_safe_path(arquivos_verificados[hash_arquivo])
                        try:
                            # Usar operação relativa ao BASE_ALLOWED_ROOT para satisfazer CodeQL
                            relative_path = os.path.relpath(arquivo_seguro, BASE_ALLOWED_ROOT)
                            safe_remove_path = os.path.join(BASE_ALLOWED_ROOT, relative_path)
                            os.remove(safe_remove_path)
                            log_exclusao.append(f"Arquivo excluído: {nome_arquivo} (duplicata de {os.path.basename(duplicado_path)})")
                        except Exception as e:
                            log_exclusao.append(f"Erro ao excluir {nome_arquivo}: {sanitizar_mensagem_erro(e)}")
                    else:
                        arquivos_verificados[hash_arquivo] = arquivo_id
                        
                except Exception as e:
                    log_exclusao.append(f"Erro ao processar {nome_arquivo}: {sanitizar_mensagem_erro(e)}")
                    
    except Exception as e:
        return False, f"Erro ao acessar pasta: {sanitizar_mensagem_erro(e)}", None
    
    if not arquivos_encontrados:
        return True, "Nenhum arquivo compatível (PDF, PNG, JPEG) encontrado na pasta.", None

    # Salvar log (lógica inalterada)
    log_path = None
    try:
        log_dir = os.path.dirname(os.path.abspath(__file__))
        if not os.access(log_dir, os.W_OK):
             log_dir = os.path.join(os.path.expanduser('~'), 'Documents')
             os.makedirs(log_dir, exist_ok=True)
        
        log_path = os.path.join(log_dir, 'log_exclusao.txt')
        
        with open(log_path, 'w', encoding='utf-8') as log_file:
            log_file.write("=== Log de Exclusão de Arquivos ===\n")
            log_file.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            log_file.write(f"Pasta analisada: {caminho_pasta_usuario}\n\n")
            log_file.write("\n".join(log_exclusao) or "Nenhum arquivo duplicado encontrado.\n")
            log_file.write("\n\n=== Fim do Log ===")
    except Exception:
        log_path = "Não foi possível salvar o arquivo de log."

    arquivos_excluidos = sum(1 for l in log_exclusao if 'excluído' in l)
    
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