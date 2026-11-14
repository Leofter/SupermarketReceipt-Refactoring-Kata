import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


@pytest.fixture
def checkout_setup():
    catalog = FakeCatalog()
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    catalog.add_product(toothbrush, 10.0)
    catalog.add_product(toothpaste, 15.0)

    teller = Teller(catalog)
    teller.add_combo_offer({toothbrush: 1, toothpaste: 1})
    return teller, toothbrush, toothpaste


def checkout(teller, products):
    cart = ShoppingCart()
    for product in products:
        cart.add_item(product)
    return teller.checks_out_articles_from(cart)


def test_applies_ten_percent_discount_to_one_complete_combo(checkout_setup):
    teller, toothbrush, toothpaste = checkout_setup

    receipt = checkout(teller, [toothbrush, toothpaste])

    assert receipt.total_price() == pytest.approx(22.5)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].discount_amount == pytest.approx(-2.5)
    assert "10% off combo" in receipt.discounts[0].description


def test_does_not_apply_discount_to_incomplete_combo(checkout_setup):
    teller, toothbrush, _ = checkout_setup

    receipt = checkout(teller, [toothbrush])

    assert receipt.total_price() == pytest.approx(10.0)
    assert receipt.discounts == []


def test_discounts_only_complete_combo_when_there_is_an_excess_item(checkout_setup):
    teller, toothbrush, toothpaste = checkout_setup

    receipt = checkout(teller, [toothbrush, toothbrush, toothpaste])

    assert receipt.total_price() == pytest.approx(32.5)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].discount_amount == pytest.approx(-2.5)


def test_applies_discount_for_each_complete_combo(checkout_setup):
    teller, toothbrush, toothpaste = checkout_setup

    receipt = checkout(teller, [toothbrush, toothbrush, toothpaste, toothpaste])

    assert receipt.total_price() == pytest.approx(45.0)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].discount_amount == pytest.approx(-5.0)


def test_shows_combo_discount_on_receipt(checkout_setup):
    teller, toothbrush, toothpaste = checkout_setup

    receipt = checkout(teller, [toothbrush, toothpaste])

    printed_receipt = ReceiptPrinter().print_receipt(receipt)
    assert "10% off combo: toothbrush + toothpaste" in printed_receipt
    assert "-2.50" in printed_receipt
    assert "Total:                             22.50" in printed_receipt


def test_does_not_stack_combo_with_individual_offer(checkout_setup):
    teller, toothbrush, toothpaste = checkout_setup
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    receipt = checkout(teller, [toothbrush, toothpaste])

    assert receipt.total_price() == pytest.approx(24.0)
    assert len(receipt.discounts) == 1
    assert receipt.discounts[0].description == "10.0% off"
