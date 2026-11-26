# Supermarket Receipt — Versão Refatorada (`project/`)

Modernização incremental do sistema legado de supermercado (`python_pytest/`), preservando as regras comerciais existentes e adicionando a promoção de **combos completos (10% de desconto)**.

---

## 1. Ambiente e Dependências

- **Linguagem:** Python `3.9+` (validado em Python `3.13.13`).
- **Dependências de produção:** `SQLAlchemy==2.1.9` (persistência SQLite via `sqlite3` padrão).
- **Dependências de desenvolvimento/testes:**
  - `pytest==9.2.0` (execução dos testes automatizados)
  - `pytest-cov` (opcional, para relatório de cobertura)
  - `bandit`, `pip-audit` e `safety` (opcional, para auditorias de segurança)

Instalação das dependências em um ambiente virtual:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Como Executar

### Modo Terminal (`main.py`)
```bash
cd project
python3 main.py
```

O `main.py` inicializa o banco SQLite, cadastra produtos e todas as ofertas (incluindo combos), processa um carrinho de exemplo e imprime o recibo no terminal.

### Interface Gráfica Interativa (`gui.py`)
```bash
cd project
python3 gui.py
```

Abre o PDV interativo em Tkinter conectado ao mesmo banco SQLite e `CheckoutController`, permitindo adicionar itens, cadastrar novos produtos, testar cenários prontos e visualizar o cupom matricial em tempo real.

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

- **Resultado atual:** **`30 passed`** e **`95%` de cobertura global** (`434` instruções).
- **O que os testes cobrem:**
  - Invariantes e cálculos das entidades (`Product`, `ProductQuantity`, `Discount`, `ShoppingCart`, `Receipt`).
  - Regressão das ofertas legadas (`3 for 2`, desconto percentual em `KILO`, `2 for amount` e `5 for amount`, carrinho vazio/sem ofertas).
  - Combos de 10% (combo completo, incompleto, repetido, produtos excedentes, múltiplos combos e convivência sem desconto duplicado com ofertas preexistentes).
  - Formatação do recibo de 40 colunas via `CheckoutController` e `ReceiptPresenter`.
  - Persistência SQLite + SQLAlchemy (`CatalogRepository`, `OfferRepository`, validação de preço negativo e checkout integrado).

---

## 4. Análises de Segurança

Foram executadas auditorias **antes** (sobre o legado) e **depois** (sobre `project/`):

| Ferramenta | Resultado no Projeto Refatorado | Observação |
| :--- | :--- | :--- |
| **Bandit `1.9.4`** | **0 alertas** em produção (`732` linhas) | Nos testes, apenas `B101` (`assert` do `pytest`), classificado como ruído esperado. |
| **pip-audit `2.10.1`** | **0 vulnerabilidades** (`SQLAlchemy==2.1.9` e `pytest==9.2.0`) | Eliminação das `16` CVEs transitivas de `urllib3` do legado ao remover `approvaltests`. |
| **Safety `3.8.1`** | Exigiu login interativo no ambiente (`EOF`) | Limitação registrada; dependências cobertas integralmente pelo `pip-audit`. |

As evidências completas estão em `docs/security/terceira_avaliacao_refatorado_v2/`.

---

## 5. Estrutura de Pastas

```text
project/
├── main.py                              # Ponto de entrada CLI e montagem das dependências (SQLite)
├── gui.py                               # Interface gráfica interativa em Tkinter 
├── pytest.ini                           # Configuração do pytest
├── requirements.txt                     # Dependências fixadas (SQLAlchemy, pytest)
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
│   │   └── gateways/repositories/       # CatalogRepository, OfferRepository (SQLite + SQLAlchemy)
│   └── infrastructure/
│       └── database/
│           ├── sqlite_db.py             # Sessão e criação das tabelas SQLite
│           └── model/                   # Base, ProductModel, OfferModel
└── tests/
    ├── conftest.py                      # Fixtures compartilhadas
    ├── fakes/                           # MemoryCatalogRepository, MemoryOfferRepository
    ├── test_domain_entities.py          # Invariantes e entidades
    ├── test_legacy_offers.py            # Regressão das ofertas antigas
    ├── test_combo_discount.py           # Combos, bordas e convivência
    ├── test_receipt_and_checkout.py     # Ponta a ponta (Controller -> Presenter)
    └── test_sqlite_repositories.py      # Integração SQLite + SQLAlchemy
```

---

## 6. Decisões Arquiteturais

- **Separação em Camadas (Clean Architecture + SOLID):** o núcleo (`domain/` e `aplication/`) não depende de memória, banco ou impressão; adaptadores externos implementam interfaces abstratas (`PriceCatalog`, `IOfferGateway`).
- **Segregação de Interfaces (ISP):** `PriceCatalog` (somente leitura) foi separado de `SupermarketCatalog` (leitura + cadastro).
- **Padrão Strategy (`DiscountStrategy`):** removeu o bloco `if/elif` de `ShoppingCart.handle_offers` e unificou `2 for amount` e `5 for amount` em `BundleForAmountStrategy` com divisão inteira `//`.
- **Padrão Factory Method (`DiscountStrategyFactory`):** centraliza a criação das estratégias a partir de `OfferType`.
- **Convivência entre Ofertas e Combos:** ofertas preexistentes são avaliadas antes de `ComboDiscountStrategy`, e cada estratégia informa quantas unidades consumiu (`consumed_quantities`), evitando desconto duplicado e liberando unidades excedentes.
- **Simplicidade (KISS):** entidades imutáveis essenciais, sem *over-engineering* de validadores extras ou arquivos de fachada desnecessários.
