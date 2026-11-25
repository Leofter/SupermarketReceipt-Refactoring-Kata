# Relatório da Terceira Avaliação de Segurança (Refatorado v2)

**Projeto:** Supermarket Receipt Refactoring Kata (Python + pytest + SQLite/SQLAlchemy)  
**Data/Hora da Reavaliação (UTC):** 2026-11-24 21:43:00 UTC (carimbo dos artefatos Bandit)  
**Data de Consolidação do Relatório (UTC):** 2026-11-25 21:34:50 UTC  
**Branch Git:** `feature/reavaliacao_3`  
**Commit Git de Referência:** `35bac2142b8106d6d3d03af1698f87abfe0c24f4`  
**Alvo da Reavaliação:** `project/tests` (lacuna apontada na segunda avaliação), `project/src` (incluindo a nova camada `infrastructure/database`) e `project/main.py`  
**Pasta de Evidências:** `docs/security/terceira_avaliacao_refatorado_v2/security/`  
**Ambiente:** Ambiente isolado de segurança (Bandit 1.9.4, pip-audit 2.10.1, Safety 3.8.1)

---

## 1. Sumário Executivo da Terceira Avaliação

Este relatório fecha o ciclo de reavaliações de segurança do projeto. A segunda avaliação analisou exclusivamente o código de produção (`project/src`) e deixou explicitamente fora de escopo os arquivos de testes implementados em `project/tests/`. A terceira reavaliação amplia o escopo para esses testes e para a nova implementação de persistência em banco de dados (SQLite via SQLAlchemy), mantendo a mesma metodologia (Bandit, pip-audit e Safety) e o comparativo com a linha de base e com a reavaliação anterior.

### Principais Conclusões:

1. **Bandit (SAST):**
   - **Código de produção (`project/src` + `project/main.py`):** **0 vulnerabilidades** em **647 linhas de código** (artefato arquivado), sem achados de severidade `High`, `Medium` ou `Low`.
   - **Varredura completa (`project/`):** **973 linhas**, com **29 alertas `B101:assert_used`** (severidade `Low`, confiança `High`) distribuídos em 4 arquivos de teste. Trata-se do mesmo ruído de teste identificado na linha de base (7 alertas), porém ampliado em função da nova suíte. Nenhum alerta real de segurança foi encontrado.
   - **Verificação complementar pós-banco (ver §3.1):** com a camada de persistência já integrada, produção passou a **732 LOC — 0 achados** e a varredura completa passou a **1152 LOC — 34 alertas `B101`** (os 5 adicionais em `project/tests/test_sqlite_repositories.py`), todos igualmente classificados como ruído de teste.
2. **pip-audit (SCA):**
   - Resultado: **`No known vulnerabilities found`**. Foram congelados 5 pacotes e o JSON estruturado lista 4 dependências sem vulnerabilidades (`iniconfig`, `pluggy`, `Pygments`, `pytest`).
   - A verificação complementar sobre o `project/requirements.txt` atual (`SQLAlchemy==2.1.9` + `pytest==9.2.0`) também retornou **0 vulnerabilidades**, cobrindo a dependência introduzida pelo banco de dados.
   - As 16 vulnerabilidades do `urllib3==2.0.6` da linha de base continuam **eliminadas**.
3. **Safety (SCA):**
   - **Não conclusivo nesta rodada:** a CLI não estava autenticada e a execução foi interrompida com `EOF when reading a line`. Não há artefato JSON de Safety nesta pasta (ao contrário das avaliações anteriores). O resultado não deve ser lido como "0 vulnerabilidades do Safety", e sim como **execução não realizada por limitação de autenticação**.

> [!NOTE]
> **Ressalva de Segurança:** As ferramentas cobrem padrões estáticos e vulnerabilidades conhecidas (CVEs/PYSEC catalogadas). Elas não comprovam segurança absoluta, não detectam falhas lógicas de negócio nem ataques zero-day. Além disso, os artefatos arquivados nesta pasta foram gerados em 2026-11-24 21:43 UTC, antes do merge da implementação do banco (commit `3f395fa`, 2026-11-25); por isso, os números da camada de persistência são apresentados separadamente como verificação complementar (§3.1 e §3.2).

---

## 2. Metodologia e Ambiente da Terceira Avaliação

As informações primárias estão consolidadas nos arquivos de evidência de [docs/security/terceira_avaliacao_refatorado_v2/security/](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/).

| Propriedade | Valor Registrado |
| :--- | :--- |
| **Data/Hora dos Artefatos (UTC)** | 2026-11-24 21:43:00 UTC (Bandit: `21:43:00.388616` para produção e `21:43:00.543371` para varredura completa) |
| **Branch Git** | `feature/reavaliacao_3` |
| **Commit Git Atual** | `35bac2142b8106d6d3d03af1698f87abfe0c24f4` |
| **Alvos Analisados** | `project/src`, `project/tests`, `project/main.py` e `project/requirements.txt` |
| **Diretório Raiz dos Comandos** | `/home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata` |
| **Ambiente de Execução do Safety** | `/tmp/sec-venv` (Python 3.13, conforme avisos de Deprecation no artefato) |

### Versões das Ferramentas Utilizadas:
- **Bandit:** `1.9.4` (registrado nos metadados `more_info` do JSON e na saída TXT).
- **pip-audit:** `2.10.1` (conforme README do projeto e avaliações anteriores).
- **Safety:** `3.8.1` (conforme README do projeto e avaliações anteriores; autenticação ausente nesta rodada).
- **Dependências congeladas:** `iniconfig==2.3.1`, `packaging==26.4`, `pluggy==1.7.0`, `Pygments==2.21.0`, `pytest==9.2.0`.

### Escopos executados (reconstruídos a partir das evidências):

| Ferramenta | Escopo / Comando | Evidência Gerada |
| :--- | :--- | :--- |
| Bandit | `python -m bandit -r project/src project/main.py` (647 LOC) | [after_bandit_src.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_src.txt) |
| Bandit | `python -m bandit -r project` (973 LOC, TXT e JSON) | [after_bandit_all.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.txt) e [after_bandit_all.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.json) |
| pip-audit | `python -m pip_audit -r .../after_pip_freeze.txt --no-deps` (TXT e JSON) | [after_pip_audit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.txt) e [after_pip_audit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.json) |
| Safety | `python -m safety scan ...` (sem token de acesso) | [after_safety.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_safety.txt) |

---

## 3. Resultados Detalhados da Terceira Avaliação

### 3.1 Análise Estática de Código (SAST) - Bandit

#### 3.1.1 Código de Produção

```text
Run started: 2026-11-24 21:43:00.388616+00:00
Test results: No issues identified.
Total lines of code: 647 | #nosec: 0 | regras desabilitadas: 0
Severidade: Undefined 0, Low 0, Medium 0, High 0
Confiança:  Undefined 0, Low 0, Medium 0, High 0
```

- **Código de saída:** `0` (sucesso).
- **Evidência:** [after_bandit_src.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_src.txt).

#### 3.1.2 Varredura Completa (produção + testes)

- **Total de linhas analisadas:** 973 (`project/main.py`: 48 LOC; `project/src`: 599 LOC; `project/tests`: 326 LOC).
- **Métricas por severidade:** `High: 0`, `Medium: 0`, `Low: 29`, `Undefined: 0`.
- **Métricas por confiança:** `High: 29`, `Medium: 0`, `Low: 0`, `Undefined: 0`.
- **Arquivos com achados:** todos os 29 alertas são `B101:assert_used` (CWE-703) em arquivos de teste:

| Arquivo de Teste | LOC | Alertas `B101` | Trecho Representativo |
| :--- | ---: | ---: | :--- |
| `project/tests/test_combo_discount.py` | 139 | 13 | `assert out.total_discount == pytest.approx(expected_discount)` (linhas 54, 55, 94-96, 124-125, 133-135, 163-165) |
| `project/tests/test_domain_entities.py` | 40 | 5 | `assert receipt.total_price() == pytest.approx(2.00)` (linhas 25, 47, 56-58) |
| `project/tests/test_legacy_offers.py` | 90 | 10 | `assert out.total_price == pytest.approx(0.99)` (linhas 21-22, 27-28, 54-55, 71-72, 107-108) |
| `project/tests/test_receipt_and_checkout.py` | 43 | 1 | `assert receipt_text == expected` (linha 51) |
| `project/tests/conftest.py` | 14 | 0 | — (apenas fixtures) |

**Diagnóstico:** o uso de `assert` é a forma padrão de verificação do `pytest`, portanto os 29 alertas são **falso positivo / ruído de teste**, semelhantes aos 7 alertas da linha de base. Nenhum alerta foi encontrado em `project/src` ou `project/main.py`.

#### 3.1.3 Verificação complementar após a integração do banco

Os artefatos arquivados foram gerados antes do merge da persistência SQLite (commit `3f395fa`). Uma repetição somente leitura das mesmas varreduras sobre o estado atual do branch confirmou a continuidade do resultado:

| Escopo | LOC | Achados Reais | Alertas `B101` (testes) |
| :--- | ---: | ---: | ---: |
| Produção (`project/src` + `project/main.py`, incluindo `infrastructure/database/`) | **732** | **0** | 0 |
| Completo (`project/`) | **1152** | **0** | **34** (13 + 5 + 10 + 1 + 5 em `test_sqlite_repositories.py`) |

O incremento de 85 LOC em produção corresponde aos arquivos `catalog_repository.py`, `offer_repository.py`, `sqlite_db.py` e modelos SQLAlchemy; nenhum deles gerou alerta estático.

### 3.2 Auditoria de Dependências (SCA) - pip-audit

Arquivo congelado analisado: [after_pip_freeze.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_freeze.txt).

| Pacote | Versão Congelada | Vulnerabilidades no JSON |
| :--- | :---: | :---: |
| `iniconfig` | 2.3.1 | 0 |
| `packaging` | 26.4 | não listada no JSON (sem achados) |
| `pluggy` | 1.7.0 | 0 |
| `Pygments` | 2.21.0 | 0 |
| `pytest` | 9.2.0 | 0 |

- **Saída textual:** `No known vulnerabilities found`.
- **JSON:** `{"dependencies": [4 entradas com "vulns": []], "fixes": []}`.
- **Avisos do pip-audit:** o uso de `--no-deps` é suportado, porém recomenda-se o hash completo das dependências fixadas (`pip-compile`).
- **Evidências:** [after_pip_audit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.txt) e [after_pip_audit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.json).

**Ressalva de escopo:** o congelamento arquivado não inclui `SQLAlchemy`, embora o `project/requirements.txt` atual o declare como `SQLAlchemy==2.1.9`. A verificação complementar executada sobre esse arquivo (com `--no-deps`) retornou igualmente `No known vulnerabilities found`, cobrindo a dependência de produção introduzida pelo banco de dados.

### 3.3 Auditoria com Safety

O Safety 3.8.1 foi invocado, mas a sessão não estava autenticada. A saída registrada foi:

```text
Please login or register Safety CLI (free forever) to scan and secure your projects with Safety
(R)egister for a free account in 30 seconds, or (L)ogin with an existing account to continue (R/L):
Unhandled exception happened: EOF when reading a line
```

- **Resultado:** **não executado** (interrompido por ausência de login interativo).
- **Evidência:** [after_safety.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_safety.txt).
- **Diferença em relação à segunda avaliação:** na reavaliação anterior houve login (`beatrizestevez29@gmail.com`) e o retorno foi `Tested 0 dependencies ... 0 security issues found`. Nesta rodada não há JSON de Safety na pasta de evidências, portanto o item permanece como **limitação operacional**, não como achado de vulnerabilidade.

---

## 4. Comparativo: Linha de Base vs. Reavaliação v1 vs. Terceira Avaliação v2

| Métrica / Dimensão de Análise | 1ª Avaliação (`python_pytest`) | 2ª Avaliação (`project/src`) | 3ª Avaliação (`project/tests` + banco) | Variação / Impacto |
| :--- | :--- | :--- | :--- | :--- |
| **LOC em produção** | 133 (212 com testes) | 545 (22 arquivos) | **647** (artefato) / **732** (pós-banco) | Crescimento esperado pela segregação em camadas e pela persistência; **0 achados reais** |
| **LOC em testes** | 79 | **Fora de escopo** | **326** (artefato) / **420** (pós-banco, incluindo `fakes/`) | Lacuna da segunda avaliação fechada; suíte de 30 testes no estado atual |
| **Achados Bandit em produção** | 0 (saída `0`) | 0 (saída `0`) | **0** (saída `0`) | Nenhuma fragilidade estática no código de negócio nem no acesso a dados |
| **Achados Bandit em testes** | 7 `B101` (Low/High) | Não avaliados | **29 `B101`** (artefato) / **34 `B101`** (pós-banco) | Aumento proporcional à suíte; ruído de `pytest`, não vulnerabilidade |
| **Severidade High/Medium** | 0 | 0 | **0 / 0** | Nenhum achado explorável nas três avaliações |
| **Dependências externas em runtime** | Indiretas (`requests`, `urllib3==2.0.6`) | Zero (Standard Library) | **`SQLAlchemy==2.1.9`** (SQLite) + `pytest==9.2.0` (dev) | Banco traz 1 dependência de produção, porém fixada e sem CVEs conhecidos |
| **Vulnerabilidades conhecidas (pip-audit)** | 16 no `urllib3` | 0 no escopo avaliado | **0** (5 pacotes congelados; 0 também em `SQLAlchemy==2.1.9`) | Risco de cadeia de suprimentos do legado eliminado |
| **Alertas do Safety** | 1 alerta de requisito não pinado (ignorado por política) | 0 (autenticado) | **Não executado** (`EOF`, sem token) | Limitação de autenticação, não regressão de segurança |

### Comparativo direto (2ª → 3ª avaliação)

- **Escopo ampliado:** de 545 LOC somente de produção para 973 LOC (produção + testes + `main.py`), chegando a 1152 LOC com o banco integrado.
- **Persistência:** de repositórios em memória para SQLite/SQLAlchemy, com acesso parametrizado via ORM (`Session.get`, `Session.merge`, `query(...).all()`), sem concatenação de SQL — reduzindo o risco de injeção.
- **Validação de dados:** inclusão da verificação de preço negativo antes de gravar no catálogo (`catalog_repository.py:20-21`), evitando persistência financeira inconsistente.
- **Testes de integração:** novo arquivo `test_sqlite_repositories.py` cobre cadastro, leitura, ofertas/combos e checkout integrado ao banco.

---

## 5. Pontos Fortes e Melhorias de Segurança Após as Mudanças

### 1. Fechamento da Lacuna de Cobertura dos Testes
A segunda avaliação excluiu explicitamente `project/tests`. A terceira analisou 326 LOC de testes (420 no estado atual, incluindo os fakes), confirmando que toda a nova suíte — domínio, ofertas legadas, combos, recibo e persistência — está livre de padrões inseguros além do `assert` idiomático do `pytest`.

### 2. Persistência Segura com SQLAlchemy
- A camada `src/infrastructure/database/` usa `create_engine`, `Base.metadata.create_all` e `Session`, mantendo o domínio e os casos de uso isolados da infraestrutura (DIP).
- As consultas utilizam identificadores e parâmetros do ORM, e não strings SQL montadas dinamicamente; portanto não há vetor de injeção SQL nos repositórios atuais.
- A validação `if price < 0: raise ValueError(...)` antes do `merge`/`commit` impede a persistência de valores financeiros inválidos.

### 3. Superfície de Ataque Controlada
A dependência transitiva `urllib3==2.0.6` (16 CVEs) foi removida junto com `approvaltests`. O único pacote de produção adicionado, `SQLAlchemy==2.1.9`, está fixado em versão específica e foi confirmado sem vulnerabilidades conhecidas na verificação complementar.

### 4. Ruído de SAST Compreendido e Documentado
Os 29 (ou 34) alertas `B101` têm natureza conhecida e foram triados como falso positivo. Caso se deseje uma esteira 100% limpa, basta desabilitar `B101` somente para `project/tests` na configuração do Bandit, sem alterar as regras de produção.

### 5. Conformidade com a Política de Evidências
Todos os artefatos brutos (TXT e JSON) foram preservados na pasta `docs/security/terceira_avaliacao_refatorado_v2/security/`, permitindo auditoria independente e comparabilidade com as avaliações anteriores.

---

## 6. Ressalvas e Recomendações Finais

1. **Regerar os artefatos após o merge do banco:** os arquivos arquivados datam de 2026-11-24 21:43 UTC e não incluem `SQLAlchemy`, `src/infrastructure/database/` nem `test_sqlite_repositories.py`. Recomenda-se salvar uma nova rodada completa na mesma pasta para que o registro oficial reflita os 732/1152 LOC atuais.
2. **Restabelecer a autenticação do Safety:** repetir o scan com token válido (como na segunda avaliação) e arquivar o JSON correspondente; enquanto isso, o item permanece inconclusivo.
3. **Endurecer o pipeline de dependências:** manter versões fixadas e gerar hashes (`pip-compile --generate-hashes`) para eliminar o aviso do `pip-audit` sobre `--no-deps`.
4. **Cuidados operacionais com o SQLite:** restringir permissões do arquivo `project/supermarket.db`, não versionar dados de produção e validar a origem de `db_url` caso a aplicação passe a aceitar configuração externa.

---

## 7. Inventário de Evidências da Terceira Avaliação

Todos os arquivos brutos foram preservados em `docs/security/terceira_avaliacao_refatorado_v2/security/`:

- [after_bandit_src.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_src.txt): varredura do Bandit em `project/src` + `project/main.py` (647 LOC, 0 achados).
- [after_bandit_all.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.txt): saída textual da varredura completa (973 LOC, 29 alertas `B101`).
- [after_bandit_all.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.json): métricas estruturadas por arquivo e detalhamento dos 29 achados.
- [after_pip_freeze.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_freeze.txt): lista de pacotes congelados antes da auditoria.
- [after_pip_audit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.txt): saída textual com `No known vulnerabilities found`.
- [after_pip_audit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.json): estrutura JSON com as dependências avaliadas e `fixes: []`.
- [after_safety.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/security/after_safety.txt): registro da tentativa de scan interrompida por ausência de autenticação (não há JSON de Safety nesta rodada).
- [relatorio_terceira_avaliacao_seguranca.md](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/security/terceira_avaliacao_refatorado_v2/relatorio_terceira_avaliacao_seguranca.md): este relatório consolidado e comparativo.
