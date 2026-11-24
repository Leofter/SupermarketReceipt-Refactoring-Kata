"""Ponto de entrada e composição das dependências do checkout."""

from src.adapters.controller.checkout_controller import CheckoutController
from src.adapters.gateways.repositories.memory_catalog_repository import (
    MemoryCatalogRepository,
)
from src.adapters.gateways.repositories.memory_offer_repository import (
    MemoryOfferRepository,
)
from src.adapters.presenter.receipt_presenter import ReceiptPresenter
from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart


def main() -> None:
    """Configura catálogo, ofertas, dependências e executa um checkout."""
    catalog = MemoryCatalogRepository()
    offer_gateway = MemoryOfferRepository()

    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    toothpaste = Product("toothpaste", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(toothpaste, 1.79)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.THREE_FOR_TWO,
            (toothbrush,),
        )
    )
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT,
            (toothbrush, toothpaste),
        )
    )

    use_case = CheckoutUseCase(catalog=catalog, offer_gateway=offer_gateway)
    presenter = ReceiptPresenter()
    controller = CheckoutController(use_case=use_case, presenter=presenter)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)
    cart.add_item_quantity(apples, 2.5)
    cart.add_item(toothpaste)

    print(controller.checkout(cart), end="")


if __name__ == "__main__":
    main()
