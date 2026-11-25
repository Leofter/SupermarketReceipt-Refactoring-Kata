# Relatório da Terceira Avaliação de Segurança (Refatorado v2) — Reexecução Completa

**Projeto:** Supermarket Receipt Refactoring Kata (Python + pytest + SQLite/SQLAlchemy)  
**Data/Hora da Reexecução (UTC):** 2026-11-25 22:29–22:34 UTC
**Branch Git:** `feature/reavaliacao_3`
**Commit Git de Referência do Código Avaliado:** `8db0849895ba641eb07eeb6a6617211a3b7bdb45`
**Alvo da Avaliação:** `project/` por completo — `project/src`, `project/tests`, `project/main.py` e `project/requirements.txt`
**Pasta de Evidências:** `docs/security/terceira_avaliacao_refatorado_v2/security/`
**Ambiente:** `supermarket-sec` (Python 3.12.16) para Bandit/Safety; venv temporário para isolar requisitos no pip-audit

---

## 1. Sumário Executivo

A terceira avaliação foi **apagada e refeita integralmente** a partir do estado atual do branch. A versão anterior desta pasta continha artefatos gerados antes do merge da persistência SQLite e registrava o Safety como **não executado** por ausência de autenticação. Nesta reexecução, a CLI do Safety foi autenticada pelo próprio usuário e o scan foi concluído com sucesso.

Resultados consolidados:

1. **Bandit (SAST):**
   - **Produção (`project/src` + `project/main.py`, incluindo `infrastructure/database/`):** **0 vulnerabilidades** em **732 LOC**, código de saída `0`.
   - **`project/` completo (exceto o diretório temporário legado `.approval_tests_temp`):** **1152 LOC**, **0 achados reais** e **34 alertas `B101:assert_used`** em testes (severidade `Low`, confiança `High`). Todos classificados como ruído esperado do `pytest`.
   - Os 34 alertas estão distribuídos em 5 arquivos de teste, incluindo os 5 novos alertas do arquivo de persistência `test_sqlite_repositories.py`.
2. **pip-audit (SCA):**
   - **`No known vulnerabilities found`** tanto sobre o `after_pip_freeze.txt` quanto sobre `project/requirements.txt`.
   - O congelamento registrou **7 pacotes**; o JSON estruturado listou **6 dependências avaliadas** (`iniconfig`, `pluggy`, `pygments`, `pytest`, `sqlalchemy`, `typing-extensions`), todas com `vulns: []` e `fixes: []`.
   - A dependência de produção introduzida pelo banco, `SQLAlchemy==2.1.9`, foi explicitamente coberta pela auditoria.
3. **Safety (SCA):**
   - Executado **autenticado** como `beatrizestevez29@gmail.com`, com política buscada da Safety Platform.
   - **2 dependências testadas** (`SQLAlchemy==2.1.9` e `pytest==9.2.0`), **0 problemas de segurança**, **0 correções sugeridas**, código de saída `0`.
   - Evidência JSON agora presente: `after_safety.json`, com `authenticated: true`.
4. **Sanidade funcional:**
   - `pytest -q`: **30 passed**, código de saída `0`.

> [!NOTE]
> **Ressalva de Segurança:** as ferramentas cobrem padrões estáticos e vulnerabilidades conhecidas catalogadas. Elas não comprovam segurança absoluta, não detectam falhas lógicas de negócio nem ataques zero-day. O diretório `.approval_tests_temp` foi excluído da varredura completa por ser artefato temporário legado, seguindo o critério da primeira avaliação.

---

## 2. O que mudou em relação à terceira avaliação anterior

| Item | Terceira avaliação anterior | Reexecução atual |
| :--- | :--- | :--- |
| **Artefatos** | Gerados em 2026-11-24 21:43 UTC, antes do merge do banco (`3f395fa`) | Regerados em 2026-11-25 sobre o código atual, já com banco e novos testes |
| **Produção Bandit** | 647 LOC no artefato original; 732 LOC apenas como verificação complementar | **732 LOC oficiais**, incluindo `infrastructure/database/` e `main.py` |
| **Varredura completa Bandit** | 973 LOC / 29 `B101` no artefato original; 1152 LOC / 34 `B101` como verificação complementar | **1152 LOC / 34 `B101`** em artefatos oficiais TXT e JSON |
| **pip-audit** | 5 pacotes congelados, sem `SQLAlchemy`; verificação complementar separada cobriu o banco | **7 pacotes congelados**, incluindo `SQLAlchemy==2.1.9` e `typing_extensions==4.16.0`; auditoria oficial cobre banco e testes |
| **Safety** | Não executado: `EOF when reading a line`, sem JSON | **Executado e autenticado**; 2 dependências testadas, 0 problemas, JSON arquivado |
| **Evidências adicionais** | Não havia JSON de Safety, JSON de produção Bandit nem registro de teste funcional | Adicionados `after_safety.json`, `after_safety_auth_status.txt`, `after_bandit_src.json`, `after_pip_audit_requirements.*` e `after_pytest.txt` |

### 2.1 Avaliação do banco de dados

A camada `project/src/infrastructure/database/` e os repositórios SQLite/SQLAlchemy passaram a fazer parte do escopo oficial da varredura de produção:

- `catalog_repository.py`, `offer_repository.py`, `sqlite_db.py` e os modelos SQLAlchemy foram analisados pelo Bandit sem alertas.
- A dependência `SQLAlchemy==2.1.9` foi instalada no venv isolado, congelada e auditada pelo pip-audit sem vulnerabilidades conhecidas.
- O Safety também detectou `SQLAlchemy==2.1.9` em `project/requirements.txt` e não encontrou problemas.
- A suíte `project/tests/test_sqlite_repositories.py` foi incluída na varredura completa, adicionando **46 LOC de teste** e **5 alertas `B101`**, todos ruído de `assert`.

### 2.2 Avaliação dos novos testes

A lacuna apontada na segunda avaliação — `project/tests` fora de escopo — foi fechada:

- **8 arquivos de teste**, **420 LOC**, incluindo `conftest.py`, `fakes/`, testes de domínio, ofertas legadas, combos, recibo e persistência.
- **34 alertas `B101`**, semanticamente idênticos ao ruído de 7 alertas da linha de base, porém proporcionais à suíte atual de 30 testes.
- Nenhum alerta de severidade `Medium` ou `High` foi encontrado em testes ou produção.

---

## 3. Metodologia e Ambiente

### 3.1 Identificação do ambiente

Registro completo em [`after_ambiente.txt`](security/after_ambiente.txt).

| Propriedade | Valor |
| :--- | :--- |
| **Data/Hora (UTC)** | 2026-11-25 22:29:43 UTC |
| **Sistema Operacional** | Linux 7.0.0-43-generic (#43~24.04.1-Ubuntu SMP x86_64) |
| **Shell** | `/bin/bash` |
| **Proxy HTTP/HTTPS** | nenhum |
| **Branch Git** | `feature/reavaliacao_3` |
| **Commit Git** | `8db0849895ba641eb07eeb6a6617211a3b7bdb45` |
| **Diretório Raiz dos Comandos** | `/home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata` |

### 3.2 Versões das ferramentas

| Ferramenta | Versão | Ambiente |
| :--- | :--- | :--- |
| **Conda** | 26.7.1 | `/home/beatriz/miniconda3/condabin/conda` |
| **Python** | 3.12.16 | `supermarket-sec` |
| **pip** | 26.2.2 | `supermarket-sec` |
| **Bandit** | 1.9.4 | `supermarket-sec` |
| **pip-audit** | 2.10.1 | venv temporário `/tmp/opencode/security-third-venv` |
| **Safety** | 3.8.1 | `supermarket-sec`, autenticado |

### 3.3 Preparação para pip-audit

Para isolar exatamente as dependências declaradas pelo produto, foi criado um venv temporário, instalados os requisitos e gerado o congelamento **antes** da instalação do próprio `pip-audit`:

```bash
python3 -m venv /tmp/opencode/security-third-venv
/tmp/opencode/security-third-venv/bin/python -m pip install -r project/requirements.txt
/tmp/opencode/security-third-venv/bin/python -m pip freeze \
  > docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_freeze.txt
/tmp/opencode/security-third-venv/bin/python -m pip install pip-audit==2.10.1
```

Pacotes congelados: `iniconfig==2.3.1`, `packaging==26.4`, `pluggy==1.7.0`, `Pygments==2.21.0`, `pytest==9.2.0`, `SQLAlchemy==2.1.9`, `typing_extensions==4.16.0`.

### 3.4 Autenticação do Safety

A CLI iniciou a rodada sem autenticação, conforme registrado em [`after_safety_tentativa.txt`](security/after_safety_tentativa.txt). O comando informado ao usuário foi:

```bash
conda run -n supermarket-sec python -m safety auth login
```

Após a autenticação, o status foi confirmado em [`after_safety_auth_status.txt`](security/after_safety_auth_status.txt):

```text
Authenticated as beatrizestevez29@gmail.com
```

---

## 4. Resultados Detalhados

### 4.1 Análise Estática de Código — Bandit

Comandos executados a partir da raiz do repositório:

```bash
conda run -n supermarket-sec python -m bandit -r project/src project/main.py \
  -f txt -o docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_src.txt
conda run -n supermarket-sec python -m bandit -r project/src project/main.py \
  -f json -o docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_src.json -q
conda run -n supermarket-sec python -m bandit -r project -x project/.approval_tests_temp \
  -f txt -o docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.txt
conda run -n supermarket-sec python -m bandit -r project -x project/.approval_tests_temp \
  -f json -o docs/security/terceira_avaliacao_refatorado_v2/security/after_bandit_all.json -q
```

#### 4.1.1 Produção

- **Código de saída:** `0`
- **Arquivos analisados:** 26 (`project/main.py` + 25 arquivos em `project/src/`)
- **LOC:** 732
- **`#nosec`:** 0
- **Severidade:** `High: 0`, `Medium: 0`, `Low: 0`, `Undefined: 0`
- **Confiança:** `High: 0`, `Medium: 0`, `Low: 0`, `Undefined: 0`
- **Evidências:** [`after_bandit_src.txt`](security/after_bandit_src.txt), [`after_bandit_src.json`](security/after_bandit_src.json)

> **Diagnóstico:** nenhuma fragilidade estática detectada, inclusive na nova camada de persistência e nos repositórios SQLite/SQLAlchemy.

#### 4.1.2 Projeto completo

- **Código de saída:** `1` — esperado, pois o Bandit retorna `1` quando encontra alertas `B101`.
- **LOC:** 1152 (732 produção + 420 testes)
- **Severidade:** `High: 0`, `Medium: 0`, `Low: 34`, `Undefined: 0`
- **Confiança:** `High: 34`, `Medium: 0`, `Low: 0`, `Undefined: 0`
- **Evidências:** [`after_bandit_all.txt`](security/after_bandit_all.txt), [`after_bandit_all.json`](security/after_bandit_all.json)

| Arquivo de Teste | LOC | Alertas `B101` | Classificação |
| :--- | ---: | ---: | :--- |
| `project/tests/test_combo_discount.py` | 139 | 13 | Falso positivo / ruído de `pytest` |
| `project/tests/test_domain_entities.py` | 40 | 5 | Falso positivo / ruído de `pytest` |
| `project/tests/test_legacy_offers.py` | 90 | 10 | Falso positivo / ruído de `pytest` |
| `project/tests/test_receipt_and_checkout.py` | 43 | 1 | Falso positivo / ruído de `pytest` |
| `project/tests/test_sqlite_repositories.py` | 46 | 5 | Falso positivo / ruído de `pytest` |
| `project/tests/conftest.py`, `fakes/` | 62 | 0 | Sem achados |

**Diagnóstico:** os 34 alertas são `B101:assert_used` (CWE-703), decorrentes do uso idiomático de `assert` em suítes `pytest`. Não há achados em `project/src` ou `project/main.py`.

### 4.2 Auditoria de Dependências — pip-audit

Comandos executados:

```bash
/tmp/opencode/security-third-venv/bin/python -m pip_audit \
  -r docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_freeze.txt \
  --no-deps -f json \
  -o docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.json
/tmp/opencode/security-third-venv/bin/python -m pip_audit \
  -r docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_freeze.txt \
  --no-deps 2>&1 | tee docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit.txt
/tmp/opencode/security-third-venv/bin/python -m pip_audit \
  -r project/requirements.txt --no-deps -f json \
  -o docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit_requirements.json
/tmp/opencode/security-third-venv/bin/python -m pip_audit \
  -r project/requirements.txt --no-deps 2>&1 | tee docs/security/terceira_avaliacao_refatorado_v2/security/after_pip_audit_requirements.txt
```

- **Código de saída:** `0` em todas as quatro execuções
- **Saída textual:** `No known vulnerabilities found`
- **Dependências listadas no JSON:** 6, todas com `vulns: []`
- **Correções sugeridas:** `0`
- **Evidências:** [`after_pip_audit.txt`](security/after_pip_audit.txt), [`after_pip_audit.json`](security/after_pip_audit.json), [`after_pip_audit_requirements.txt`](security/after_pip_audit_requirements.txt), [`after_pip_audit_requirements.json`](security/after_pip_audit_requirements.json)

| Pacote | Versão | Vulnerabilidades |
| :--- | :---: | :---: |
| `iniconfig` | 2.3.1 | 0 |
| `pluggy` | 1.7.0 | 0 |
| `pygments` | 2.21.0 | 0 |
| `pytest` | 9.2.0 | 0 |
| `sqlalchemy` | 2.1.9 | 0 |
| `typing-extensions` | 4.16.0 | 0 |

> **Observação:** o `after_pip_freeze.txt` registrou também `packaging==26.4`; o JSON estruturado do pip-audit relacionou as 6 dependências acima. Em nenhuma das saídas houve vulnerabilidade conhecida. O aviso padrão sobre `--no-deps` e o uso recomendado de hashes foi emitido, mas não representa achado de segurança.

### 4.3 Auditoria com Safety

Comandos executados:

```bash
conda run -n supermarket-sec python -m safety scan --target project \
  2>&1 | tee docs/security/terceira_avaliacao_refatorado_v2/security/after_safety.txt
conda run -n supermarket-sec python -m safety scan --target project --output json \
  > docs/security/terceira_avaliacao_refatorado_v2/security/after_safety.json
```

- **Código de saída:** `0`
- **Conta:** `beatrizestevez29@gmail.com`
- **Projeto:** `supermarketreceipt-refactoring-kata`
- **Branch:** `feature/reavaliacao_3`
- **Política:** buscada da Safety Platform (`source: cloud`)
- **Arquivo detectado:** `project/requirements.txt`
- **Dependências testadas:** 2
- **Resultado:** `0 security issues found, 0 fixes suggested`
- **Evidências:** [`after_safety.txt`](security/after_safety.txt), [`after_safety.json`](security/after_safety.json), [`after_safety_json_stderr.txt`](security/after_safety_json_stderr.txt)

| Dependência | Especificação | Problemas conhecidos |
| :--- | :--- | :---: |
| `sqlalchemy` | `SQLAlchemy==2.1.9` | 0 |
| `pytest` | `pytest==9.2.0` | 0 |

### 4.4 Sanidade funcional

```bash
cd project
/tmp/opencode/security-third-venv/bin/python -m pytest -q
```

- **Código de saída:** `0`
- **Resultado:** `30 passed in 0.37s`
- **Evidência:** [`after_pytest.txt`](security/after_pytest.txt)

---

## 5. Comparação entre as Avaliações

| Métrica / Dimensão | 1ª Avaliação (`python_pytest`) | 2ª Avaliação (`project/src`) | 3ª Avaliação (`project/` completo) | Variação / Impacto |
| :--- | :--- | :--- | :--- | :--- |
| **LOC em produção** | 133 (212 com testes) | 545 (22 arquivos) | **732** (26 arquivos, com banco) | Crescimento por camadas, persistência e `main.py`; **0 achados reais** |
| **LOC em testes** | 79 | Fora de escopo | **420** (8 arquivos) | Lacuna da 2ª avaliação fechada |
| **Achados Bandit em produção** | 0 | 0 | **0** | Nenhuma fragilidade estática no negócio ou acesso a dados |
| **Achados Bandit em testes** | 7 `B101` | Não avaliados | **34 `B101`** | Aumento proporcional à suíte; ruído de `pytest`, não vulnerabilidade |
| **Severidade High/Medium** | 0 / 0 | 0 / 0 | **0 / 0** | Nenhum achado explorável nas três avaliações |
| **Dependências externas em runtime** | Indiretas: `requests` e `urllib3==2.0.6` | Zero (somente stdlib no escopo avaliado) | **`SQLAlchemy==2.1.9`** + `pytest==9.2.0` (dev) | Banco adiciona 1 dependência de produção, fixada e sem CVEs |
| **Vulnerabilidades pip-audit no escopo do produto** | 16 no `urllib3` | 0 no escopo de `src` | **0** (6 dependências listadas) | Risco transitivo do legado eliminado |
| **Vulnerabilidades no ambiente da ferramenta** | `filelock` fora do escopo | 29 (`filelock` + `urllib3`) no ambiente | **0** no venv isolado de requisitos | Isolamento evitou contaminação por dependências do Safety |
| **Safety** | 1 alerta de requisito não pinado, ignorado por política | 0 problemas, **0 dependências testadas** (autenticado) | **0 problemas, 2 dependências testadas** (autenticado) | Maior cobertura: `requirements.txt` agora é lido e validado |
| **Autenticação Safety** | Concluída | Concluída após expiração | **Concluída nesta rodada** | Limitação da versão anterior resolvida |

### Comparativo direto 2ª → 3ª avaliação

- **Escopo:** de 545 LOC somente de produção para **1152 LOC** cobrindo produção, testes e ponto de entrada.
- **Banco de dados:** repositórios em memória evoluíram para SQLite/SQLAlchemy com acesso parametrizado via ORM; nenhuma concatenação dinâmica de SQL foi detectada.
- **Validação:** `catalog_repository.py` valida preço negativo antes da persistência, evitando dados financeiros inválidos.
- **Testes integrados:** `test_sqlite_repositories.py` cobre cadastro, leitura, ofertas/combos e checkout com banco.
- **Cadeia de suprimentos:** `approvaltests`/`urllib3==2.0.6` removidos; `SQLAlchemy==2.1.9` adicionado com versão fixada e 0 vulnerabilidades conhecidas.

---

## 6. Conclusão e Recomendações

A reexecução da terceira avaliação confirmou que o estado atual do branch `feature/reavaliacao_3` não apresenta vulnerabilidades identificadas pelas três ferramentas em seus escopos aplicáveis. A diferença mais relevante em relação à rodada anterior é a **inclusão oficial do banco de dados e dos novos testes**, além da **conclusão bem-sucedida do Safety com autenticação**.

Recomendações:

1. Manter versões fixadas em `project/requirements.txt`.
2. Gerar hashes com `pip-compile --generate-hashes` para eliminar o aviso sobre `--no-deps`.
3. Restringir permissões do arquivo `project/supermarket.db` e não versionar dados de produção.
4. Validar a origem de `db_url` caso a aplicação passe a aceitar configuração externa.
5. Opcionalmente, desabilitar `B101` apenas para `project/tests` na configuração do Bandit, sem alterar as regras de produção, caso se deseje uma esteira SAST com saída `0`.

---

## 7. Inventário de Evidências

| Arquivo | Conteúdo |
| :--- | :--- |
| [`after_ambiente.txt`](security/after_ambiente.txt) | Data/hora, SO, shell, proxy, branch, commit, versões das ferramentas |
| [`after_pip_freeze.txt`](security/after_pip_freeze.txt) | Pacotes congelados do venv isolado antes da instalação do pip-audit |
| [`after_pip_audit.txt`](security/after_pip_audit.txt) | Saída textual do pip-audit sobre o congelamento |
| [`after_pip_audit.json`](security/after_pip_audit.json) | JSON estruturado do pip-audit sobre o congelamento |
| [`after_pip_audit_requirements.txt`](security/after_pip_audit_requirements.txt) | Saída textual do pip-audit sobre `project/requirements.txt` |
| [`after_pip_audit_requirements.json`](security/after_pip_audit_requirements.json) | JSON estruturado do pip-audit sobre `project/requirements.txt` |
| [`after_bandit_src.txt`](security/after_bandit_src.txt) | Bandit em `project/src` + `project/main.py`: 732 LOC, 0 achados |
| [`after_bandit_src.json`](security/after_bandit_src.json) | Métricas estruturadas da varredura de produção |
| [`after_bandit_all.txt`](security/after_bandit_all.txt) | Bandit em `project/`: 1152 LOC, 34 `B101` |
| [`after_bandit_all.json`](security/after_bandit_all.json) | Métricas estruturadas e detalhamento dos 34 alertas |
| [`after_safety_tentativa.txt`](security/after_safety_tentativa.txt) | Registro da verificação inicial sem autenticação |
| [`after_safety_auth_status.txt`](security/after_safety_auth_status.txt) | Confirmação da autenticação do Safety |
| [`after_safety.txt`](security/after_safety.txt) | Saída textual do scan autenticado em `project/` |
| [`after_safety.json`](security/after_safety.json) | Relatório estruturado do Safety autenticado |
| [`after_safety_json_stderr.txt`](security/after_safety_json_stderr.txt) | Avisos de depreciação emitidos pela CLI do Safety |
| [`after_pytest.txt`](security/after_pytest.txt) | Sanidade funcional: 30 testes aprovados |
| [`relatorio_terceira_avaliacao_seguranca.md`](relatorio_terceira_avaliacao_seguranca.md) | Este relatório consolidado |
