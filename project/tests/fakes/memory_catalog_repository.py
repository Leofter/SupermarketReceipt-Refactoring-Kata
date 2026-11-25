"""Implementação em memória do catálogo de produtos para testes."""

from typing import Optional

from src.domain.entities.product import Product
from src.domain.interfaces.catalog import SupermarketCatalog


class MemoryCatalogRepository(SupermarketCatalog):
    """Fake em memória que armazena produtos e preços unitários para testes."""

    def __init__(self) -> None:
        self._prices: dict[Product, float] = {}

    def add_product(self, product: Product, price: float) -> None:
        """Registra ou atualiza o preço unitário de um produto."""
        self._prices[product] = float(price)

    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário do produto."""
        return self._prices[product]

    def find_by_name(self, name: str) -> Optional[Product]:
        """Busca um produto cadastrado pelo nome."""
        for product in self._prices:
            if product.name == name:
                return product
        return None
