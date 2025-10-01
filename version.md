# Changelog Versão 3.0.0.0

## Resumo da Versão
A versão 3.0.0.0 marca a migração da interface principal de **Tkinter** para **Flask**, oferecendo uma experiência totalmente baseada em navegador, mais flexível, moderna e simples de operar pelos integrantes administrativos da **IGREJA APOSTÓLICA RENASCER EM CRISTO**. Foram removidas dependências estruturais (como o arquivo `pex.lic`) e ampliada a automação de build, mantendo a lógica central de identificação e exclusão de arquivos duplicados (PDF / PNG / JPEG) com maior clareza e profissionalismo.

---

## Alterações Realizadas

### Substituição / Reorganização de Tecnologias
- **Interface Principal:**
  - Antes: 100% em **Tkinter**.
  - Agora: **Flask** (UI web responsiva + Tailwind CDN) abrindo automaticamente no navegador.
- **Tkinter** permanece de forma pontual apenas para o *diálogo nativo de seleção de pasta* (rota `/select_folder`).
- **Removido:** Dependência operacional de `pex.lic` para determinar caminho.
- **Adicionado / Consolidado:**
  - Flask (servidor local)
  - Estrutura HTML/CSS embutida (single-file)
  - Iframe para exibição dinâmica de direitos autorais
  - Ampliação do uso de `pathlib` para robustez de caminhos

### Evolução da Arquitetura
| Componente | Antes (2.x) | Agora (3.0) |
|------------|-------------|-------------|
| UI | Janela Tkinter | Página Web Flask (single file) |
| Seleção de Pasta | Leitura de `pex.lic` ou manual | Botão "Selecionar Pasta" (diálogo nativo) + campo livre |
| Direitos Autorais | Texto estático interno | Iframe externo oficial |
| Log | Mensagens locais simples | `log_exclusao.txt` centralizado com fallback seguro |
| Build | Script básico | `version_compilador.py` com versão, limpeza, hidden imports e assinatura opcional |
| Execução duplicada | Possível via reloader | Prevenção: `use_reloader=False` + supressão de logs |
| Comparação PDF | Parcial / básica | Extração de texto por página (PyPDF2) + hashing concatenado |

---

## Implementações e Melhorias

### 1. Nova Interface Web (Flask)
**Benefícios:**
- Independência de resolução / layout do SO.
- Facilidade de operação (link local abre sozinho: `http://127.0.0.1:5000/`).
- Possibilidade futura de adicionar novas abas e endpoints sem reestruturar janelas.
- Uso de Tailwind via CDN para estilização rápida e consistente.

### 2. Mecanismo Unificado de Hash de Conteúdo
- **Imagens (PNG / JPEG):** Normalização via Pillow convertendo para bytes PNG padronizados → hash SHA-256.
- **PDF:** Extração de texto página a página com PyPDF2; concatenação segura no buffer de hash.
- **Resultado:** Redução de falsos negativos; base de comparação independente de nomes.

### 3. Remoção da Dependência de `pex.lic`
- O caminho é agora informado diretamente ou selecionado via diálogo.
- Elimina acoplamento a arquivos externos e simplifica distribuição.

### 4. Log Estruturado
- `log_exclusao.txt` registra exclusões e decisões.
- Fallback automático para diretório de Documentos caso não haja permissão.

### 5. Automação de Build Avançada
- Script `version_compilador.py`:
  - Incremento automático de versão (controle em `version.txt`).
  - Limpeza prévia de artefatos (build/dist/spec/__pycache__).
  - Empacotamento PyInstaller `--onefile` com ícone.
  - Inserção de hidden imports: Flask, PIL, PyPDF2, tkinter.
  - Coleta de recursos dinâmicos (`--collect-all=PyPDF2`).
  - Assinatura digital opcional (uso de `certificado-code-signing.pfx`).

### 6. Estabilidade e Robustez
- Desativado o reloader do Flask para impedir execução dupla.
- Supressão de logs excessivos do Werkzeug.
- Uso consistente de `pathlib` evita problemas de escape (ex: `\b`).
- Tratamento de exceções em leitura de arquivos (corrupção / permissões).

### 7. Direitos Autorais Dinâmicos
- Exibição via iframe apontando para página oficial externa.
- Facilita atualização de textos sem rebuild.

### 8. Segurança Operacional
- Sem upload de arquivos: apenas caminhos locais processados.
- Aplicativo destinado a uso local administrativo (não expor publicamente sem autenticação).

### 9. Base Preparada para Extensões Futuras
- Estrutura de rotas permite adicionar endpoints (status, relatório, API JSON) sem refatoração pesada.
- Facilidade para introduzir fila assíncrona ou barra de progresso incremental.

---

## Linha do Tempo da Evolução 3.0
1. **Fase 1 – Refatoração da Lógica Core:** Adaptação da função de verificação para uso em contexto web.
2. **Fase 2 – Remoção de `pex.lic`:** Parametrização de input via formulário e diálogo nativo.
3. **Fase 3 – Construção da Página Única:** HTML + JS + Tailwind embutidos no mesmo arquivo `.py`.
4. **Fase 4 – Hashing Aprimorado:** Consolidação da extração de texto PDF e normalização de imagens.
5. **Fase 5 – Automação de Build:** Revisão do script de compilação, inclusão de assinatura e hidden imports.
6. **Fase 6 – Direitos Autorais Externos:** Substituição de bloco fixo por iframe dinâmico.
7. **Fase 7 – Otimizações Finais:** Remoção de reloader, supressão de logs, auto-abertura no navegador.

---

## Compatibilidade e Migração a partir da 2.x
| Ação | Necessário? | Observação |
|------|-------------|-----------|
| Excluir `pex.lic` | Recomendado | Não é mais utilizado. |
| Ajustar atalhos / scripts | Sim | Aponte agora para `PROJETO DE EXTENÇÃO I.py` ou executável gerado. |
| Instalar novas dependências | Possível | `flask`, `Pillow`, `PyPDF2` (caso não presentes). |
| Reconfigurar build | Sim | Usar `version_compilador.py` em vez do antigo `compilador.py`. |

---

## Considerações Técnicas
- Complexidade principal: O(n) para hashing (n = quantidade de arquivos). Bottleneck: I/O + leitura de PDF.
- Possível evolução: Cache de hashes (ex: SQLite) ou threading para diretórios muito grandes.
- PDFs baseados somente em imagem não terão texto extraído; comparar via OCR seria um próximo passo.

---

## Exemplo Simplificado da Função de Verificação
```python
def verificar_duplicados(caminho_pasta):
    # Percorre diretórios, calcula hash de conteúdo e remove duplicados encontrados.
    # Mantém dicionário hash->caminho e registra exclusões em log_exclusao.txt
    ...
```

---

## Referências Internas
- `PROJETO DE EXTENÇÃO I.py`: App Flask + UI embutida.
- `version_compilador.py`: Automação de build e assinatura.
- `version.txt`: Metadados de versão (usado pelo PyInstaller).

---

## Continuidade e Suporte
Mesmo após a entrega anterior, decidiu-se manter suporte evolutivo voluntário, modernizando a experiência de uso e garantindo longevidade operacional da ferramenta para a **IGREJA APOSTÓLICA RENASCER EM CRISTO**.

---

## Próximos Passos Sugeridos
1. Barra de progresso assíncrona (AJAX / WebSocket).
2. Relatório HTML detalhado (estatísticas de espaço economizado).
3. Modo "quarentena" antes da exclusão definitiva.
4. Extensão de tipos (DOCX / XLSX / PPTX) via extração textual.
5. OCR para PDFs baseados em imagem.

---

## Créditos
© 2025 Delean Mafra – Todos os direitos reservados.

Versão 3.0.0.0 – Interface principal em Flask, mantendo apenas seleção de pasta via diálogo nativo.
