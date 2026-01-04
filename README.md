[![DOI](https://zenodo.org/badge/898218271.svg)](https://doi.org/10.5281/zenodo.18142968)

# PROJETO DE EXTENSÃO I - Exclusão de Arquivos Duplicados v3.0

Projeto de Extensão I (CDADOS) – Ferramenta para identificar e excluir arquivos duplicados (PDF, PNG, JPEG/JPG) com interface web.

> Esta é a versão **3.0** do projeto. Nesta atualização a interface original em **Tkinter** foi substituída por **Flask**, trazendo maior flexibilidade de uso para os integrantes administrativos da **IGREJA APOSTÓLICA RENASCER EM CRISTO**.

## Objetivo
Eliminar arquivos duplicados em uma pasta informada pelo usuário, liberando espaço e organizando melhor o acervo digital (documentos e imagens). A ferramenta oferece:
- Interface web simples (abrindo no navegador automaticamente)
- Seleção da pasta via diálogo nativo (Tkinter) ou digitação manual
- Remoção segura de duplicados baseada no conteúdo real dos arquivos
- Geração de log detalhado das exclusões
- Exibição de direitos autorais via iframe externo

## Principais Mudanças da Versão 3.0
| Item | Antes (v2.x) | Agora (v3.0) |
|------|--------------|--------------|
| Interface | Tkinter | Flask (UI web responsiva + Tailwind) |
| Dependência de `pex.lic` | Obrigatória para apontar caminho | Removida (usuário informa o caminho na página) |
| Seleção de pasta | Somente leitura via arquivo de licença | Botão "Selecionar Pasta" (diálogo nativo) + campo manual |
| Feedback de progresso | Caixa de diálogo simples | Página dinâmica com mensagens e log | 
| Direitos autorais | Texto local | Iframe para página oficial externa |
| Empacotamento | PyInstaller básico | Script de compilação com assinatura digital|

## Como a Detecção de Duplicados Funciona
1. Percorre recursivamente a pasta selecionada.
2. Para cada arquivo suportado:
   - PNG / JPEG: a imagem é aberta com **Pillow**, convertida para bytes PNG normalizados e então calculado um hash SHA-256.
   - PDF: o texto de cada página é extraído via **PyPDF2** e concatenado no hash.
   - (Outros tipos – ignorados nesta versão.)
3. Mantém-se um dicionário `hash -> caminho`. Se um novo arquivo gera um hash já visto, ele é considerado duplicado e removido.
4. Cria-se um `log_exclusao.txt` no diretório do script (ou fallback em *Documents* se não houver permissão).

### Vantagens da Estratégia
- Compara conteúdo real, não apenas nomes ou tamanhos.
- Minimiza falsos positivos (mesmo nome diferente → detecta duplicidade se conteúdo igual).

### Limitações / Observações
- Extração de texto de PDFs depende da qualidade do documento (PDFs só imagem sem camada de texto não são comparados pelo conteúdo visual).
- O navegador não pode (por segurança) fornecer o caminho absoluto local; o botão de seleção abre um diálogo nativo via rota `/select_folder` (usa Tkinter no host). Em modo totalmente headless isso não estará disponível.
- Se a pasta contiver muitos arquivos grandes, a operação pode levar tempo (hashing é O(n)).

## Estrutura dos Arquivos Principais
| Arquivo | Função |
|---------|--------|
| `PROJETO DE EXTENSÃO I.py` | Aplicação Flask + lógica de exclusão + UI embutida em `INDEX_HTML` |
| `version_compilador.py` | Script de build PyInstaller (gera executável e faz assinatura digital) |
| `version.txt` | Metadados de versão usados pelo PyInstaller (`--version-file`) |
| `ico.png` | Ícone do executável |
| `log_exclusao.txt` | Log gerado após cada execução (se houver duplicados ou tentativa de análise) |

## Dependências
Mínimas para runtime:
- Flask
- Pillow (PIL)
- PyPDF2

Se ainda não tiver um `requirements.txt` apropriado, você pode instalar rapidamente:
```
pip install flask Pillow PyPDF2
```

## Execução em Ambiente de Desenvolvimento
```
python "PROJETO DE EXTENSÃO I.py"
```
O script:
1. Inicia o servidor Flask em `http://127.0.0.1:5000/`
2. Abre automaticamente o navegador padrão.
3. Permite digitar ou selecionar a pasta.
4. Exibe resultado e caminho do log.

## Geração do Executável (PyInstaller)
Use o script automatizado:
```
python version_compilador.py
```
O que ele faz:
1. Incrementa o campo `ProductVersion` em `version.txt`.
2. Limpa diretórios anteriores (`build/`, `dist/`, `__pycache__`, `.spec`).
3. Executa PyInstaller com:
   - `--onefile`
   - Ícone personalizado (`ico.png`)
   - Hidden imports necessários (Flask, PIL, PyPDF2, tkinter.filedialog)
4. Assina o executável usando certificado `certificado-code-signing.pfx` se presente e senha configurada.

### Ajustes Possíveis
- Remover `--console` para ocultar o terminal.
- Adicionar compressão UPX se instalado: `--upx-dir=...`.
- Incluir mais hidden imports caso módulos dinâmicos sejam adicionados futuramente.

## Segurança e Boas Práticas
- Sempre revise os arquivos listados para exclusão se for adaptar a lógica; atualmente a remoção acontece imediatamente ao detectar duplicado.
- Considere adicionar uma opção de *backup/ quarentena* antes de exclusão definitiva (já há espaço no front-end para futuras flags).
- Não sirva esta aplicação diretamente exposta à Internet sem autenticação (é uma ferramenta local administrativa).

## Manutenção e Suporte
Embora o projeto original já tenha sido finalizado e entregue, esta versão 3.0 foi mantida e atualizada voluntariamente para oferecer maior usabilidade e suporte contínuo aos processos administrativos da **IGREJA APOSTÓLICA RENASCER EM CRISTO**.

## Créditos e Direitos Autorais
Desenvolvido por **Delean Mafra** – 2025

Direitos autorais: © 2025 Delean Mafra – Todos os direitos reservados.

Licença de conteúdo/documentação: **CC BY-NC-SA 4.0** (Atribuição, Não Comercial, Compartilha Igual).

Página de direitos autorais exibida via iframe: https://delean-mafra.github.io/pex/direitos_autorais

## Próximas Melhorias (Ideias)
- Opção de backup automático antes de excluir.
- Suporte a mais tipos de arquivos (DOCX, XLSX) usando leitura de conteúdo textual.
- Relatório HTML detalhado com estatísticas de espaço economizado.
- Integração com OCR para PDFs baseados em imagem.

## Contato
Para dúvidas ou suporte adicional, consulte os contatos oficiais do mantenedor (Delean Mafra) conforme divulgados nos canais institucionais.

---
**Versão:** 3.0  |  **Framework UI:** Flask  |  **Substitui:** Interface Tkinter anterior
