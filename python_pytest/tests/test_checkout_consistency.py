
import pytest

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from tests.fake_catalog import FakeCatalog


@pytest.fixture
def mixed_purchase():
    catalog = FakeCatalog()
    product_a = Product("A", ProductUnit.EACH)
    product_b = Product("B", ProductUnit.EACH)
    product_c = Product("C", ProductUnit.KILO)
    catalog.add_product(product_a, 10.00)
    catalog.add_product(product_b, 20.00)
    catalog.add_product(product_c, 4.00)
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, product_a, 0)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, product_b, 10.0)
    cart = ShoppingCart()
    cart.add_item_quantity(product_a, 3)
    cart.add_item_quantity(product_b, 2)
    cart.add_item_quantity(product_c, 2.5)
    return teller, cart, (product_a, product_b, product_c)


def receipt_content(receipt):
    """Captura dados publicos, sem depender de igualdade entre recibos."""
    return (
        [(item.product, item.quantity, item.price, item.total_price)
         for item in receipt.items],
        [(discount.product, discount.description, discount.discount_amount)
         for discount in receipt.discounts],
    )


def test_mixed_purchase_has_correct_lines_discounts_and_total(mixed_purchase):
    teller, cart, products = mixed_purchase
    product_a, product_b, product_c = products

    receipt = teller.checks_out_articles_from(cart)

    assert len(receipt.items) == 3
    expected_lines = [(product_a, 3, 10.00, 30.00),
                      (product_b, 2, 20.00, 40.00),
                      (product_c, 2.5, 4.00, 10.00)]
    for item, (product, quantity, price, subtotal) in zip(receipt.items, expected_lines):
        assert item.product is product
        assert (item.quantity, item.price, item.total_price) == pytest.approx(
            (quantity, price, subtotal), rel=0, abs=1e-9
        )
    assert len(receipt.discounts) == 2
    for product, description, amount in [
        (product_a, "3 for 2", -10.00),
        (product_b, "10.0% off", -4.00),
    ]:
        matches = [d for d in receipt.discounts if d.product is product]
        assert len(matches) == 1
        assert matches[0].description == description
        assert matches[0].discount_amount == pytest.approx(amount, rel=0, abs=1e-9)
    assert all(d.product is not product_c for d in receipt.discounts)
    assert receipt.total_price() == pytest.approx(66.00, rel=0, abs=1e-9)


def test_repeated_total_queries_preserve_receipt_content(mixed_purchase):
    teller, cart, _ = mixed_purchase
    receipt = teller.checks_out_articles_from(cart)
    before = receipt_content(receipt)

    for _ in range(3):
        assert receipt.total_price() == pytest.approx(66.00, rel=0, abs=1e-9)
        assert receipt_content(receipt) == before


def test_repeated_checkout_creates_distinct_equivalent_receipts(mixed_purchase):
    teller, cart, _ = mixed_purchase
    first = teller.checks_out_articles_from(cart)
    first_content = receipt_content(first)

    second = teller.checks_out_articles_from(cart)

    assert second is not first
    assert receipt_content(first) == first_content
    assert receipt_content(second) == first_content
    for receipt in (first, second):
        assert len(receipt.items) == 3
        assert len(receipt.discounts) == 2
        assert sorted(d.discount_amount for d in receipt.discounts) == pytest.approx(
            [-10.00, -4.00], rel=0, abs=1e-9
        )
        assert receipt.total_price() == pytest.approx(66.00, rel=0, abs=1e-9)


def test_checkout_preserves_cart_items_and_accumulated_quantities(mixed_purchase):
    teller, cart, products = mixed_purchase
    before_items = [(item.product, item.quantity) for item in cart.items]
    before_quantities = dict(cart.product_quantities)
    assert before_items == list(zip(products, [3, 2, 2.5]))

    teller.checks_out_articles_from(cart)

    assert [(item.product, item.quantity) for item in cart.items] == before_items
    assert cart.product_quantities == before_quantities
