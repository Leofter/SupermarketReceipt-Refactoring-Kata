"""Promotion rule for a fixed group of products bought together."""

import math

from model_objects import Discount, Product, ProductUnit


class ComboOffer:
    """Applies a percentage discount to each complete group in a cart."""

    def __init__(self, required_products, discount_percentage=10.0, description=None):
        if not required_products:
            raise ValueError("A combo must contain at least one product")
        if any(quantity <= 0 for quantity in required_products.values()):
            raise ValueError("The required quantity of each combo product must be positive")

        self.required_products = dict(required_products)
        self.discount_percentage = discount_percentage
        self.description = description or self._default_description()
        self._receipt_product = Product(self.description, ProductUnit.EACH)

    def calculate_discount(self, product_quantities, catalog):
        complete_combos = self._number_of_complete_combos(product_quantities)
        if complete_combos == 0:
            return None

        combo_subtotal = sum(
            catalog.unit_price(product) * quantity
            for product, quantity in self.required_products.items()
        )
        discount_amount = combo_subtotal * complete_combos * self.discount_percentage / 100.0
        return Discount(self._receipt_product, self.description, -discount_amount)

    def uses_product_with_individual_offer(self, individual_offers):
        """Prevent two promotions from discounting the same combo items."""
        return any(product in individual_offers for product in self.required_products)

    def _number_of_complete_combos(self, product_quantities):
        quantities_available = (
            math.floor(product_quantities.get(product, 0) / required_quantity)
            for product, required_quantity in self.required_products.items()
        )
        return min(quantities_available)

    def _default_description(self):
        product_names = " + ".join(product.name for product in self.required_products)
        return f"{self.discount_percentage:g}% off combo: {product_names}"
