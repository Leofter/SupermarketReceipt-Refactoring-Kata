"""Contratos abstratos para consulta e manutenção do catálogo de produtos."""

from abc import ABC, abstractmethod

from src.domain.entities.product import Product


class PriceCatalog(ABC):
    """Contrato somente leitura para consulta de preços unitários."""

    @abstractmethod
    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário de um produto cadastrado no catálogo."""


class SupermarketCatalog(PriceCatalog, ABC):
    """Contrato completo de catálogo com suporte a cadastro de produtos."""

    @abstractmethod
    def add_product(self, product: Product, price: float) -> None:
        """Registra ou atualiza um produto e seu preço unitário."""
