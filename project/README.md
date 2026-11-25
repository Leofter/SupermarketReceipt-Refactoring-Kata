# Supermarket Receipt — Versão Refatorada (`project/`)

Modernização incremental do sistema legado de supermercado (`python_pytest/`), preservando as regras comerciais existentes e adicionando a promoção de **combos completos (10% de desconto)**.

---

## 1. Ambiente e Dependências

- **Linguagem:** Python `3.9+` (validado em Python `3.13.13`).
- **Dependências de produção:** nenhuma (usa apenas a biblioteca padrão do Python).
- **Dependências de desenvolvimento/testes:**
  - `pytest` (execução dos testes automatizados)
  - `pytest-cov` (opcional, para relatório de cobertura)
  - `bandit`, `pip-audit` e `safety` (opcional, para auditorias de segurança)

Instalação opcional das ferramentas de teste em um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest pytest-cov
```

---

## 2. Como Executar

A partir da raiz do repositório ou dentro de `project/`:
```bash
cd project
python3 main.py
```

O `main.py` monta o catálogo, registra as ofertas (incluindo combos), processa um carrinho de exemplo e imprime o recibo formatado no terminal.

---

## 3. Como Rodar os Testes

Dentro da pasta `project/`:
```bash
cd project
pytest -v
```

Para rodar com cobertura de código:
```bash
pytest -v --cov=src --cov-report=term-missing
```

- **Resultado atual:** **`28 passed`** e **`95%` de cobertura global**.
- **O que os testes cobrem:**
  - Invariantes e cálculos das entidades (`Product`, `ProductQuantity`, `Discount`, `ShoppingCart`, `Receipt`).
  - Regressão das ofertas legadas (`3 for 2`, desconto percentual em `KILO`, `2 for amount` e `5 for amount`, carrinho vazio/sem ofertas).
  - Combos de 10% (combo completo, incompleto, repetido, produtos excedentes, múltiplos combos e convivência sem desconto duplicado com ofertas preexistentes).
  - Formatação do recibo de 40 colunas via `CheckoutController` e `ReceiptPresenter`.

---

## 4. Análises de Segurança

Foram executadas auditorias **antes** (sobre o legado) e **depois** (sobre `project/`):

| Ferramenta | Resultado no Projeto Refatorado | Observação |
| :--- | :--- | :--- |
| **Bandit `1.9.4`** | **0 alertas** em produção (`647` linhas) | Nos testes, apenas `B101` (`assert` do `pytest`), classificado como ruído esperado. |
| **pip-audit `2.10.1`** | **0 vulnerabilidades** (`5` pacotes auditados) | Eliminação das `16` CVEs transitivas de `urllib3` do legado ao remover `approvaltests`. |
| **Safety `3.8.1`** | Exigiu login interativo no ambiente (`EOF`) | Limitação registrada; dependências cobertas integralmente pelo `pip-audit`. |

Os relatórios e evidências completas estão em `docs/security/`.

---

## 5. Estrutura de Pastas

```text
project/
├── main.py                              # Ponto de entrada e montagem das dependências
├── pytest.ini                           # Configuração do pytest
├── src/
│   ├── domain/
│   │   ├── entities/                    # Product, ShoppingCart, Discount, Receipt
│   │   └── interfaces/                  # PriceCatalog, SupermarketCatalog, IOfferGateway, DiscountStrategy
│   ├── aplication/
│   │   ├── dto/                         # DTOs de entrada (input/) e saída (output/)
│   │   ├── service/
│   │   │   ├── discount_strategy_factory.py  # Factory Method (OfferType -> Strategy)
│   │   │   └── strategies/              # ThreeForTwo, Percentage, BundleForAmount, ComboDiscount
│   │   └── use_cases/                   # CheckoutUseCase (orquestração do checkout)
│   ├── adapters/
│   │   ├── controller/                  # CheckoutController
│   │   ├── presenter/                   # ReceiptPresenter (formatação em 40 colunas)
│   │   └── gateways/repositories/       # MemoryCatalogRepository, MemoryOfferRepository
│   └── infrastructure/
│       └── database/                    # Reservado para persistência futura (ex.: SQLite)
└── tests/
    ├── conftest.py                      # Fixtures compartilhadas
    ├── test_domain_entities.py          # Invariantes e entidades
    ├── test_legacy_offers.py            # Regressão das ofertas antigas
    ├── test_combo_discount.py           # Combos, bordas e convivência
    └── test_receipt_and_checkout.py     # Ponta a ponta (Controller -> Presenter)
```

---

## 6. Decisões Arquiteturais

- **Separação em Camadas (Clean Architecture + SOLID):** o núcleo (`domain/` e `aplication/`) não depende de memória, banco ou impressão; adaptadores externos implementam interfaces abstratas (`PriceCatalog`, `IOfferGateway`).
- **Segregação de Interfaces (ISP):** `PriceCatalog` (somente leitura) foi separado de `SupermarketCatalog` (leitura + cadastro).
- **Padrão Strategy (`DiscountStrategy`):** removeu o bloco `if/elif` de `ShoppingCart.handle_offers` e unificou `2 for amount` e `5 for amount` em `BundleForAmountStrategy` com divisão inteira `//`.
- **Padrão Factory Method (`DiscountStrategyFactory`):** centraliza a criação das estratégias a partir de `OfferType`.
- **Convivência entre Ofertas e Combos:** ofertas preexistentes são avaliadas antes de `ComboDiscountStrategy`, e cada estratégia informa quantas unidades consumiu (`consumed_quantities`), evitando desconto duplicado e liberando unidades excedentes.
- **Simplicidade (KISS):** entidades imutáveis essenciais, sem *over-engineering* de validadores extras ou arquivos de fachada desnecessários.
