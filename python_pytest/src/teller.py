from combo_offer import ComboOffer
from model_objects import Offer
from receipt import Receipt


class Teller:

    def __init__(self, catalog):
        self.catalog = catalog
        self.offers = {}
        self.combo_offers = []

    def add_special_offer(self, offer_type, product, argument):
        self.offers[product] = Offer(offer_type, product, argument)

    def add_combo_offer(self, required_products, discount_percentage=10.0, description=None):
        """Register a group promotion without changing the legacy offer API."""
        self.combo_offers.append(
            ComboOffer(required_products, discount_percentage, description)
        )

    def checks_out_articles_from(self, the_cart):
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)
        self._apply_combo_offers(receipt, the_cart.product_quantities)

        return receipt

    def _apply_combo_offers(self, receipt, product_quantities):
        for combo_offer in self.combo_offers:
            if combo_offer.uses_product_with_individual_offer(self.offers):
                continue
            discount = combo_offer.calculate_discount(product_quantities, self.catalog)
            if discount:
                receipt.add_discount(discount)

    def product_with_name(self, name):
        return self.catalog.products.get(name, None)
