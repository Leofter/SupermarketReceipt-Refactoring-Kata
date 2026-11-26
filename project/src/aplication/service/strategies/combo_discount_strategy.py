"""Estratégia de desconto para combos completos de produtos."""

from typing import Optional

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog
from src.domain.interfaces.discount_strategy import DiscountStrategy


class ComboDiscountStrategy(DiscountStrategy):
    """Aplica desconto percentual (padrão 10%) apenas a combos completos."""

    def __init__(
        self, products: tuple[Product, ...], percentage: float = 10.0
    ) -> None:
        if len(products) < 2:
            raise ValueError("Combo deve possuir pelo menos 2 produtos.")
        if len(set(products)) != len(products):
            raise ValueError("Produtos do combo não devem ser duplicados.")
        if percentage <= 0 or percentage > 100:
            raise ValueError("percentage deve estar entre 0 (exclusivo) e 100.")
        self._products = products
        self._percentage = float(percentage)

    def calculate_discount(
        self, cart: ShoppingCart, catalog: PriceCatalog
    ) -> Optional[Discount]:
        quantities = cart.product_quantities()
        complete_combos = min(
            int(quantities.get(product, 0)) for product in self._products
        )
        if complete_combos < 1:
            return None

        combo_base_price = sum(
            catalog.unit_price(product) for product in self._products
        )
        discount_amount = (
            complete_combos * combo_base_price * (self._percentage / 100.0)
        )
        return Discount(
            products=self._products,
            description=f"Combo {self._percentage}% off",
            amount=discount_amount,
        )

    def consumed_quantities(self, cart: ShoppingCart) -> dict[Product, float]:
        """Consome 1 unidade de cada produto para cada combo completo."""
        quantities = cart.product_quantities()
        complete_combos = min(
            int(quantities.get(product, 0)) for product in self._products
        )
        if complete_combos < 1:
            return {}
        return {product: float(complete_combos) for product in self._products}
