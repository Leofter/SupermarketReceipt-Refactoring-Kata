"""Modelo ORM para a tabela de produtos."""

from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.model.base import Base


class ProductModel(Base):
    """Tabela de produtos e preços unitários."""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String, primary_key=True)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    unit_price: Mapped[float] = mapped_column(Float, nullable=False)
