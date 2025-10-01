import os
import subprocess
from pathlib import Path

# Função para incrementar a versão
def incrementar_versao(versao):
    partes = versao.split('.')
    partes[-1] = str(int(partes[-1]) + 1)
    return '.'.join(partes)

BASE_DIR = Path(r'D:/Python/complementos/pex').resolve()

# Caminho do arquivo de versão
version_file_path = BASE_DIR / 'version.txt'

# Ler o arquivo de versão
with open(version_file_path, 'r', encoding='utf-8') as file:
    linhas = file.readlines()

# Atualizar as linhas com a nova versão, sem tocar no filevers
for i, linha in enumerate(linhas):
    if "StringStruct('ProductVersion'," in linha:
        partes = linha.split("'")
        nova_versao = incrementar_versao(partes[3])
        partes[3] = nova_versao
        linhas[i] = "'".join(partes)

# Escrever as novas linhas de volta no arquivo de versão
with open(version_file_path, 'w', encoding='utf-8') as file:
    file.writelines(linhas)

# Mudar para o drive D:
os.chdir(str(BASE_DIR))

# Limpar arquivos antigos do PyInstaller para evitar conflitos
def limpar_arquivos_antigos():
    """Remove arquivos antigos do PyInstaller que podem causar conflitos"""
    arquivos_para_remover = [
        BASE_DIR / 'build',
        BASE_DIR / 'dist',
        BASE_DIR / '__pycache__',
        BASE_DIR / 'PROJETO DE EXTENSÃO I.spec'
    ]
     
    import shutil
    for arquivo in arquivos_para_remover:
        try:
            if arquivo.exists():
                if arquivo.is_file():
                    arquivo.unlink()
                    print(f"Arquivo removido: {arquivo}")
                else:
                    shutil.rmtree(arquivo)
                    print(f"Pasta removida: {arquivo}")
        except Exception as e:
            print(f"Aviso: Não foi possível remover {arquivo}: {e}")
 
# Caminho do ícone
icon_path = str(BASE_DIR / 'ico.png')

# Caminho correto do arquivo de versão
correct_version_file_path = str(version_file_path)

# Executar o comando do PyInstaller
print("Verificando e removendo pacote pathlib obsoleto...")
try:
    # Remover o pacote pathlib obsoleto se existir
    result = subprocess.run(['python', '-m', 'pip', 'uninstall', 'pathlib', '-y'], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("Pacote pathlib obsoleto removido com sucesso.")
    else:
        print("Pacote pathlib não estava instalado ou já foi removido.")
except Exception as e:
    print(f"Aviso: Não foi possível verificar o pacote pathlib: {e}")

print("Limpando arquivos antigos do PyInstaller...")
limpar_arquivos_antigos()

print("Executando PyInstaller...")
# Arquivo principal a ser empacotado (atualizado para usar a versão com interface Flask completa)
python_file_path = str(BASE_DIR / 'PROJETO DE EXTENSÃO I.py')

# Nome do executável (PyInstaller gerará <exe_name>.exe). Pode conter espaços, mas definimos também uma versão sem espaços para facilitar checagens.
exe_name = 'PROJETO DE EXTENSÃO I'
exe_name_fs = exe_name  # Mantém nome original; se preferir sem espaços use: exe_name_fs = exe_name.replace(' ', '_')

# Comando PyInstaller com binários e dados específicos
pyinstaller_cmd = [
    'pyinstaller',
    '--onefile',
    f'--name={exe_name}',
    f'--version-file={correct_version_file_path}',
    f'--icon={icon_path}',
    f'--distpath={BASE_DIR / 'dist'}',
    f'--workpath={BASE_DIR / 'build'}',
    f'--specpath={BASE_DIR}',
    # Módulos necessários para o app Flask de exclusão (reduzido para acelerar build)
    '--hidden-import=flask',
    '--hidden-import=PIL',
    '--hidden-import=PIL.Image',
    '--hidden-import=PyPDF2',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.filedialog',
    # Coletar dados adicionais que às vezes são necessários
    '--collect-all=PyPDF2',
    # Excluir módulos grandes não usados
    '--exclude-module=matplotlib',
    '--exclude-module=PyQt5',
    '--exclude-module=PyQt6',
    '--exclude-module=PySide2',
    '--exclude-module=PySide6',
    '--console',
    python_file_path
]

print('Comando PyInstaller:', ' '.join(pyinstaller_cmd))
pyinstaller_result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

if pyinstaller_result.returncode != 0:
    print("ERRO no PyInstaller:")
    print(pyinstaller_result.stderr)
    print("Saída padrão:")
    print(pyinstaller_result.stdout)
    input("Pressione Enter para continuar...")
    exit(1)
else:
    print("PyInstaller executado com sucesso!")
    print("Saída do PyInstaller:")
    print(pyinstaller_result.stdout)

# Verificar possíveis localizações do executável
possible_paths = [
    str(BASE_DIR / 'dist' / f'{exe_name_fs}.exe'),
    str(Path('dist') / f'{exe_name_fs}.exe')
]

exe_path = None
for path in possible_paths:
    if os.path.exists(path):
        exe_path = path
        print(f"Executável encontrado em: {exe_path}")
        break

if not exe_path:
    print("Procurando executável em todos os diretórios...")
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file == f'{exe_name_fs}.exe':
                exe_path = os.path.join(root, file)
                print(f"Executável encontrado em: {exe_path}")
                break
        if exe_path:
            break

# Caminho para o certificado PFX
certificate_path = str(BASE_DIR / 'certificado-code-signing.pfx')

# Função para encontrar o signtool.exe
def find_signtool():
    """
    Procura pelo signtool.exe nos locais padrão do Windows SDK
    """
    # Primeiro, tentar versões específicas x64 (mais compatível)
    possible_paths = [
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x64\signtool.exe", 
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.18362.0\x64\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
        # Versões x86 como fallback
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x86\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x86\signtool.exe",
        r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22000.0\x86\signtool.exe",
        # Versões antigas do SDK
        r"C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\signtool.exe",
        r"C:\Program Files (x86)\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.7.2 Tools\x64\signtool.exe",
        "signtool.exe"  # Tentar no PATH
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Signtool encontrado em: {path}")
            return path
    
    # Busca automática na pasta Windows Kits, priorizando x64 e x86
    windows_kits_path = r"C:\Program Files (x86)\Windows Kits\10\bin"
    if os.path.exists(windows_kits_path):
        # Procurar por versões x64 primeiro
        for root, dirs, files in os.walk(windows_kits_path):
            if "signtool.exe" in files and ("x64" in root or "x86" in root):
                # Priorizar x64 sobre x86, evitar arm64
                if "arm64" not in root.lower():
                    signtool_path = os.path.join(root, "signtool.exe")
                    print(f"Signtool encontrado automaticamente em: {signtool_path}")
                    return signtool_path
    
    return None

# Função para assinar o executável com certificado digital
def sign_executable_with_certificate(exe_path, cert_path, cert_password=None):
    """
    Assina o executável usando signtool.exe com certificado PFX
    """
    try:
        # Encontrar o signtool.exe
        signtool_path = find_signtool()
        if not signtool_path:
            print("signtool.exe não encontrado. Tentando alternativa com osslsigncode...")
            return sign_with_osslsigncode(exe_path, cert_path, cert_password)
        
        # Comando básico do signtool com algoritmo de hash SHA256
        cmd = [
            signtool_path, 'sign',
            '/f', cert_path,
            '/fd', 'SHA256',  # Algoritmo de hash recomendado
            '/t', 'http://timestamp.digicert.com',  # Servidor de timestamp
            '/v',  # Verbose output
            exe_path
        ]
        
        # Se houver senha do certificado, adicione aqui
        if cert_password:
            cmd.insert(-1, '/p')
            cmd.insert(-1, cert_password)
        
        print(f"Executando comando: {' '.join(cmd)}")
        
        # Executar o comando de assinatura
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Executável assinado com sucesso!")
            print(result.stdout)
            return True
        else:
            print("Erro ao assinar o executável:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return False

def sign_with_osslsigncode(exe_path, cert_path, cert_password=None):
    """
    Alternativa usando osslsigncode (instalar com: pip install osslsigncode)
    """
    try:
        # Verificar se osslsigncode está disponível
        result = subprocess.run(['osslsigncode', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("osslsigncode não encontrado. Instalando...")
            install_result = subprocess.run(['pip', 'install', 'osslsigncode'], capture_output=True, text=True)
            if install_result.returncode != 0:
                print("Erro ao instalar osslsigncode:")
                print(install_result.stderr)
                return False
        
        # Comando osslsigncode
        cmd = [
            'osslsigncode', 'sign',
            '-pkcs12', cert_path,
            '-t', 'http://timestamp.digicert.com',
            '-in', exe_path,
            '-out', exe_path + '_signed'
        ]
        
        if cert_password:
            cmd.extend(['-pass', cert_password])
        
        print(f"Executando comando osslsigncode: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Substituir o arquivo original pelo assinado
            os.replace(exe_path + '_signed', exe_path)
            print("Executável assinado com sucesso usando osslsigncode!")
            return True
        else:
            print("Erro ao assinar com osslsigncode:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("Erro: Nem signtool.exe nem osslsigncode foram encontrados.")
        print("Opções:")
        print("1. Instale o Windows SDK para usar signtool")
        print("2. Execute: pip install osslsigncode")
        return False
    except Exception as e:
        print(f"Erro inesperado com osslsigncode: {e}")
        return False

# Verificar se o executável foi criado
if exe_path and os.path.exists(exe_path):
    print(f"Executável criado: {exe_path}")
    
    # Solicitar senha do certificado (se necessário)
    cert_password = ''
    
    # Assinar o executável
    success = sign_executable_with_certificate(exe_path, certificate_path, cert_password)
    
    if success:
        print("Assinatura digital aplicada com sucesso!")
        print("O executável agora possui a aba 'Assinaturas Digitais' nas propriedades.")
    else:
        print("Falha na assinatura digital.")
else:
    print("Erro: Executável não foi criado pelo PyInstaller.")
    print("Verificando conteúdo do diretório atual:")
    print(os.listdir('.'))

# Pausar a execução (equivalente ao 'pause' no .bat)
input("Pressione Enter para continuar...")