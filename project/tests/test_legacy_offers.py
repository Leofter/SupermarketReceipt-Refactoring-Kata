"""Testes de regressão das ofertas legadas e da fábrica de estratégias."""

import pytest

from src.aplication.dto.input.checkout_input_dto import CheckoutInputDTO
from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart


def test_empty_cart_and_cart_without_offers(catalog, offer_gateway):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    use_case = CheckoutUseCase(catalog, offer_gateway)

    empty_out = use_case.execute(CheckoutInputDTO(ShoppingCart()))
    assert empty_out.total_price == 0.0
    assert empty_out.discounts == ()

    cart = ShoppingCart()
    cart.add_item(toothbrush)
    out = use_case.execute(CheckoutInputDTO(cart))
    assert out.total_discount == 0.0
    assert out.total_price == pytest.approx(0.99)


@pytest.mark.parametrize(
    "qty, expected_discount, expected_total",
    [
        (2, 0.0, 1.98),
        (3, 0.99, 1.98),
        (4, 0.99, 2.97),
    ],
)
def test_three_for_two_offer(
    catalog, offer_gateway, qty, expected_discount, expected_total
):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.THREE_FOR_TWO, (toothbrush,)
        )
    )

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, qty)
    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))

    assert out.total_discount == pytest.approx(expected_discount)
    assert out.total_price == pytest.approx(expected_total)


def test_ten_percent_discount_on_kilo_product(catalog, offer_gateway):
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.TEN_PERCENT_DISCOUNT, (apples,), 10.0
        )
    )

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)
    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))

    assert out.total_discount == pytest.approx(0.4975)
    assert out.total_price == pytest.approx(4.4775)


@pytest.mark.parametrize(
    "offer_type, bundle_price, qty, expected_discount, expected_total",
    [
        (OfferType.TWO_FOR_AMOUNT, 1.50, 1, 0.0, 0.99),
        (OfferType.TWO_FOR_AMOUNT, 1.50, 2, 0.48, 1.50),
        (OfferType.TWO_FOR_AMOUNT, 1.50, 3, 0.48, 2.49),
        (OfferType.FIVE_FOR_AMOUNT, 4.00, 4, 0.0, 3.96),
        (OfferType.FIVE_FOR_AMOUNT, 4.00, 5, 0.95, 4.00),
        (OfferType.FIVE_FOR_AMOUNT, 4.00, 6, 0.95, 4.99),
    ],
)
def test_bundle_for_amount_offers(
    catalog,
    offer_gateway,
    offer_type,
    bundle_price,
    qty,
    expected_discount,
    expected_total,
):
    rice = Product("rice", ProductUnit.EACH)
    catalog.add_product(rice, 0.99)
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            offer_type, (rice,), bundle_price
        )
    )

    cart = ShoppingCart()
    cart.add_item_quantity(rice, qty)
    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))

    assert out.total_discount == pytest.approx(expected_discount)
    assert out.total_price == pytest.approx(expected_total)
