"""Configuração da sessão SQLite com SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.infrastructure.database.model.base import Base
from src.infrastructure.database.model.offer_model import OfferModel
from src.infrastructure.database.model.product_model import ProductModel


def create_sqlite_session(db_url: str = "sqlite:///supermarket.db") -> Session:
    """Cria o engine SQLite, garante as tabelas e retorna uma sessão."""
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return Session(engine)
