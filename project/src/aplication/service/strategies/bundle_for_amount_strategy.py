"""Estratégia de desconto para lotes com preço promocional fechado."""

from typing import Optional

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog
from src.domain.interfaces.discount_strategy import DiscountStrategy


class BundleForAmountStrategy(DiscountStrategy):
    """Aplica preço promocional fechado para lotes de N unidades (ex: 2 por X, 5 por X)."""

    def __init__(
        self, product: Product, bundle_size: int, bundle_price: float
    ) -> None:
        if bundle_size < 2:
            raise ValueError("bundle_size deve ser maior ou igual a 2.")
        if bundle_price < 0:
            raise ValueError("bundle_price não pode ser negativo.")
        self._product = product
        self._bundle_size = bundle_size
        self._bundle_price = float(bundle_price)

    def calculate_discount(
        self, cart: ShoppingCart, catalog: PriceCatalog
    ) -> Optional[Discount]:
        quantity = int(cart.product_quantities().get(self._product, 0))
        if quantity < self._bundle_size:
            return None

        unit_price = catalog.unit_price(self._product)
        bundles = quantity // self._bundle_size
        remainder = quantity % self._bundle_size
        promo_total = bundles * self._bundle_price + remainder * unit_price
        discount_amount = max(0.0, quantity * unit_price - promo_total)
        return Discount(
            products=(self._product,),
            description=f"{self._bundle_size} for {self._bundle_price}",
            amount=discount_amount,
        )

    def consumed_quantities(self, cart: ShoppingCart) -> dict[Product, float]:
        """Consome apenas os lotes completos de tamanho bundle_size."""
        quantity = int(cart.product_quantities().get(self._product, 0))
        consumed = (quantity // self._bundle_size) * self._bundle_size
        return {self._product: float(consumed)} if consumed > 0 else {}
