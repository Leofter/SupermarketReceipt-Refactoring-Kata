"""Testes da regra de combos promocionais, bordas e convivência."""

import pytest

from src.aplication.dto.input.checkout_input_dto import CheckoutInputDTO
from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.aplication.service.strategies.combo_discount_strategy import (
    ComboDiscountStrategy,
)
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart


@pytest.mark.parametrize(
    "escova_qty, pasta_qty, expected_discount, expected_total",
    [
        (1, 1, 2.50, 22.50),  # 1 combo completo
        (2, 1, 2.50, 32.50),  # 1 combo + 1 escova excedente integral
        (2, 2, 5.00, 45.00),  # 2 combos completos
        (1, 0, 0.00, 10.00),  # combo incompleto
    ],
)
def test_combo_discount_scenarios(
    catalog,
    offer_gateway,
    escova_qty,
    pasta_qty,
    expected_discount,
    expected_total,
):
    escova = Product("escova", ProductUnit.EACH)
    pasta = Product("creme dental", ProductUnit.EACH)
    catalog.add_product(escova, 10.00)
    catalog.add_product(pasta, 15.00)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (escova, pasta)
        )
    )

    cart = ShoppingCart()
    if escova_qty > 0:
        cart.add_item_quantity(escova, escova_qty)
    if pasta_qty > 0:
        cart.add_item_quantity(pasta, pasta_qty)

    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))

    assert out.total_discount == pytest.approx(expected_discount)
    assert out.total_price == pytest.approx(expected_total)


def test_combo_rejects_single_or_duplicated_products():
    escova = Product("escova", ProductUnit.EACH)
    with pytest.raises(ValueError):
        ComboDiscountStrategy((escova,))
    with pytest.raises(ValueError):
        ComboDiscountStrategy((escova, escova))


def test_multiple_combos_do_not_double_discount_same_item(
    catalog, offer_gateway
):
    escova = Product("escova", ProductUnit.EACH)
    pasta = Product("creme dental", ProductUnit.EACH)
    fio = Product("fio dental", ProductUnit.EACH)
    catalog.add_product(escova, 10.00)
    catalog.add_product(pasta, 15.00)
    catalog.add_product(fio, 5.00)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (escova, pasta)
        )
    )
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (escova, fio)
        )
    )

    cart = ShoppingCart()
    cart.add_item(escova)
    cart.add_item(pasta)
    cart.add_item(fio)

    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))

    assert len(out.discounts) == 1
    assert out.total_discount == pytest.approx(2.50)
    assert out.total_price == pytest.approx(27.50)


def test_combo_coexists_with_three_for_two_without_duplicate_discount(
    catalog, offer_gateway
):
    escova = Product("escova", ProductUnit.EACH)
    pasta = Product("creme dental", ProductUnit.EACH)
    catalog.add_product(escova, 10.00)
    catalog.add_product(pasta, 15.00)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (escova, pasta)
        )
    )
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.THREE_FOR_TWO, (escova,)
        )
    )

    cart_no_surplus = ShoppingCart()
    cart_no_surplus.add_item_quantity(escova, 3)
    cart_no_surplus.add_item(pasta)
    out_no_surplus = CheckoutUseCase(catalog, offer_gateway).execute(
        CheckoutInputDTO(cart_no_surplus)
    )
    assert len(out_no_surplus.discounts) == 1
    assert out_no_surplus.total_discount == pytest.approx(10.00)

    cart_with_surplus = ShoppingCart()
    cart_with_surplus.add_item_quantity(escova, 4)
    cart_with_surplus.add_item(pasta)
    out_with_surplus = CheckoutUseCase(catalog, offer_gateway).execute(
        CheckoutInputDTO(cart_with_surplus)
    )
    assert len(out_with_surplus.discounts) == 2
    assert out_with_surplus.total_discount == pytest.approx(12.50)
    assert out_with_surplus.total_price == pytest.approx(42.50)


def test_combo_coexists_with_offer_on_different_product(catalog, offer_gateway):
    escova = Product("escova", ProductUnit.EACH)
    pasta = Product("creme dental", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(escova, 10.00)
    catalog.add_product(pasta, 15.00)
    catalog.add_product(apples, 2.00)

    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.TEN_PERCENT_DISCOUNT, (apples,), 10.0
        )
    )
    offer_gateway.add_offer(
        DiscountStrategyFactory.create_strategy(
            OfferType.COMBO_TEN_PERCENT, (escova, pasta)
        )
    )

    cart = ShoppingCart()
    cart.add_item(escova)
    cart.add_item(pasta)
    cart.add_item_quantity(apples, 2.5)

    out = CheckoutUseCase(catalog, offer_gateway).execute(CheckoutInputDTO(cart))
    assert len(out.discounts) == 2
    assert out.total_discount == pytest.approx(3.00)
    assert out.total_price == pytest.approx(27.00)
