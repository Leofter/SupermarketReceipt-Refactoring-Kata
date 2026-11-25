"""Testes de integração dos repositórios SQLite + SQLAlchemy."""

import pytest

from src.adapters.gateways.repositories.catalog_repository import (
    CatalogRepository,
)
from src.adapters.gateways.repositories.offer_repository import (
    OfferRepository,
)
from src.aplication.dto.input.checkout_input_dto import CheckoutInputDTO
from src.aplication.service.discount_strategy_factory import OfferType
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart
from src.infrastructure.database.sqlite_db import create_sqlite_session


@pytest.fixture
def sqlite_repos():
    session = create_sqlite_session("sqlite:///:memory:")
    catalog = CatalogRepository(session)
    offer_gateway = OfferRepository(session, catalog)
    yield catalog, offer_gateway
    session.close()


def test_sqlite_catalog_persists_and_finds_products(sqlite_repos):
    catalog, _ = sqlite_repos
    escova = Product("escova", ProductUnit.EACH)
    catalog.add_product(escova, 10.00)
    catalog.add_product(escova, 12.50)

    assert catalog.unit_price(escova) == pytest.approx(12.50)
    assert catalog.find_by_name("escova") == escova
    assert catalog.find_by_name("inexistente") is None

    with pytest.raises(KeyError):
        catalog.unit_price(Product("inexistente", ProductUnit.EACH))


def test_sqlite_offer_repository_and_checkout_with_combo(sqlite_repos):
    catalog, offer_gateway = sqlite_repos
    escova = Product("escova", ProductUnit.EACH)
    pasta = Product("creme dental", ProductUnit.EACH)
    catalog.add_product(escova, 10.00)
    catalog.add_product(pasta, 15.00)

    offer_gateway.save_offer(OfferType.COMBO_TEN_PERCENT, (escova, pasta))

    cart = ShoppingCart()
    cart.add_item_quantity(escova, 2)
    cart.add_item(pasta)

    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))
    assert out.total_discount == pytest.approx(2.50)
    assert out.total_price == pytest.approx(32.50)
