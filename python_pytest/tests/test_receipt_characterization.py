"""Testes do prompt 5: Receipt e caracterizacao do comportamento legado.

Os testes com prefixo test_legacy documentam decisoes atuais, nao requisitos
obrigatorios para uma futura versao. Nao pressupomos copias profundas.
"""

import pytest

from model_objects import Discount, Product, ProductUnit, SpecialOfferType
from receipt import Receipt, ReceiptItem
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


def test_receipt_empty_total_is_zero():
    assert Receipt().total_price() == 0


def test_receipt_add_product_preserves_line_data():
    product = Product("apples", ProductUnit.KILO)
    receipt = Receipt()

    receipt.add_product(product, 2.5, 4.00, 10.00)

    assert len(receipt.items) == 1
    item = receipt.items[0]
    assert item.product is product
    assert item.quantity == pytest.approx(2.5, rel=0, abs=1e-9)
    assert item.price == pytest.approx(4.00, rel=0, abs=1e-9)
    assert item.total_price == pytest.approx(10.00, rel=0, abs=1e-9)


def test_receipt_total_includes_all_subtotals_and_negative_discounts():
    product_a = Product("A", ProductUnit.EACH)
    product_b = Product("B", ProductUnit.EACH)
    receipt = Receipt()
    receipt.add_product(product_a, 3, 10.00, 30.00)
    receipt.add_product(product_b, 2, 20.00, 40.00)
    receipt.add_discount(Discount(product_a, "3 for 2", -10.00))
    receipt.add_discount(Discount(product_b, "10% off", -4.00))

    assert receipt.total_price() == pytest.approx(56.00, rel=0, abs=1e-9)


@pytest.mark.parametrize("operation", ["append", "pop"])
def test_receipt_items_list_changes_do_not_modify_internal_collection(operation):
    product = Product("A", ProductUnit.EACH)
    receipt = Receipt()
    receipt.add_product(product, 1, 10.00, 10.00)
    original = receipt.items[0]
    returned_items = receipt.items

    if operation == "append":
        returned_items.append(ReceiptItem(product, 2, 10.00, 20.00))
        assert len(returned_items) == 2
    else:
        assert returned_items.pop() is original
        assert returned_items == []

    assert len(receipt.items) == 1
    assert receipt.items[0] is original
    assert receipt.total_price() == pytest.approx(10.00, rel=0, abs=1e-9)


@pytest.mark.parametrize("operation", ["append", "pop"])
def test_receipt_discounts_list_changes_do_not_modify_internal_collection(operation):
    product = Product("A", ProductUnit.EACH)
    receipt = Receipt()
    receipt.add_product(product, 1, 10.00, 10.00)
    original = Discount(product, "10% off", -1.00)
    receipt.add_discount(original)
    returned_discounts = receipt.discounts

    if operation == "append":
        returned_discounts.append(Discount(product, "extra", -2.00))
        assert len(returned_discounts) == 2
    else:
        assert returned_discounts.pop() is original
        assert returned_discounts == []

    assert len(receipt.discounts) == 1
    assert receipt.discounts[0] is original
    assert receipt.total_price() == pytest.approx(9.00, rel=0, abs=1e-9)


def test_legacy_second_offer_for_same_product_replaces_first():
    product = Product("A", ProductUnit.EACH)
    catalog = FakeCatalog()
    catalog.add_product(product, 10.00)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, product, 0)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product, 20.0)
    cart = ShoppingCart()
    cart.add_item_quantity(product, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(24.00, rel=0, abs=1e-9)
    assert len(receipt.discounts) == 1
    discount = receipt.discounts[0]
    assert discount.product is product
    assert discount.description == "20.0% off"
    assert discount.discount_amount == pytest.approx(-6.00, rel=0, abs=1e-9)


def test_legacy_product_with_name_returns_registered_product():
    product = Product("apples", ProductUnit.KILO)
    catalog = FakeCatalog()
    catalog.add_product(product, 4.00)

    assert Teller(catalog).product_with_name("apples") is product


def test_legacy_product_with_name_returns_none_for_unknown_name():
    catalog = FakeCatalog()
    catalog.add_product(Product("apples", ProductUnit.KILO), 4.00)

    assert Teller(catalog).product_with_name("unknown") is None


def test_legacy_same_name_products_have_separate_cart_quantities():
    first = Product("toothbrush", ProductUnit.EACH)
    second = Product("toothbrush", ProductUnit.EACH)
    cart = ShoppingCart()

    cart.add_item_quantity(first, 2)
    cart.add_item_quantity(second, 3)

    assert len(cart.product_quantities) == 2
    assert cart.product_quantities[first] == 2
    assert cart.product_quantities[second] == 3
    assert len(cart.items) == 2
    assert cart.items[0].product is first
    assert cart.items[1].product is second


def test_legacy_offer_uses_product_identity_while_catalog_uses_name():
    first = Product("toothbrush", ProductUnit.EACH)
    second = Product("toothbrush", ProductUnit.EACH)
    catalog = FakeCatalog()
    catalog.add_product(first, 10.00)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, first, 10.0)
    cart = ShoppingCart()
    cart.add_item(first)
    cart.add_item(second)

    receipt = teller.checks_out_articles_from(cart)

    assert catalog.unit_price(second) == pytest.approx(10.00, rel=0, abs=1e-9)
    assert len(receipt.items) == 2
    assert receipt.items[0].product is first
    assert receipt.items[1].product is second
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].product is first
    assert receipt.discounts[0].discount_amount == pytest.approx(-1.00, rel=0, abs=1e-9)
    assert receipt.total_price() == pytest.approx(19.00, rel=0, abs=1e-9)
