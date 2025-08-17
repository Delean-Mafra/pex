# Política de Segurança e Privacidade / Security & Privacy Policy

Projeto: CDADOS – Projeto de Extensão I – Exclusão de Arquivos Duplicados
Versão Atual: **3.0.0.0** (migração da interface de Tkinter para Flask – operação local em navegador)
Licença de Conteúdo / Documentação: **CC BY-NC-SA 4.0**
Autor / Maintainer: **Delean Mafra (2024–2025)**

---
## 1. Escopo / Scope
Este documento descreve a política de segurança, privacidade, suporte de versões e processo de reporte de vulnerabilidades do software. / This document outlines the security, privacy, supported versions and vulnerability reporting process of the software.

---
## 2. Versões Suportadas / Supported Versions
| Versão | Suporte | Notas |
|--------|---------|-------|
| 3.0.0.3 | :white_check_mark: | Versão atual (UI Flask) |
| 3.0.0.0 | :white_check_mark: | Suporte de transição limitado |
| 2.0.0.47 | :warning: | Manutenção corretiva apenas (legacy Tkinter) |
| < 2.0.0.0 | :x: | Sem suporte |

Legenda: :white_check_mark: (ativo) · :warning: (parcial) · :x: (descontinuado)

> Novos patches de segurança são aplicados prioritariamente à versão 3.x. Correções só são retroportadas para 2.0.0.2 se tecnicamente viáveis.

---
## 3. Modelo de Execução Local / Local Execution Model
- A aplicação é executada **localmente** em `localhost` (ex.: `http://127.0.0.1:5000/`).
- Não envia dados a servidores externos.
- Não realiza telemetria, coleta analítica ou rastreamento de uso.
- O diálogo de seleção de pasta usa `tkinter.filedialog` apenas para obter um caminho local (não expõe o caminho para fora do host).

---
## 4. Dados Processados / Data Processed
| Tipo | Origem | Retenção | Transmissão Externa |
|------|--------|----------|---------------------|
| Arquivos PDF / Imagem | Pasta escolhida | Não armazenados pelo app (somente leitura e possível exclusão de duplicados) | Nenhuma |
| Hashes de Conteúdo | Gerados em memória | Volátil | Nenhuma |
| Log de Exclusão (`log_exclusao.txt`) | Gerado localmente | Persistente local (texto) | Nenhuma |
| Caminho da Pasta | Seleção do usuário | Volátil (exceto em mensagens de retorno) | Nenhuma |

### Observações
- O arquivo de log contém nomes (paths) dos arquivos excluídos e timestamps. **Não** inclui conteúdo dos arquivos.
- Não há envio de hashes, nomes de arquivos ou caminhos a terceiros.

---
## 5. Privacidade / Privacy
### Português
O software não coleta dados pessoais. Todo processamento ocorre no ambiente do usuário. É responsabilidade do operador garantir que a pasta selecionada não contenha arquivos sigilosos cuja exclusão acidental possa comprometer processos administrativos.

### English
The software does not collect personal data. All processing occurs locally. It is the operator's responsibility to ensure the chosen folder does not contain confidential files whose accidental deletion could impact administrative processes.

---
## 6. Segurança Operacional / Operational Security
| Medida / Measure | Descrição |
|------------------|-----------|
| Execução Local | Elimina dependência de rede para operação principal. |
| Hash por Conteúdo | Reduz risco de falsos positivos ao comparar duplicados. |
| Exclusão Imediata | Arquivo duplicado é removido após detecção; recomenda-se backup manual prévio. |
| Log Centralizado | Rastreabilidade das exclusões para auditoria. |
| Supressão de Reloader | Evita duplicação de processos (Flask `use_reloader=False`). |
| Limitação de Escopo | Apenas extensões suportadas (PDF, PNG, JPEG). |

### Recomendações ao Usuário
1. Testar em uma cópia da pasta antes de usar em ambiente oficial.  
2. Versionar ou arquivar dados críticos (backup incremental) antes de grandes exclusões.  
3. Restringir acesso ao executável a usuários autorizados.  
4. Se integrar em fluxo maior, adicionar controle de acesso (auth + TLS reverso, se exposto).  

---
## 7. Vetores de Risco Conhecidos / Known Risk Vectors
| Vetor | Risco | Mitigação Recomendada |
|-------|-------|-----------------------|
| Exclusão Irreversível | Perda de arquivo que era referência adotada erroneamente como duplicado | Backup/quarentena antes de exclusão (futuro) |
| PDF Sem Texto | Conteúdo igual baseado em imagem não detectado se OCR não aplicado | Integração futura com OCR (Tesseract) |
| Execução em Rede Compartilhada | Delay ou condições de corrida em arquivos sendo usados por outros processos | Executar em janela de manutenção / lock de uso |
| Modificação Durante Escaneamento | Hash inconsistente se arquivo alterado no meio do processo | Bloquear alterações (copiar para staging) em cenários críticos |

---
## 8. Logs
- Arquivo: `log_exclusao.txt`.
- Conteúdo: timestamp, ação (EXCLUIDO / ERRO), caminho do arquivo.
- Sensibilidade: Baixa (metadados). Pode revelar estrutura interna de diretórios — proteger em ambientes sensíveis.

### Rotação (Sugestão)
Implementar rotação manual ou script de arquivamento se o volume crescer. (Não implementado nativamente.)

---
## 9. Dependências Críticas / Critical Dependencies
| Pacote | Uso | Notas de Segurança |
|--------|-----|--------------------|
| Flask | Servidor local / rotas | Manter atualizado (corrige CVEs rapidamente). |
| Pillow | Processar imagens | Preferir versões recentes (corrige parsing). |
| PyPDF2 | Leitura de PDFs | PDFs malformados devem ser tratados com try/except. |
| Tkinter | Diálogo de pasta | Uso mínimo; não expõe conteúdo além do caminho. |

> Recomenda-se verificação periódica de CVEs (ex.: `pip audit`).

---
## 10. Construção & Integridade / Build & Integrity
- Empacotamento via `PyInstaller` (`version_compilador.py`).
- Suporte a assinatura de código (certificado `.pfx`).
- Verificar hash do executável após distribuição quando a cadeia de confiança for crítica.

### Cadeia de Confiança
Se assinatura digital for aplicada, validar com:
- `signtool verify /pa arquivo.exe` (Windows)  
- ou ferramenta equivalente.

---
## 11. Reporte de Vulnerabilidades / Vulnerability Reporting
Envie (em ordem de prioridade):
1. Descrição clara do problema.
2. Passos para reprodução.
3. Impacto estimado.
4. Ambiente (SO, versão do app, hash do executável).

Canais sugeridos (exemplos – ajustar conforme divulgação real):
- E-mail institucional do mantenedor.
- Canal interno autorizado da organização.

Tempo alvo de resposta inicial: **5 dias úteis**.

Divulgação responsável: Não publique detalhes antes de correção acordada.

---
## 12. Política de Atualizações / Update Policy
- Versão 3.x recebe novas features + correções.
- Versões 2.x: apenas correções críticas (quando simples e seguras).
- Releases numeradas `MAJOR.MINOR.PATCH.BUILD`.

---
## 13. Alterações Nesta Versão 3.0 (Resumo de Segurança)
| Mudança | Impacto |
|---------|---------|
| Migração para Flask | Melhora flexibilidade e separação de camadas; atenção a exposição inadvertida (recomenda-se manter local). |
| Remoção de `pex.lic` | Reduz superfície de dependências externas. |
| Hash de Conteúdo Consolidado | Aumenta precisão na detecção; pequeno custo de CPU. |
| Supressão de Reloader | Evita múltiplas threads acessando simultaneamente o mesmo diretório. |
| Log Unificado | Auditoria simplificada. |

---
## 14. Futuras Melhorias de Segurança / Future Security Enhancements
1. Modo "quarentena" em vez de exclusão imediata.
2. OCR para PDFs baseados em imagem.
3. Cache incremental de hashes com verificação de integridade.
4. Assinatura reproduzível (reproducible builds) com manifesto de dependências fixadas.
5. Endpoint opcional de status com token de acesso (se ampliado para rede interna).

---
## 15. Declaração de Isenção / Disclaimer
O software é fornecido "no estado em que se encontra" para uso administrativo interno. Cabe ao operador validar se o conjunto de arquivos submetidos pode ser excluído de forma segura.

---
## 16. Direitos Autorais / Copyright
© 2025 Delean Mafra – Todos os direitos reservados.  
Documento e conteúdo sob licença **CC BY-NC-SA 4.0**.

---
# English Section (Mirror)

## 1. Scope
This document defines security, privacy, supported versions, and vulnerability reporting process.

## 2. Supported Versions
| Version | Support | Notes |
|---------|---------|-------|
| 3.0.0.3 | :white_check_mark: | Current (Flask UI) |
| 2.0.0.0 | :white_check_mark: | Transitional limited support |
| 2.0.0.47 | :warning: | Security fixes only if trivial |
| < 2.0.0.0 | :x: | Unsupported |

## 3. Local Execution Model
Runs only on localhost; no external telemetry; no uploads.

## 4. Data Processed
- Reads PDF / image files, computes hashes in memory.
- Deletes confirmed duplicates immediately.
- Writes a local text log with filenames only.

## 5. Privacy
No personal data intentionally collected. All operations stay on the local machine.

## 6. Operational Security
- Content hashing (PDF text, normalized image bytes).
- Single-process (reloader disabled).
- Optional code signing for integrity.

## 7. Known Risks
| Vector | Risk | Mitigation |
|--------|------|-----------|
| Immediate deletion | Loss of needed file | Add quarantine (future) |
| Image-only PDFs | Undetected duplicates | OCR enhancement (future) |
| Concurrent edits | Inconsistent hash | Run during maintenance window |

## 8. Logging
`log_exclusao.txt` – local only; contains filenames; treat as low-sensitivity metadata.

## 9. Dependencies
Keep Flask, Pillow, PyPDF2 updated; audit regularly (`pip audit`).

## 10. Build & Integrity
Packaged via PyInstaller; optional code signing; verify signature/hash after distribution.

## 11. Vulnerability Reporting
Provide steps, impact, environment details. Private disclosure first. Target initial response within 5 business days.

## 12. Update Policy
3.x = features + fixes; 2.x = critical fixes only; semantic versioning with 4 fields.

## 13. 3.0 Security Changes Summary
- Migrated to Flask (flexibility, modularity)
- Removed external license file dependency
- Unified robust content hashing
- Disabled auto reloader
- Centralized logging

## 14. Future Security Enhancements
Quarantine mode; OCR for image-only PDFs; incremental hash cache; reproducible builds; optional auth-protected status endpoint.

## 15. Disclaimer
Provided as-is for internal administrative use. Operator responsible for validating safe deletion.

## 16. Copyright
© 2025 Delean Mafra – All rights reserved. CC BY-NC-SA 4.0.

---
**Fim / End**
