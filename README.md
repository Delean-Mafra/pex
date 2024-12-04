CDADOS - Projeto de Extensão I - Delean Mafra 

 

 

Descrição do Projeto  

 

Este projeto tem como objetivo automatizar a conferência de recibos de pagamentos de eventos beneficentes da Igreja Renascer em Cristo. Com a implementação deste sistema, busca-se:  

 

Descrição da 1° parte do Projeto: 

 

Criei um plano de ação com os seguintes objetivos: 

 

Reduzir o Trabalho Manual: A conferência de recibos e a exclusão de arquivos duplicados são tarefas que consomem tempo e esforço. O sistema desenvolvido em Python automatiza esse processo, permitindo que a equipe da igreja se concentre em outras atividades mais relevantes.  

Aumentar a Precisão: A automação minimiza a probabilidade de erros humanos, garantindo que todos os recibos sejam verificados de maneira eficiente e que nenhum documento importante seja perdido ou tratado incorretamente.  

Gerar Relatórios: O sistema também inclui a funcionalidade de gerar logs detalhados de arquivos excluídos. Isso garante transparência no processo e permite que a equipe rastreie as ações tomadas pelo sistema.  

Facilitar o Acesso às Informações: O uso de um arquivo de configuração para o caminho da pasta aumenta a facilidade de acesso e utilização do sistema, promovendo um ambiente de trabalho mais produtivo.  

Com esses objetivos, o projeto visa não apenas a eficiência operacional, mas também um suporte adequado às atividades da Igreja Renascer em Cristo.  

  

Descrição da 2° parte do Projeto:  

A atualização no código permite ler automaticamente o caminho da pasta a partir de um arquivo de configuração (pex.lic), trazendo uma melhoria significativa em termos de usabilidade e eficiência. O sistema não exige que o usuário insira manualmente o caminho da pasta a cada execução, minimizando o tempo necessário para configurar e rodar o script. Esse aprimoramento torna o processo mais ágil, reduz a chance de erros de digitação ao informar o caminho e permite que a equipe execute a verificação de duplicados com um clique. Além disso, essa modificação facilita a integração do sistema com outros processos automatizados e garante uma experiência mais prática e acessível para a equipe da igreja. 

  

Observação: 

  

Inicialmente, optei por utilizar a biblioteca “kivy” para criar uma interface mais agradável, combinada com a biblioteca "cryptography” para criar um registro de licença criptografado, evitando que o programa fosse compartilhado com outras pessoas além do pastor Julian e do Bispo Gabriel. Infelizmente, tive diversos problemas com as duas bibliotecas, pois o código funcionava perfeitamente no meu ambiente de teste, porém, quando era compilado para um executável, ele não conseguia ler corretamente o registro de licença criado. Outro problema foi que a compilação do programa utilizando a biblioteca “kivy” era muito longa, levando aproximadamente 30 para concluir cada compilação. Foram compiladas 47 versões (1.0.0.47) desse projeto inicial, totalizando aproximadamente 23 horas de programação e compilação do programa. 

  

3ª Parte do Projeto: Lançando a versão 2.0.0.0 

Removi do código a biblioteca “kivy” e "cryptography” e adicionei a biblioteca “Tkinter” no lugar da “kivy”. 

A implementação da biblioteca “Tkinter” no projeto permitiu criar uma interface gráfica amigável e visualmente agradável, oferecendo várias vantagens:  

Acessibilidade e Usabilidade:  

Interface Intuitiva: Tkinter possibilita a criação de interfaces gráficas simples e intuitivas, facilitando a interação do usuário com o programa, sem necessidade de comandos no terminal.  

Feedback Imediato: Com "Tkinter”, os usuários recebem feedback imediato através de mensagens de diálogo, como a confirmação de exclusão de arquivos duplicados, o que melhora a experiência geral.  

Credibilidade e Profissionalismo:  

Aspecto Visual Agradável: A interface gráfica proporciona um aspecto mais profissional ao projeto, aumentando a credibilidade do software perante os usuários.  

Customização: Elementos visuais, como labels e botões, foram personalizados para incluir informações de autoria, como "©2024 Delean Mafra - Todos os direitos reservados", conferindo autenticidade ao trabalho.  

Boas Práticas de Desenvolvimento:  

Separação de Funções: A criação de uma GUI (Graphical User Interface) permite uma separação clara entre a lógica do programa e a interface do usuário, tornando o código mais modular e fácil de manter.  

Manutenibilidade: Interfaces gráficas facilitam futuras atualizações e a introdução de novas funcionalidades sem a necessidade de alterar a lógica principal do código.  

  

4ª Parte do Projeto: Criação do Arquivo de Controle de Versão (version.txt)  

A implementação de um sistema de controle de versão utilizando o arquivo “version.txt” permite acompanhar e documentar as diferentes versões do software, garantindo um histórico claro das alterações e evoluções do projeto.  

Organização e Controle:  

Histórico de Versões: O arquivo de controle de versão documenta o histórico de todas as compilações do software, facilitando o rastreamento de mudanças e a identificação de versões específicas.  

Gestão de Liberações: Definir versões claras do software (como 2.0.0.0) ajuda na gestão e na liberação organizada de updates, proporcionando uma visão estruturada das melhorias implementadas.  

Facilidade de Manutenção:  

Rastreabilidade: O controle de versão permite identificar rapidamente as mudanças feitas em cada versão, facilitando a resolução de bugs e a implementação de novas funcionalidades.  

Documentação: A inclusão de detalhes como o nome do autor, a descrição do arquivo e o copyright no “version.txt” contribui para uma documentação robusta e completa do projeto.  

Preparação para Distribuição:  

Conversão para Executável: A criação do arquivo de controle de versão é essencial para a conversão do código em um executável (.exe), permitindo a distribuição mais fácil e profissional do software, sem a necessidade de um ambiente de desenvolvimento específico.  

Credibilidade: A inclusão do nome "Delean Mafra" e do copyright reforça a autenticidade e profissionalidade do projeto.  

  

5ª Parte do Projeto: Criação do Compilador em Python (compilador.py)  

Na quinta parte do projeto, foi desenvolvido um compilador em Python com o objetivo de transformar o código em um executável (.exe), utilizando as bibliotecas “pyinstaller” e “subprocess”. Esta etapa é fundamental para a distribuição do software, permitindo que ele seja executado no ambiente dos usuários sem a necessidade de um interpretador Python instalado.  

Profissionalismo:  

Apresentação: Oferecer o software como um executável melhora a apresentação e a experiência do usuário, conferindo ao projeto um aspecto mais profissional e refinado.  

Automatização do Processo de Build:  

Automação: A utilização de um script de compilação automatiza o processo de build, tornando-o repetível e reduzindo a margem de erro, o que é particularmente útil para futuras atualizações e versões do software.  

  

Linha do tempo para conclusão do projeto  

  

1° parte do projeto identifiquei a necessidade da instituição e criei uma solução em python:  

  

import os  

import hashlib  

   

def calcular_hash(arquivo):  

    """Calcula o hash SHA-256 de um arquivo para identificar duplicados."""  

    hash_sha256 = hashlib.sha256()  

    with open(arquivo, 'rb') as f:  

        for chunk in iter(lambda: f.read(4096), b""):  

            hash_sha256.update(chunk)  

    return hash_sha256.hexdigest()  

   

def verificar_duplicados(caminho_pasta):  

    """Verifica e exclui arquivos duplicados na pasta especificada."""  

    arquivos_verificados = {}  

    log_exclusao = []  

   

    for root, _, arquivos in os.walk(caminho_pasta):  

        for nome_arquivo in arquivos:  

            if nome_arquivo.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):  

                caminho_completo = os.path.join(root, nome_arquivo)  

                hash_arquivo = calcular_hash(caminho_completo)  

   

                if hash_arquivo in arquivos_verificados:  

                    # Excluir o arquivo duplicado  

                    os.remove(caminho_completo)  

                    log_exclusao.append(caminho_completo)  

                else:  

                    # Armazenar o hash para comparação futura  

                    arquivos_verificados[hash_arquivo] = caminho_completo  

   

    # Salvar log dos arquivos excluídos  

    with open('log_exclusao.txt', 'w') as log:  

        for item in log_exclusao:  

            log.write(f"{item}\n")  

    print("Processo concluído. Log salvo em 'log_exclusao.txt'.")  

   

# Solicita o caminho da pasta ao usuário e executa a verificação de duplicados  

if __name__ == "__main__":  

    caminho = input("Informe o caminho da pasta com os arquivos: ")  

    verificar_duplicados(caminho)  

  

  

2° parte do projeto: Adicionado uma função no código para que não seja necessário ter que sempre informar manualmente o caminho da pasta.  

  

def obter_caminho_da_pasta():   

"""Lê o caminho da pasta a partir de um arquivo de texto."""   

with open('pex.lic', 'r') as arquivo: caminho_pasta = arquivo.readline().strip() return caminho_pasta  

  

  

3° parte do projeto: Criado uma interface para que o programa não precisasse ser executado pelo terminal, melhorando a intuição e experiencia do usuário  

  

import os  

import hashlib  

import tkinter as tk  

from tkinter import messagebox  

  

def calcular_hash(arquivo):  

    # Calcula o hash SHA-256 de um arquivo para identificar duplicados  

    hash_sha256 = hashlib.sha256()  

    with open(arquivo, 'rb') as f:  

        for chunk in iter(lambda: f.read(4096), b""):  

            hash_sha256.update(chunk)  

    return hash_sha256.hexdigest()  

  

def verificar_duplicados(caminho_pasta):  

    # Verifica e exclui arquivos duplicados na pasta especificada  

    arquivos_verificados = {}  

    log_exclusao = []  

  

    for root, _, arquivos in os.walk(caminho_pasta):  

        for nome_arquivo in arquivos:  

            if nome_arquivo.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):  

                caminho_completo = os.path.join(root, nome_arquivo)  

                hash_arquivo = calcular_hash(caminho_completo)  

  

                if hash_arquivo in arquivos_verificados:  

                    os.remove(caminho_completo)  # Excluir o arquivo duplicado  

                    log_exclusao.append(caminho_completo)  

                else:  

                    arquivos_verificados[hash_arquivo] = caminho_completo  

  

    # Salvar log dos arquivos excluídos  

    with open('log_exclusao.txt', 'w') as log:  

        for item in log_exclusao:  

            log.write(f"{item}\n")  

    return "Processo concluído. Log salvo em 'log_exclusao.txt'."  

  

def obter_caminho_da_pasta():  

    # Lê o caminho da pasta a partir de um arquivo de texto  

    with open('pex.lic', 'r') as arquivo:  

        caminho_pasta = arquivo.readline().strip()  

    return caminho_pasta  

  

def excluir_arquivos_duplicados():  

    # Executa a função de exclusão de arquivos duplicados e exibe mensagem de conclusão  

    caminho = obter_caminho_da_pasta()  

    mensagem = verificar_duplicados(caminho)  

    messagebox.showinfo("Resultado", f"{mensagem}\nTodos os arquivos duplicados foram excluídos.")  

  

def main():  

    root = tk.Tk()  

    root.withdraw()  # Oculta a janela principal inicialmente  

  

    # Configuração da interface para executar a exclusão de arquivos duplicados  

    root.deiconify()  # Mostra a janela principal para o botão de execução  

    root.title("Exclusão de Arquivos Duplicados")  

    root.geometry("400x200")  

  

    # Label de autoria  

    label_copyright = tk.Label(root, text="©2024 Delean Mafra - Todos os direitos reservados")  

    label_copyright.pack(pady=10)  

  

    # Botão para iniciar o processo de exclusão  

    btn_executar = tk.Button(  

        root, text="Excluir Arquivos Duplicados", command=excluir_arquivos_duplicados  

    )  

    btn_executar.pack(pady=20)  

  

    root.mainloop()  

  

if __name__ == "__main__":  

    main()  

  

  

4° Parte: Criado arquivo de versão(version.txt)  

# UTF-8  

#  

# Para mais detalhes sobre o 'ffi' veja:  

# http://msdn.microsoft.com/en-us/library/ms646997.aspx  

   

VSVersionInfo(  

  ffi=FixedFileInfo(  

    filevers=(2, 0, 0, 0 ),  

    prodvers=(2, 0, 0, 0 ),  

    mask=0x3f,  

    flags=0x0,  

    OS=0x4,  

    fileType=0x1,  

    subtype=0x0,  

    date=(0, 0)  

  ),  

  kids=[  

    StringFileInfo(  

      [  

        StringTable(  

          '041604B0',  

          [  

            StringStruct('CompanyName', 'Delean Mafra'),  

            StringStruct('FileDescription', 'Exclui Arquivos Duplicados'),  

            StringStruct('FileVersion', '2.0.0.0'),  

            StringStruct('InternalName', 'Exclui Arquivos Duplicados'),  

            StringStruct('LegalCopyright', 'Copyright ©2024 | Delean Mafra, todos os direitos reservados.'),  

            StringStruct('OriginalFilename', 'Exclui Arquivos Duplicados.exe'),  

            StringStruct('ProductName', 'Exclui Arquivos Duplicados'),  

            StringStruct('ProductVersion', '2.0.0.2'),  

          ]  

        )  

      ]  

    ),  

    VarFileInfo([VarStruct('Translation', [1046, 1200])])  

  ]  

)  

  

5° parte: Criado compilador:  

  

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

  

  

 

 

 

 

 

 

 

6° Parte: Realizado a compilação o software e disponibilizada aos computadores dos usuários via AnyDesk.  

  

  

 

 

 

 

 
