"""Prompt 6: formatacao textual e recibos de referencia revisados."""

import pytest
from approvaltests import verify
from approvaltests.reporters import PythonNativeReporter

from model_objects import Discount, Product, ProductUnit, SpecialOfferType
from receipt import Receipt, ReceiptItem
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog
from tests.receipt_printer import ReceiptPrinter


def test_empty_receipt_prints_zero_total():
    actual = ReceiptPrinter().print_receipt(Receipt())
    assert actual == "\nTotal:                              0.00\n"


def test_single_unit_has_no_multiplication_line():
    item = ReceiptItem(Product("A", ProductUnit.EACH), 1, 10.00, 10.00)
    assert ReceiptPrinter().print_receipt_item(item) == (
        "A                                  10.00\n"
    )


def test_multiple_units_include_unit_price_and_quantity():
    item = ReceiptItem(Product("A", ProductUnit.EACH), 3, 10.00, 30.00)
    assert ReceiptPrinter().print_receipt_item(item) == (
        "A                                  30.00\n"
        "  10.00 * 3\n"
    )


def test_weight_has_three_decimal_places():
    item = ReceiptItem(Product("C", ProductUnit.KILO), 2.5, 4.00, 10.00)
    assert ReceiptPrinter().print_receipt_item(item) == (
        "C                                  10.00\n"
        "  4.00 * 2.500\n"
    )


@pytest.mark.parametrize("value, expected", [
    (0, "0.00"), (10, "10.00"), (1.2, "1.20"), (-4, "-4.00"),
])
def test_price_has_two_decimal_places(value, expected):
    assert ReceiptPrinter().print_price(value) == expected


def test_discount_prints_description_product_and_negative_amount():
    discount = Discount(Product("B", ProductUnit.EACH), "10.0% off", -4.00)
    assert ReceiptPrinter().print_discount(discount) == (
        "10.0% off (B)                      -4.00\n"
    )


def test_total_has_two_decimal_places():
    receipt = Receipt()
    receipt.add_product(Product("A", ProductUnit.EACH), 1, 10.00, 10.00)
    assert ReceiptPrinter().present_total(receipt) == (
        "Total:                             10.00\n"
    )


@pytest.mark.parametrize("columns, expected", [
    (40, "A                                  10.00\n"),
    (24, "A                  10.00\n"),
])
def test_line_alignment_respects_column_width(columns, expected):
    actual = ReceiptPrinter(columns).format_line_with_whitespace("A", "10.00")
    assert actual == expected
    assert len(actual.rstrip("\n")) == columns


def test_empty_receipt_approval():
    verify(ReceiptPrinter().print_receipt(Receipt()), reporter=PythonNativeReporter())


def test_mixed_receipt_approval():
    # Referencia: 10 + 40 + 10 - 4 = 56. Sem TWO_FOR_AMOUNT.
    catalog = FakeCatalog()
    product_a = Product("A", ProductUnit.EACH)
    product_b = Product("B", ProductUnit.EACH)
    product_c = Product("C", ProductUnit.KILO)
    catalog.add_product(product_a, 10.00)
    catalog.add_product(product_b, 20.00)
    catalog.add_product(product_c, 4.00)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product_b, 10.0)
    cart = ShoppingCart()
    cart.add_item_quantity(product_a, 1)
    cart.add_item_quantity(product_b, 2)
    cart.add_item_quantity(product_c, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    verify(ReceiptPrinter().print_receipt(receipt), reporter=PythonNativeReporter())
