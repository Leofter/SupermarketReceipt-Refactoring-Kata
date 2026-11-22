"""Estratégia de desconto 'leve 3, pague 2'."""

from typing import Optional

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog
from src.domain.interfaces.discount_strategy import DiscountStrategy


class ThreeForTwoStrategy(DiscountStrategy):
    """Aplica promoção 'leve 3, pague 2' para um produto específico."""

    def __init__(self, product: Product) -> None:
        self._product = product

    def calculate_discount(
        self, cart: ShoppingCart, catalog: PriceCatalog
    ) -> Optional[Discount]:
        quantity = int(cart.product_quantities().get(self._product, 0))
        if quantity < 3:
            return None

        unit_price = catalog.unit_price(self._product)
        free_items = quantity // 3
        discount_amount = free_items * unit_price
        return Discount(
            products=(self._product,),
            description="3 for 2",
            amount=discount_amount,
        )
