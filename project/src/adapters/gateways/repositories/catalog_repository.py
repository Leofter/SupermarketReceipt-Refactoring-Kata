"""Repositório SQLite + SQLAlchemy do catálogo de produtos."""

from typing import Optional

from sqlalchemy.orm import Session

from src.domain.entities.product import Product, ProductUnit
from src.domain.interfaces.catalog import SupermarketCatalog
from src.infrastructure.database.model.product_model import ProductModel


class CatalogRepository(SupermarketCatalog):
    """Persiste produtos e preços unitários no SQLite."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def add_product(self, product: Product, price: float) -> None:
        """Insere ou atualiza um produto e seu preço unitário."""
        if price < 0:
            raise ValueError("price não pode ser negativo.")
        model = ProductModel(
            name=product.name,
            unit=product.unit.name,
            unit_price=float(price),
        )
        self._session.merge(model)
        self._session.commit()

    def unit_price(self, product: Product) -> float:
        """Retorna o preço unitário do produto."""
        row = self._session.get(ProductModel, product.name)
        if row is None:
            raise KeyError(product)
        return row.unit_price

    def find_by_name(self, name: str) -> Optional[Product]:
        """Busca um produto cadastrado pelo nome."""
        row = self._session.get(ProductModel, name)
        if row is None:
            return None
        return Product(row.name, ProductUnit[row.unit])

    def list_products(self) -> tuple[tuple[Product, float], ...]:
        """Retorna todos os produtos cadastrados e seus preços."""
        rows = self._session.query(ProductModel).all()
        return tuple(
            (Product(row.name, ProductUnit[row.unit]), row.unit_price)
            for row in rows
        )
