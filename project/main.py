"""Ponto de entrada e composição das dependências do checkout."""

from pathlib import Path

from src.adapters.controller.checkout_controller import CheckoutController
from src.adapters.gateways.repositories.catalog_repository import (
    CatalogRepository,
)
from src.adapters.gateways.repositories.offer_repository import (
    OfferRepository,
)
from src.adapters.presenter.receipt_presenter import ReceiptPresenter
from src.aplication.service.discount_strategy_factory import OfferType
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart
from src.infrastructure.database.sqlite_db import create_sqlite_session


def main() -> None:
    """Configura banco SQLite, catálogo, ofertas e executa um checkout."""
    db_path = Path(__file__).resolve().parent / "supermarket.db"
    session = create_sqlite_session(f"sqlite:///{db_path}")

    catalog = CatalogRepository(session)
    offer_gateway = OfferRepository(session, catalog)

    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    rice = Product("rice", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(toothpaste, 1.79)
    catalog.add_product(tomatoes, 0.69)
    catalog.add_product(rice, 2.49)

    if not offer_gateway.list_active_offers():
        offer_gateway.save_offer(OfferType.THREE_FOR_TWO, (toothbrush,))
        offer_gateway.save_offer(OfferType.TEN_PERCENT_DISCOUNT, (apples,))
        offer_gateway.save_offer(OfferType.TWO_FOR_AMOUNT, (tomatoes,), 0.99)
        offer_gateway.save_offer(OfferType.FIVE_FOR_AMOUNT, (rice,), 7.49)
        offer_gateway.save_offer(OfferType.COMBO_TEN_PERCENT, (toothbrush, toothpaste))

    use_case = CheckoutUseCase(catalog=catalog, offer_gateway=offer_gateway)
    presenter = ReceiptPresenter()
    controller = CheckoutController(use_case=use_case, presenter=presenter)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 4)
    cart.add_item_quantity(apples, 2.5)
    cart.add_item(toothpaste)
    cart.add_item_quantity(tomatoes, 2)
    cart.add_item_quantity(rice, 5)

    print(controller.checkout(cart), end="")
    session.close()


if __name__ == "__main__":
    main()
