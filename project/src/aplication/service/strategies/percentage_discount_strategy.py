"""Estratégia de desconto percentual sobre um produto."""

from typing import Optional

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog
from src.domain.interfaces.discount_strategy import DiscountStrategy


class PercentageDiscountStrategy(DiscountStrategy):
    """Aplica desconto percentual sobre todas as unidades de um produto."""

    def __init__(self, product: Product, percentage: float) -> None:
        if percentage <= 0 or percentage > 100:
            raise ValueError("percentage deve estar entre 0 (exclusivo) e 100.")
        self._product = product
        self._percentage = float(percentage)

    def calculate_discount(
        self, cart: ShoppingCart, catalog: PriceCatalog
    ) -> Optional[Discount]:
        quantity = cart.product_quantities().get(self._product, 0.0)
        if quantity <= 0:
            return None

        unit_price = catalog.unit_price(self._product)
        discount_amount = quantity * unit_price * (self._percentage / 100.0)
        return Discount(
            products=(self._product,),
            description=f"{self._percentage}% off",
            amount=discount_amount,
        )
