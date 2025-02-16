# CDADOS - Projeto de Extensão I - Delean Mafra

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
Visitei a igreja e conversei com o pastor Julian que é o oficial responsável pela tesouraria da igreja. Identifiquei as principais áreas de interesse e as questões a serem exploradas durante a visita.

### Contatos Iniciais
Estabeleci comunicação com os representantes da Igreja Renascer em Cristo para agendar reuniões e visitas. Falei inicialmente com o pastor Julian que informou que no último evento beneficente ele e o bispo da igreja acabaram perdendo praticamente o sábado inteiro pois receberam vários recibos de pagamentos duplicados, então eles precisaram fazer a conferência de mais de 100 recibos abrindo 1 a 1 para ver quais eram duplicados e quais ainda precisavam ser lançados no sistema financeiro da igreja. O mesmo mencionou que seria muito útil se existisse um sistema que identificasse os recibos duplicados e já os excluíssem para evitar o retrabalho. Confirmei a disponibilidade e obtive informações preliminares sobre a instituição.

### Realização de Reuniões
Conduzi reuniões iniciais com os representantes da Igreja Renascer em Cristo para discutir o contexto, a missão e as necessidades da instituição. Documentei as informações coletadas durante as reuniões, incluindo os desafios enfrentados e as oportunidades de colaboração. A documentação completa do projeto pode ser acessada pelo link: [CDADOS - Projeto de Extensão I - Delean Mafra](https://descomplica2-my.sharepoint.com/:w:/g/personal/delean_2444070_aluno_faculdadedescomplica_com_br/ETkGd5quBbdDlRpbeOilzvcBpsXROP3t3QbiCxx5hkVtkw?e=Qrq4mq)

### Participação em Atividades Locais
Participei de atividades e eventos organizados pela instituição para me familiarizar com o ambiente e entender melhor o funcionamento diário. Observei as operações e interagi com os membros da comunidade para obter insights práticos. Muitos dos membros da comunidade fizeram ou fazem faculdade na Descomplica na área de tecnologia, como o próprio Pr Julian e outros 4 membros (Joarle, Gabriel, Erick e seu primo Douglas).

### Estudo de Documentos e Materiais
Nesse caso, os documentos analisados foram apenas os recibos que eles precisavam automatizar a exclusão em caso de arquivos duplicados. Esses recibos, em sua maioria, eram em formato PDF, PNG e JPEG. Identifiquei informações relevantes que possam influenciar o planejamento das atividades de extensão.

### 2ª Parte do Projeto

A atualização no código permite ler automaticamente o caminho da pasta a partir de um arquivo de configuração (`pex.lic`), trazendo uma melhoria significativa em termos de usabilidade e eficiência. O sistema não exige que o usuário insira manualmente o caminho da pasta a cada execução, minimizando o tempo necessário para configurar e rodar o script. Esse aprimoramento torna o processo mais ágil, reduz a chance de erros de digitação ao informar o caminho e permite que a equipe execute a verificação de duplicados com um clique. Além disso, essa modificação facilita a integração do sistema com outros processos automatizados e garante uma experiência mais prática e acessível para a equipe da igreja.

### Observação

Inicialmente, optei por utilizar a biblioteca `kivy` para criar uma interface mais agradável, combinada com a biblioteca `cryptography` para criar um registro de licença criptografado, evitando que o programa fosse compartilhado com outras pessoas além do pastor Julian e do Bispo Gabriel. Infelizmente, tive diversos problemas com as duas bibliotecas, pois o código funcionava perfeitamente no meu ambiente de teste, porém, quando era compilado para um executável, ele não conseguia ler corretamente o registro de licença criado. Outro problema foi que a compilação do programa utilizando a biblioteca `kivy` era muito longa, levando aproximadamente 30 minutos para concluir cada compilação. Foram compiladas 47 versões (1.0.0.47) desse projeto inicial, totalizando aproximadamente 23 horas de programação e compilação do programa na versão 1.0.0.0.

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

### 5ª Parte do Projeto: Criação do Compilador em Python (`compilador.py`)

Na quinta parte do projeto, foi desenvolvido um compilador em Python com o objetivo de transformar o código em um executável (.exe), utilizando as bibliotecas `pyinstaller` e `subprocess`. Esta etapa é fundamental para a distribuição do software, permitindo que ele seja executado no ambiente dos usuários sem a necessidade de um interpretador Python instalado.

- **Profissionalismo**:
  - **Apresentação**: Oferecer o software como um executável melhora a apresentação e a experiência do usuário, conferindo ao projeto um aspecto mais profissional e refinado.

- **Automatização do Processo de Build**:
  - **Automação**: A utilização de um script de compilação automatiza o processo de build, tornando-o repetível e reduzindo a margem de erro, o que é particularmente útil para futuras atualizações e versões do software.

### Código Implementado

```python
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
    """Lê o caminho da pasta a partir de um arquivo de texto."""
    with open('pex.lic', 'r') as arquivo: 
        caminho_pasta = arquivo.readline().strip() 
    return caminho_pasta

def excluir_arquivos_duplicados():
    """Executa a função de exclusão de arquivos duplicados e exibe mensagem de conclusão"""
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
    btn_executar = tk.Button(root, text="Excluir Arquivos Duplicados", command=excluir_arquivos_duplicados)  
    btn_executar.pack(pady=20)  

    root.mainloop()  

if __name__ == "__main__":
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
