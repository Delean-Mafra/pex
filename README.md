# CDADOS - Projeto de Extensão I - Delean Mafra

## Obs

O nome do pastor e dos membros da igreja foram removidos para preservar suas identidades

## Descrição do Projeto

Este projeto tem como objetivo automatizar a conferência de recibos de pagamentos de eventos beneficentes da Igreja Renascer em Cristo. Com a implementação deste sistema, busca-se:

### 1ª Parte do Projeto (Versão 1.0.0.0)

Criei um plano de ação com os seguintes objetivos:

- **Reduzir o Trabalho Manual**: A conferência de recibos e a exclusão de arquivos duplicados são tarefas que consomem tempo e esforço. O sistema desenvolvido em Python automatiza esse processo, permitindo que a equipe se concentre em atividades mais estratégicas.
- **Aumentar a Precisão**: A automação minimiza a probabilidade de erros humanos, garantindo que todos os recibos sejam verificados de maneira eficiente e que nenhum documento importante seja perdido.
- **Gerar Relatórios**: O sistema inclui a funcionalidade de gerar logs detalhados de arquivos excluídos. Isso garante transparência no processo e permite que a equipe rastreie as ações tomadas.
- **Facilitar o Acesso às Informações**: O uso de um arquivo de configuração para o caminho da pasta aumenta a facilidade de acesso e utilização do sistema, promovendo um ambiente de trabalho mais eficiente.

Com esses objetivos, o projeto visa não apenas a eficiência operacional, mas também um suporte adequado às atividades da Igreja Renascer em Cristo.

## O QUE REALIZEI

### Início do Projeto
Iniciei o projeto preenchendo a “CARTA DE APRESENTAÇÃO”. Escolhi a organização IGREJA CRISTÃ APOSTÓLICA RENASCER EM CRISTO (nome fantasia: Igreja Apostólica Renascer em Cristo) para visitar e me apresentar. Após a autorização da organização, com o preenchimento do “TERMO DE AUTORIZAÇÃO PARA REALIZAÇÃO DAS ATIVIDADES EXTENSIONISTAS”, iniciei o projeto.

### Planejamento de Visita
Visitei a igreja e conversei com o pastor  que é o oficial responsável pela tesouraria da igreja. Identifiquei as principais áreas de interesse e as questões a serem exploradas durante a visita.

### Contatos Iniciais
Estabeleci comunicação com os representantes da Igreja Renascer em Cristo para agendar reuniões e visitas. Falei inicialmente com o pastor  que informou que no último evento beneficente ele e o bispo da igreja acabaram perdendo praticamente o sábado inteiro pois receberam vários recibos de pagamentos duplicados, então eles precisaram fazer a conferência de mais de 100 recibos abrindo 1 a 1 para ver quais eram duplicados e quais ainda precisavam ser lançados no sistema financeiro da igreja. O mesmo mencionou que seria muito útil se existisse um sistema que identificasse os recibos duplicados e já os excluíssem para evitar o retrabalho. Confirmei a disponibilidade e obtive informações preliminares sobre a instituição.

### Realização de Reuniões
Conduzi reuniões iniciais com os representantes da Igreja Renascer em Cristo para discutir o contexto, a missão e as necessidades da instituição. Documentei as informações coletadas durante as reuniões, incluindo os desafios enfrentados e as oportunidades de colaboração. A documentação completa do projeto pode ser acessada pelo link: [CDADOS - Projeto de Extensão I - Delean Mafra](https://descomplica2-my.sharepoint.com/:w:/g/personal/delean_2444070_aluno_faculdadedescomplica_com_br/ETkGd5quBbdDlRpbeOilzvcBpsXROP3t3QbiCxx5hkVtkw?e=Qrq4mq)

### Participação em Atividades Locais
Participei de atividades e eventos organizados pela instituição para me familiarizar com o ambiente e entender melhor o funcionamento diário. Observei as operações e interagi com os membros da comunidade para obter insights práticos. Muitos dos membros da comunidade fizeram ou fazem faculdade na Descomplica na área de tecnologia, como o próprio Pastor e outros 4 membros.

### Estudo de Documentos e Materiais
Nesse caso, os documentos analisados foram apenas os recibos que eles precisavam automatizar a exclusão em caso de arquivos duplicados. Esses recibos, em sua maioria, eram em formato PDF, PNG e JPEG. Identifiquei informações relevantes que possam influenciar o planejamento das atividades de extensão.

### 2ª Parte do Projeto

A atualização no código permite ler automaticamente o caminho da pasta a partir de um arquivo de configuração (`pex.lic`), trazendo uma melhoria significativa em termos de usabilidade e eficiência. O sistema não exige que o usuário insira manualmente o caminho da pasta a cada execução, minimizando o tempo necessário para configurar e rodar o script. Esse aprimoramento torna o processo mais ágil, reduz a chance de erros de digitação ao informar o caminho e permite que a equipe execute a verificação de duplicados com um clique. Além disso, essa modificação facilita a integração do sistema com outros processos automatizados e garante uma experiência mais prática e acessível para a equipe da igreja.

### Observação

Inicialmente, optei por utilizar a biblioteca `kivy` para criar uma interface mais agradável, combinada com a biblioteca `cryptography` para criar um registro de licença criptografado, evitando que o programa fosse compartilhado com outras pessoas além do pastor  e do Bispo Gabriel. Infelizmente, tive diversos problemas com as duas bibliotecas, pois o código funcionava perfeitamente no meu ambiente de teste, porém, quando era compilado para um executável, ele não conseguia ler corretamente o registro de licença criado. Outro problema foi que a compilação do programa utilizando a biblioteca `kivy` era muito longa, levando aproximadamente 30 minutos para concluir cada compilação. Foram compiladas 47 versões (1.0.0.47) desse projeto inicial, totalizando aproximadamente 23 horas de programação e compilação do programa na versão 1.0.0.0.

### 3ª Parte do Projeto: Lançando a versão 2.0.0.0

Removi do código as bibliotecas `kivy` e `cryptography` e adicionei a biblioteca `Tkinter` no lugar da `kivy`.

A implementação da biblioteca `Tkinter` no projeto permitiu criar uma interface gráfica amigável e visualmente agradável, oferecendo várias vantagens:

- **Acessibilidade e Usabilidade**:
  - **Interface Intuitiva**: `Tkinter` possibilita a criação de interfaces gráficas simples e intuitivas, facilitando a interação do usuário com o programa, sem necessidade de comandos no terminal.
  - **Feedback Imediato**: Com `Tkinter`, os usuários recebem feedback imediato através de mensagens de diálogo, como a confirmação de exclusão de arquivos duplicados, o que melhora a experiência do usuário.

- **Credibilidade e Profissionalismo**:
  - **Aspecto Visual Agradável**: A interface gráfica proporciona um aspecto mais profissional ao projeto, aumentando a credibilidade do software perante os usuários.
  - **Customização**: Elementos visuais, como labels e botões, foram personalizados para incluir informações de autoria, como "©2024 Delean Mafra - Todos os direitos reservados", conferindo autenticidade ao software.

- **Boas Práticas de Desenvolvimento**:
  - **Separação de Funções**: A criação de uma GUI (Graphical User Interface) permite uma separação clara entre a lógica do programa e a interface do usuário, tornando o código mais modular e fácil de manter.
  - **Manutenibilidade**: Interfaces gráficas facilitam futuras atualizações e a introdução de novas funcionalidades sem a necessidade de alterar a lógica principal do código.

A maior vantagem de trocar a biblioteca `kivy` pela `Tkinter` foi que a `Tkinter` não apresentou nenhum conflito de leitura de arquivos após a compilação, sendo possível lançar a versão final na segunda compilação da versão 2.0.0.0, sendo a versão final 2.0.0.2. O tempo de compilação reduziu de 30 minutos para 5 minutos e a nova versão, embora não possua uma interface tão moderna e avançada como o `kivy`, atendeu ao mesmo objetivo sem perder nenhuma funcionalidade.

### 4ª Parte do Projeto: Criação do Arquivo de Controle de Versão (`version.txt`)

A implementação de um sistema de controle de versão utilizando o arquivo `version.txt` permite acompanhar e documentar as diferentes versões do software, garantindo um histórico claro das alterações e evoluções do projeto.

- **Organização e Controle**:
  - **Histórico de Versões**: O arquivo de controle de versão documenta o histórico de todas as compilações do software, facilitando o rastreamento de mudanças e a identificação de versões específicas.
  - **Gestão de Liberações**: Definir versões claras do software (como 2.0.0.0) ajuda na gestão e na liberação organizada de updates, proporcionando uma visão estruturada das melhorias implementadas.

- **Facilidade de Manutenção**:
  - **Rastreabilidade**: O controle de versão permite identificar rapidamente as mudanças feitas em cada versão, facilitando a resolução de bugs e a implementação de novas funcionalidades.
  - **Documentação**: A inclusão de detalhes como o nome do autor, a descrição do arquivo e o copyright no `version.txt` contribui para uma documentação robusta e completa do projeto.

- **Preparação para Distribuição**:
  - **Conversão para Executável**: A criação do arquivo de controle de versão é essencial para a conversão do código em um executável (.exe), permitindo a distribuição mais fácil e profissional do software, sem a necessidade de um ambiente de desenvolvimento específico.
  - **Credibilidade**: A inclusão do nome "Delean Mafra" e do copyright reforça a autenticidade e profissionalidade do projeto.

```python
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

```


### 5ª Parte do Projeto: Criação do Compilador em Python (`compilador.py`)

Na quinta parte do projeto, foi desenvolvido um compilador em Python com o objetivo de transformar o código em um executável (.exe), utilizando as bibliotecas `pyinstaller` e `subprocess`. Esta etapa é fundamental para a distribuição do software, permitindo que ele seja executado no ambiente dos usuários sem a necessidade de um interpretador Python instalado.

- **Profissionalismo**:
  - **Apresentação**: Oferecer o software como um executável melhora a apresentação e a experiência do usuário, conferindo ao projeto um aspecto mais profissional e refinado.

- **Automatização do Processo de Build**:
  - **Automação**: A utilização de um script de compilação automatiza o processo de build, tornando-o repetível e reduzindo a margem de erro, o que é particularmente útil para futuras atualizações e versões do software.
 
```python
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

```

### Código Implementado

```python
import os
import hashlib
import tkinter as tk
from tkinter import messagebox
from PIL import Image
import io
from PyPDF2 import PdfReader

def calcular_hash(arquivo):
    hash_sha256 = hashlib.sha256()
    if arquivo.lower().endswith(('.png', '.jpeg', '.jpg')):
        with open(arquivo, 'rb') as f:
            img = Image.open(f)
            with io.BytesIO() as img_bytes:
                img.save(img_bytes, format='PNG')
                hash_sha256.update(img_bytes.getvalue())
    elif arquivo.lower().endswith('.pdf'):
        with open(arquivo, 'rb') as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                with io.BytesIO() as page_bytes:
                    page_bytes.write(page.extract_text().encode('utf-8'))
                    hash_sha256.update(page_bytes.getvalue())
    return hash_sha256.hexdigest()

def verificar_duplicados(caminho_pasta):
    arquivos_verificados = {}
    log_exclusao = []
    
    # Verifica se existem arquivos para processar
    arquivos_encontrados = False
    
    for root, _, arquivos in os.walk(caminho_pasta):
        for nome_arquivo in arquivos:
            if nome_arquivo.lower().endswith(('.pdf', '.png', '.jpeg', '.jpg')):
                arquivos_encontrados = True
                caminho_completo = os.path.join(root, nome_arquivo)
                try:
                    hash_arquivo = calcular_hash(caminho_completo)
                    if hash_arquivo in arquivos_verificados:
                        try:
                            os.remove(caminho_completo)
                            log_exclusao.append(f"Arquivo excluído: {caminho_completo}")
                        except PermissionError:
                            log_exclusao.append(f"Erro: Sem permissão para excluir {caminho_completo}")
                    else:
                        arquivos_verificados[hash_arquivo] = caminho_completo
                except Exception as e:
                    log_exclusao.append(f"Erro ao processar {caminho_completo}: {str(e)}")
    
    if not arquivos_encontrados:
        return "Nenhum arquivo compatível encontrado na pasta especificada."

    # Define o caminho do arquivo de log no mesmo diretório do script
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_exclusao.txt')
    
    try:
        # Tenta criar ou abrir o arquivo de log
        with open(log_path, 'w', encoding='utf-8') as log:
            log.write("=== Log de Exclusão de Arquivos ===\n")
            log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for item in log_exclusao:
                log.write(f"{item}\n")
            log.write("\n=== Fim do Log ===")
        
        return f"Processo concluído. {len([l for l in log_exclusao if 'excluído' in l])} arquivos duplicados encontrados. Log salvo em: {log_path}"
    
    except PermissionError:
        # Tenta criar o log em uma pasta alternativa (Documents)
        try:
            documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
            log_path = os.path.join(documents_path, 'log_exclusao.txt')
            
            with open(log_path, 'w', encoding='utf-8') as log:
                log.write("=== Log de Exclusão de Arquivos ===\n")
                log.write(f"Data e hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for item in log_exclusao:
                    log.write(f"{item}\n")
                log.write("\n=== Fim do Log ===")
            
            return f"Processo concluído. Log salvo em pasta alternativa: {log_path}"
        
        except Exception as e:
            return f"Processo concluído, mas não foi possível salvar o log. Erro: {str(e)}"

def obter_caminho_da_pasta():
    caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pex.lic')
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"O arquivo {caminho_arquivo} não foi encontrado.")
    with open(caminho_arquivo, 'r') as arquivo:
        caminho_pasta = arquivo.readline().strip()
    return caminho_pasta

def excluir_arquivos_duplicados():
    try:
        caminho = obter_caminho_da_pasta()
        mensagem = verificar_duplicados(caminho)
        messagebox.showinfo("Resultado", mensagem)
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

def main():
    root = tk.Tk()
    root.title("Exclusão de Arquivos Duplicados")
    root.geometry("400x200")
    
    label_copyright = tk.Label(root, text="©2024 Delean Mafra - Todos os direitos reservados")
    label_copyright.pack(pady=10)
    
    btn_executar = tk.Button(
        root, text="Excluir Arquivos Duplicados", command=excluir_arquivos_duplicados
    )
    btn_executar.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    import datetime
    main()

```

### 6ª Parte do Projeto: Competências e Comunidades

#### COMPETÊNCIAS DESENVOLVIDAS

#### Programação e Desenvolvimento de Software
Desenvolvi habilidades em escrever códigos eficientes e criar aplicações.

#### Consultoria e Suporte Técnico
Forneci orientação e suporte técnico para uma empresa que atende a comunidade local.

### SOFT SKILLS DESENVOLVIDAS

#### Trabalho Colaborativo
Colaborei com colegas e membros da comunidade.

#### Pensamento Crítico e Resolução de Problemas
Analisei problemas complexos e desenvolvi soluções criativas e eficazes.

#### Empatia e Sensibilidade Social
Entendi e me importei com as necessidades da comunidade e dos usuários finais.

#### Adaptabilidade e Flexibilidade
Adaptei-me a novas tecnologias e mudanças nos projetos.

#### Iniciativa e Proatividade
Tomei a iniciativa e fui proativo na identificação e resolução de problemas.

#### Ética e Responsabilidade
Comprometi-me com a ética profissional e a responsabilidade social no desenvolvimento e implementação de tecnologias.

### Sobre as Comunidades que a Igreja Atende e Alcança

#### Centro de Recuperação Renascer
**Objetivo**: Oferecer dignidade, restauração e um caminho de libertação para homens em situação de dependência química.
**Atividades**: Terapia ocupacional, acompanhamento espiritual, nutricional, psicológico, psiquiátrico e clínico. O tratamento é totalmente gratuito e tem duração de seis meses.

#### Centro Assistencial Bispo Tid Hernandes
**Objetivo**: Oferecer suporte educacional, esportivo e social para crianças e adolescentes.
**Atividades**: Reforço escolar, palestras, atividades esportivas, aulas de artes marciais, orientação social, aulas de música, apoio psicológico, acompanhamento nutricional e alimentação balanceada.

#### Fé com Obras
**Objetivo**: Atender famílias carentes em comunidades vulneráveis.
**Atividades**: Distribuição de alimentos, roupas e produtos de higiene.

#### GAUF (Grupo de Apoio ao Usuário e Familiares)
**Objetivo**: Oferecer suporte a usuários de drogas e seus familiares.
**Atividades**: Reuniões semanais com troca de experiências, palestras e acompanhamento espiritual e psicológico.

#### Expresso da Solidariedade
**Objetivo**: Distribuir alimentos, roupas e produtos de higiene em comunidades carentes.
**Atividades**: Entrega mensal de toneladas de alimentos e outros itens essenciais.

#### Mais que Vencedoras (+QV)
**Objetivo**: Revolucionar o ministério feminino no Brasil.
**Atividades**: Encontros presenciais e online, desafios em diversas áreas como relacionamentos, saúde, carreira, família e ministério. Mais de 50 mil mulheres participam ativamente.

#### Internacional
**Impacto**: A Igreja Renascer em Cristo também possui projetos em outros países, como a Associação Renascer Angola, levando suporte e alimento a diversas comunidades ao redor do mundo.

### Linha do Tempo para Conclusão do Projeto

- **1ª Parte do Projeto**: Identifiquei a necessidade da instituição e criei uma solução em Python.
- **2ª Parte do Projeto**: Adicionei uma função no código para que não fosse necessário informar manualmente o caminho da pasta.
- **3ª Parte do Projeto**: Criei uma interface para que o programa não precisasse ser executado pelo terminal, melhorando a intuição e a experiência do usuário.
- **4ª Parte**: Criei o arquivo de versão (`version.txt`).
- **5ª Parte**: Criei o compilador (`compilador.py`).
- **6ª Parte**: Realizei a compilação do software e disponibilizei aos computadores dos usuários via AnyDesk.

## Informação Documentada

- [Documentação do Projeto](https://descomplica2-my.sharepoint.com/:w:/g/personal/delean_2444070_aluno_faculdadedescomplica_com_br/ETkGd5quBbdDlRpbeOilzvcBpsXROP3t3QbiCxx5hkVtkw?e=Qrq4mq)
- [Roteiro do Projeto](https://descomplica2-my.sharepoint.com/:w:/g/personal/delean_2444070_aluno_faculdadedescomplica_com_br/EWoeghM5UuZOisuQEx7kSwgBP1ojKAonvG2zkhfZtY5oqQ?e=3N3x69)

## Conclusão

A igreja passou a ter um software desenvolvido por mim que automatiza suas tarefas. O que antes levava de 6 a 8 horas para realizar, agora é feito em alguns minutos com o novo software desenvolvido e distribuído de forma gratuita por mim.
