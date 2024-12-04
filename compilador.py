import os
import subprocess


# Função para incrementar a versão
def incrementar_versao(versao):
    partes = versao.split('.')
    partes[-1] = str(int(partes[-1]) + 1)
    return '.'.join(partes)

# Caminho do arquivo de versão
version_file_path = 'D:/Python/Python_projcts/pex/version.txt'

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
os.chdir('D:/')

# Mudar para o diretório do projeto
os.chdir('D:/Python/Python_projcts/pex')

# Caminho do ícone
icon_path = 'D:/Python/Python_projcts/pex/ico_lupa.ico'

# Caminho correto do arquivo de versão
correct_version_file_path = 'D:/Python/Python_projcts/pex/version.txt'

# Executar o comando do PyInstaller
subprocess.run(['pyinstaller', '--onefile', f'--version-file={correct_version_file_path}', f'--icon={icon_path}', 'pex.py'])

# Pausar a execução (equivalente ao 'pause' no .bat)
input("Pressione Enter para continuar...")
