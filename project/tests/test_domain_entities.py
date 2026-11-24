"""Testes das entidades e invariantes de domínio."""

import pytest

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product, ProductQuantity, ProductUnit
from src.domain.entities.receipt import Receipt
from src.domain.entities.shopping_cart import ShoppingCart


def test_product_rejects_empty_name():
    with pytest.raises(ValueError):
        Product("", ProductUnit.EACH)


def test_each_product_rejects_fractional_quantity():
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    with pytest.raises(ValueError):
        ProductQuantity(toothbrush, 1.5)


def test_kilo_product_accepts_fractional_quantity():
    apples = Product("apples", ProductUnit.KILO)
    pq = ProductQuantity(apples, 2.5)
    assert pq.quantity == 2.5


@pytest.mark.parametrize("invalid_qty", [0, -1])
def test_product_quantity_must_be_positive(invalid_qty):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    with pytest.raises(ValueError):
        ProductQuantity(toothbrush, invalid_qty)


def test_discount_rejects_negative_amount():
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    with pytest.raises(ValueError):
        Discount(products=(toothbrush,), description="invalid", amount=-1.0)


def test_shopping_cart_consolidates_product_quantities():
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    cart = ShoppingCart()
    cart.add_item(toothbrush)
    cart.add_item_quantity(toothbrush, 2)

    assert cart.product_quantities()[toothbrush] == 3.0


def test_receipt_calculates_subtotal_discount_and_total():
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    receipt = Receipt()
    receipt.add_product(toothbrush, 3, 1.00)
    receipt.add_discount(Discount((toothbrush,), "3 for 2", 1.00))

    assert receipt.subtotal() == pytest.approx(3.00)
    assert receipt.total_discount() == pytest.approx(1.00)
    assert receipt.total_price() == pytest.approx(2.00)
