"""Modelo ORM para a tabela de ofertas e combos."""

from sqlalchemy import JSON, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.model.base import Base


class OfferModel(Base):
    """Tabela de ofertas unitárias e combos promocionais."""

    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    offer_type: Mapped[str] = mapped_column(String, nullable=False)
    product_names: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    argument: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
