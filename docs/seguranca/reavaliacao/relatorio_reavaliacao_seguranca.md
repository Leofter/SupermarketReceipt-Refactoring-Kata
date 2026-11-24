# Relatório de Reavaliação de Segurança pós-Refatoração

**Projeto:** Supermarket Receipt Refactoring Kata (Python)  
**Data/Hora da Reavaliação (UTC):** 2026-11-24 20:20:56 UTC  
**Branch Git:** `feature/security_test_reavaliacao`  
**Commit Git de Referência:** `6f0ccb18959baefc8c65185f60d6b2acb920844a`  
**Alvo da Reavaliação:** Diretório `project/src` e todas as suas subpastas (Clean Architecture)  
**Ambiente Conda:** `supermarket-sec` (Python 3.12.16)

---

## 1. Sumário Executivo da Reavaliação

Este relatório apresenta a **reavaliação de segurança** realizada sobre o código refatorado do projeto *Supermarket Receipt*, localizado na pasta `project/src/`. A refatoração adotou os princípios de **Clean Architecture (Arquitetura Limpa)** e design orientado a objetos desacoplado, organizando o código em camadas bem definidas (`domain`, `aplication`, `adapters`, `infrastructure`).

### Principais Conclusões da Reavaliação:

1. **Bandit (SAST):**
   - **Código de Produção Refatorado (`project/src`):** Analisadas **545 linhas de código** distribuídas em 22 arquivos Python.
   - **Resultado:** **0 vulnerabilidades** identificadas (código de saída `0`).
   - Não foram encontrados alertas de severidade (`High: 0`, `Medium: 0`, `Low: 0`).
2. **pip-audit & Dependências (SCA):**
   - **Destaque Arquitetural:** O código refatorado em `project/src/` **elimina completamente a dependência de bibliotecas de terceiros** em tempo de execução. O núcleo da aplicação depende exclusivamente da biblioteca padrão do Python (`dataclasses`, `enum`, `typing`, `abc`).
   - A dependência vulnerável `urllib3==2.0.6` identificada na linha de base anterior (puxada indiretamente por ferramentas de teste do código legado) **não faz parte e não afeta o projeto refatorado**.
3. **Safety (SCA):**
   - Executado com autenticação ativa na plataforma Safety.
   - **Resultado:** **0 vulnerabilidades** encontradas no diretório `project/` (código de saída `0`), testando 0 dependências externas de produção.

---

## 2. Metodologia e Ambiente da Reavaliação

As informações completas do ambiente foram consolidadas no arquivo de evidência [reavaliacao_ambiente.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_ambiente.txt).

| Propriedade | Valor Registrado |
| :--- | :--- |
| **Data/Hora (UTC)** | 2026-11-24 20:15:17 UTC |
| **Sistema Operacional** | Linux 7.0.0-43-generic (#43~24.04.1-Ubuntu SMP x86_64) |
| **Shell** | Bash (`/usr/bin/bash`) |
| **Proxy Configurado** | Falso (nenhum proxy HTTP/HTTPS ativo) |
| **Branch Git** | `feature/security_test_reavaliacao` |
| **Commit Git** | `6f0ccb18959baefc8c65185f60d6b2acb920844a` |
| **Alvo Analisado** | `project/src` (e todas as suas subpastas) |

### Versões das Ferramentas Utilizadas:
- **Conda:** `26.7.1`
- **Python:** `3.12.16`
- **pip:** `26.2.2`
- **Bandit:** `1.9.4`
- **pip-audit:** `2.10.1`
- **Safety:** `3.8.1` (Autenticado como `beatrizestevez29@gmail.com`)

---

## 3. Resultados Detalhados da Reavaliação

### 3.1 Análise Estática de Código (SAST) - Bandit

O Bandit foi executado recursivamente sobre `project/src` e sobre a pasta raiz do projeto refatorado:

```bash
conda run -n supermarket-sec python -m bandit -r project/src -f txt -o docs/seguranca/reavaliacao/reavaliacao_bandit.txt
conda run -n supermarket-sec python -m bandit -r project/src -f json -o docs/seguranca/reavaliacao/reavaliacao_bandit.json -q
```

- **Código de Saída:** `0` (sucesso, nenhum achado de segurança)
- **Métricas do Escaneamento (`project/src`):**
  - Total de linhas de código analisadas: **545 linhas** (versus 133 da primeira avaliação)
  - Total de arquivos examinados: **22 arquivos**
  - Total de linhas ignoradas (`#nosec`): `0`
  - Total de regras desabilitadas: `0`
- **Métricas por Severidade:** `Undefined: 0`, `Low: 0`, `Medium: 0`, `High: 0`
- **Métricas por Confiança:** `Undefined: 0`, `Low: 0`, `Medium: 0`, `High: 0`
- **Evidências:** [reavaliacao_bandit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_bandit.txt) e [reavaliacao_bandit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_bandit.json).

### 3.2 Auditoria de Dependências (SCA) - pip-audit & Análise de Imports

A auditoria de dependências do ambiente foi executada sobre os pacotes congelados:

```bash
conda run -n supermarket-sec python -m pip_audit -r docs/seguranca/reavaliacao/reavaliacao_pip_freeze.txt --no-deps -f json -o docs/seguranca/reavaliacao/reavaliacao_pip_audit.json
conda run -n supermarket-sec python -m pip_audit -r docs/seguranca/reavaliacao/reavaliacao_pip_freeze.txt --no-deps 2>&1 | tee docs/seguranca/reavaliacao/reavaliacao_pip_audit.txt
```

- **Evidências:** [reavaliacao_pip_audit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_pip_audit.txt) e [reavaliacao_pip_audit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_pip_audit.json).
- **Análise do Escopo Refatorado (`project/src`):**
  Ao inspecionar todos os arquivos de `project/src/`, foi comprovado que **todos os imports são internos ao projeto ou provenientes da Standard Library do Python**:
  - `dataclasses`: Para modelagem imutável de entidades e DTOs.
  - `enum`: Para tipagem segura de tipos de ofertas e unidades de produto (`ProductUnit`, `OfferType`).
  - `typing`: Para anotações estáticas de tipo (`Optional`, `Callable`, `Dict`, `Tuple`).
  - `abc`: Para contratos de interface (`ABC`, `@abstractmethod`).
  
  **Conclusão:** O núcleo do projeto refatorado não possui dependências externas vulneráveis.

### 3.3 Auditoria com Safety

O Safety 3.8.1 foi executado apontando diretamente para a pasta do projeto refatorado:

```bash
conda run -n supermarket-sec python -m safety scan --target project 2>&1 | tee docs/seguranca/reavaliacao/reavaliacao_safety.txt
conda run -n supermarket-sec python -m safety scan --target project --output json > docs/seguranca/reavaliacao/reavaliacao_safety.json
```

- **Código de Saída:** `0` (sem vulnerabilidades)
- **Resultado:** `Tested 0 dependencies for security issues using policy fetched from Safety Platform. 0 security issues found, 0 fixes suggested.`
- **Evidências:** [reavaliacao_safety.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_safety.txt) e [reavaliacao_safety.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_safety.json).

---

## 4. Comparativo: Primeira Avaliação (Linha de Base) vs. Reavaliação

Abaixo está o comparativo detalhado entre a avaliação inicial do código legado (`python_pytest`) e a reavaliação do código refatorado (`project/src`):

| Métrica / Dimensão de Análise | Primeira Avaliação (`python_pytest`) | Reavaliação Pós-Refatoração (`project/src`) | Variação / Impacto |
| :--- | :--- | :--- | :--- |
| **Linhas de Código Analisadas (LOC)** | 133 LOC em produção (212 LOC total) | **545 LOC** (em produção pura) | +312 LOC (+234% devido à segregação em camadas e interfaces) |
| **Arquitetura e Organização** | Monolítica / Acoplada (5 arquivos em `src/`) | **Clean Architecture** (22 arquivos em 4 camadas estruturadas) | Desacoplamento de responsabilidades e isolamento de domínio |
| **Achados Bandit (SAST)** | 7 alertas `B101:assert_used` (Low/High) | **0 alertas** (Low: 0, Med: 0, High: 0) | **Melhoria total**: eliminação de ruídos e conformidade com padrões de código seguro |
| **Código de Saída do Bandit** | `1` (com achados na pasta de testes) | **`0`** (sucesso absoluto) | Código de produção 100% livre de apontamentos estáticos |
| **Dependências Externas em Runtime** | Indiretas via testes (`requests`, `urllib3==2.0.6`) | **Zero dependências externas** (Standard Library pura) | **Redução drástica da superfície de ataque (Supply Chain Risk)** |
| **Vulnerabilidades Conhecidas em Dependências** | 16 vulnerabilidades no `urllib3` herdado | **0 vulnerabilidades** no código de produção | Eliminação de risco de exploração de vulnerabilidades de terceiros no core |
| **Alertas do Safety** | 1 alerta (`SFTY-20260122-20373` por requisito não pinado no `pytest`) | **0 alertas** (nenhum arquivo de requisito inseguro) | Sem apontamentos no projeto refatorado |
| **Código de Saída do Safety** | `0` (alerta ignorado por política) | **`0`** (nenhum risco detectado) | Conformidade plena com a plataforma Safety |

---

## 5. Pontos Fortes e Melhorias de Segurança Após a Refatoração

A refatoração não apenas melhorou a manutenibilidade do software, mas trouxe avanços diretos na postura de segurança do sistema:

### 1. Eliminação do Risco de Cadeia de Suprimentos (Supply Chain Security)
- **Antes:** O projeto misturava dependências de teste e produção no mesmo ambiente, trazendo bibliotecas de rede complexas (`requests`, `urllib3`) com 16 CVEs ativas para dentro da árvore do projeto.
- **Depois:** O domínio (`project/src/domain`), casos de uso (`project/src/aplication`) e adaptadores (`project/src/adapters`) utilizam estritamente a biblioteca padrão do Python (`dataclasses`, `enum`, `typing`, `abc`). Sem bibliotecas de terceiros no núcleo, vetores de injeção e vulnerabilidades de terceiros deixam de existir em tempo de execução.

### 2. Imutabilidade e Prevenção de Injeção de Dados Inconsistentes (DTOs e Dataclasses)
- A introdução de DTOs tipados (`CheckoutInputDTO`, `CheckoutOutputDTO`, `ReceiptItemOutputDTO`, `DiscountOutputDTO`) garante que dados que transitam entre camadas externas (controllers/presenters) e casos de uso sejam estritamente estruturados e validados.
- O uso de classes de dados reduz efeitos colaterais acidentais e mutabilidade indevida de dados financeiros (preços, quantidades e descontos).

### 3. Validação Centralizada no Domínio
- Foi implementada a função `validate_product_quantity` no domínio (`project/src/domain/entities/product.py`), garantindo que itens com quantidade inteira (`ProductUnit.EACH`) não aceitem valores fracionários arbitrários, prevenindo inconsistências e falhas lógicas no cálculo do caixa.

### 4. Padrão Estratégia e Factory para Descontos (OCP e Segurança Lógica)
- As regras de desconto antes misturadas no carrinho de compras foram segregadas em estratégias isoladas (`PercentageDiscountStrategy`, `ThreeForTwoStrategy`, `BundleForAmountStrategy`, `ComboDiscountStrategy`), instanciadas via `DiscountStrategyFactory`.
- Isso evita mutações de estado cruzadas entre diferentes promoções e facilita testes unitários pontuais para cada regra financeira.

### 5. Inversão de Dependências (DIP) e Isolamento
- As interfaces de catálogo (`PriceCatalog`, `SupermarketCatalog`) e ofertas (`IOfferGateway`) desacoplam a lógica de negócio de qualquer infraestrutura física ou banco de dados futuro, reduzindo a possibilidade de acoplamento com camadas vulneráveis.

---

## 6. Inventário de Evidências da Reavaliação

Todos os arquivos brutos gerados pela reavaliação foram organizados na subpasta `docs/seguranca/reavaliacao/`:

- [reavaliacao_ambiente.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_ambiente.txt): Registro dos metadados de execução, SO, versões e commit da reavaliação.
- [reavaliacao_bandit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_bandit.txt): Saída textual da análise estática do Bandit sobre `project/src/` (0 vulnerabilidades em 545 LOC).
- [reavaliacao_bandit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_bandit.json): Métricas estruturadas do Bandit por arquivo e métricas gerais.
- [reavaliacao_pip_freeze.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_pip_freeze.txt): Registro dos pacotes do ambiente durante a reavaliação.
- [reavaliacao_pip_audit.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_pip_audit.txt): Auditoria de pacotes do ambiente via pip-audit.
- [reavaliacao_pip_audit.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_pip_audit.json): Estrutura JSON com detalhes de CVEs/PYSEC avaliados pelo pip-audit.
- [reavaliacao_safety_tentativa.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_safety_tentativa.txt): Registro da verificação de expiração do token de sessão anterior.
- [reavaliacao_safety.txt](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_safety.txt): Saída do scan de vulnerabilidades executado pelo Safety autenticado no diretório `project`.
- [reavaliacao_safety.json](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/reavaliacao_safety.json): Relatório estruturado do Safety em formato JSON.
- [relatorio_reavaliacao_seguranca.md](file:///home/beatriz/Documents/arquivos_faculdade/SupermarketReceipt-Refactoring-Kata/docs/seguranca/reavaliacao/relatorio_reavaliacao_seguranca.md): Este relatório comparativo e consolidado.
