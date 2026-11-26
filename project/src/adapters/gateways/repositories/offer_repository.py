"""Repositório SQLite + SQLAlchemy de ofertas e combos."""

from sqlalchemy.orm import Session

from src.adapters.gateways.repositories.catalog_repository import (
    CatalogRepository,
)
from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.domain.entities.product import Product
from src.domain.interfaces.discount_strategy import DiscountStrategy
from src.domain.interfaces.offer_gateway import IOfferGateway
from src.infrastructure.database.model.offer_model import OfferModel


class OfferRepository(IOfferGateway):
    """Persiste e carrega ofertas unitárias e combos do SQLite."""

    def __init__(self, session: Session, catalog: CatalogRepository) -> None:
        self._session = session
        self._catalog = catalog

    def save_offer(
        self,
        offer_type: OfferType,
        products: tuple[Product, ...],
        argument: float = 0.0,
    ) -> None:
        """Salva uma oferta ou combo no banco."""
        offer = OfferModel(
            offer_type=offer_type.name,
            product_names=[product.name for product in products],
            argument=float(argument),
        )
        self._session.add(offer)
        self._session.commit()

    def list_active_offers(self) -> tuple[DiscountStrategy, ...]:
        """Lista as ofertas do banco e instancia suas estratégias."""
        rows = self._session.query(OfferModel).all()
        return tuple(
            DiscountStrategyFactory.create_strategy(
                OfferType[row.offer_type],
                tuple(self._get_product(name) for name in row.product_names),
                row.argument,
            )
            for row in rows
        )

    def _get_product(self, name: str) -> Product:
        product = self._catalog.find_by_name(name)
        if product is None:
            raise KeyError(name)
        return product
