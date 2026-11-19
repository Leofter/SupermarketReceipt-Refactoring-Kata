import pytest

from model_objects import Product, SpecialOfferType, ProductUnit
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


@pytest.fixture
def catalog():
    return FakeCatalog()


@pytest.fixture
def cart():
    return ShoppingCart()


@pytest.fixture
def teller(catalog):
    return Teller(catalog)


def test_checkout_empty_cart(teller, cart):
    receipt = teller.checks_out_articles_from(cart)

    assert cart.items == []
    assert cart.product_quantities == {}
    assert receipt.items == []
    assert receipt.discounts == []
    assert receipt.total_price() == 0


def test_checkout_single_unit(catalog, teller, cart):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)

    assert cart.product_quantities == {toothbrush: 1}
    assert receipt.discounts == []
    assert receipt.total_price() == pytest.approx(0.99)
    assert len(receipt.items) == 1
    item = receipt.items[0]
    assert item.product is toothbrush
    assert item.quantity == 1
    assert item.price == pytest.approx(0.99)
    assert item.total_price == pytest.approx(0.99)


def test_checkout_multiple_units_in_one_addition(catalog, teller, cart):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)

    assert cart.product_quantities == {toothbrush: 3}
    assert receipt.discounts == []
    assert receipt.total_price() == pytest.approx(2.97)
    assert len(receipt.items) == 1
    item = receipt.items[0]
    assert item.product is toothbrush
    assert item.quantity == 3
    assert item.price == pytest.approx(0.99)
    assert item.total_price == pytest.approx(2.97)


def test_checkout_different_products_sums_subtotals(catalog, teller, cart):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(toothpaste, 1.79)
    cart.add_item_quantity(toothbrush, 2)
    cart.add_item(toothpaste)

    receipt = teller.checks_out_articles_from(cart)

    assert cart.product_quantities == {toothbrush: 2, toothpaste: 1}
    assert receipt.discounts == []
    assert len(receipt.items) == 2
    toothbrush_item, toothpaste_item = receipt.items
    assert toothbrush_item.product is toothbrush
    assert toothbrush_item.quantity == 2
    assert toothbrush_item.price == pytest.approx(0.99)
    assert toothbrush_item.total_price == pytest.approx(1.98)
    assert toothpaste_item.product is toothpaste
    assert toothpaste_item.quantity == 1
    assert toothpaste_item.price == pytest.approx(1.79)
    assert toothpaste_item.total_price == pytest.approx(1.79)
    assert receipt.total_price() == pytest.approx(3.77)
    assert receipt.total_price() == pytest.approx(
        sum(item.total_price for item in receipt.items)
    )


def test_checkout_product_sold_by_weight(catalog, teller, cart):
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 4.00)
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert cart.product_quantities == {apples: 2.5}
    assert receipt.discounts == []
    assert receipt.total_price() == pytest.approx(10.00)
    assert len(receipt.items) == 1
    item = receipt.items[0]
    assert item.product is apples
    assert item.quantity == 2.5
    assert item.price == pytest.approx(4.00)
    assert item.total_price == pytest.approx(10.00)


def test_separate_additions_preserve_receipt_lines_and_accumulate_quantity(
    catalog, teller, cart
):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    cart.add_item(toothbrush)
    cart.add_item_quantity(toothbrush, 2)

    receipt = teller.checks_out_articles_from(cart)

    assert cart.product_quantities == {toothbrush: 3}
    assert len(cart.items) == 2
    first_cart_item, second_cart_item = cart.items
    assert first_cart_item.product is toothbrush
    assert first_cart_item.quantity == 1
    assert second_cart_item.product is toothbrush
    assert second_cart_item.quantity == 2
    assert receipt.discounts == []
    assert receipt.total_price() == pytest.approx(2.97)
    assert len(receipt.items) == 2
    first_item, second_item = receipt.items
    assert first_item.product is toothbrush
    assert first_item.quantity == 1
    assert first_item.price == pytest.approx(0.99)
    assert first_item.total_price == pytest.approx(0.99)
    assert second_item.product is toothbrush
    assert second_item.quantity == 2
    assert second_item.price == pytest.approx(0.99)
    assert second_item.total_price == pytest.approx(1.98)


def test_offer_for_absent_product_does_not_apply_discount(catalog, teller, cart):
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)

    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == pytest.approx(4.975)
    assert receipt.discounts == []
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product is apples
    assert receipt_item.price == pytest.approx(1.99)
    assert receipt_item.total_price == pytest.approx(4.975)
    assert receipt_item.quantity == 2.5
