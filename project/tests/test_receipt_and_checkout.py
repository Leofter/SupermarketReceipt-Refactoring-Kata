"""Testes de formatação do recibo e fluxo completo via CheckoutController."""

from src.adapters.controller.checkout_controller import CheckoutController
from src.adapters.presenter.receipt_presenter import ReceiptPresenter
from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart


def test_controller_formats_receipt_with_legacy_and_combo_rules(
    catalog, offer_gateway
):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(toothpaste, 1.79)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (toothbrush, toothpaste)
        )
    )

    controller = CheckoutController(
        use_case=CheckoutUseCase(catalog, offer_gateway),
        presenter=ReceiptPresenter(),
    )

    cart = ShoppingCart()
    cart.add_item(toothbrush)
    cart.add_item_quantity(apples, 2.5)
    cart.add_item(toothpaste)

    receipt_text = controller.checkout(cart)

    expected = (
        "toothbrush                          0.99\n"
        "apples                              4.97\n"
        "  1.99 * 2.500\n"
        "toothpaste                          1.79\n"
        "Combo 10.0% off (toothbrush, toothpaste)-0.28\n"
        "\n"
        "Total:                              7.48\n"
    )
    assert receipt_text == expected
