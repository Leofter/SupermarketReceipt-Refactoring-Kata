"""Implementação em memória do gateway de catálogo de produtos."""

from src.domain.entities.product import Product
from src.domain.interfaces.catalog import SupermarketCatalog


class MemoryCatalogRepository(SupermarketCatalog):
    """Armazena produtos e preços unitários em memória."""

    def __init__(self) -> None:
        self._prices: dict[Product, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        """Registra ou atualiza o preço unitário de um produto."""
        self._prices[product] = float(price)

    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário do produto."""
        return self._prices[product]
