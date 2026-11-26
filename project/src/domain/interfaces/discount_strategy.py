"""Contrato abstrato (Strategy) para cálculo de descontos e promoções."""

from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog


class DiscountStrategy(ABC):
    """Define a interface comum para políticas de desconto (padrão Strategy)."""

    @abstractmethod
    def calculate_discount(
        self, cart: ShoppingCart, catalog: PriceCatalog
    ) -> Optional[Discount]:
        """Calcula o desconto aplicável ao carrinho, ou None se não elegível."""

    def consumed_quantities(self, cart: ShoppingCart) -> dict[Product, float]:
        """Retorna as quantidades de produtos consumidas por esta oferta."""
        return {}
