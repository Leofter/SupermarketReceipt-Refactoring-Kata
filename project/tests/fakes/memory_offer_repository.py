"""Implementação em memória do gateway de ofertas para testes."""

from src.aplication.service.discount_strategy_factory import (
    DiscountStrategyFactory,
    OfferType,
)
from src.domain.entities.product import Product
from src.domain.interfaces.discount_strategy import DiscountStrategy
from src.domain.interfaces.offer_gateway import IOfferGateway


class MemoryOfferRepository(IOfferGateway):
    """Fake em memória que armazena estratégias de desconto para testes."""

    def __init__(self) -> None:
        self._offers: list[DiscountStrategy] = []

    def add_offer(self, strategy: DiscountStrategy) -> None:
        """Adiciona uma estratégia de desconto à lista de ofertas ativas."""
        self._offers.append(strategy)

    def save_offer(
        self,
        offer_type: OfferType,
        products: tuple[Product, ...],
        argument: float = 0.0,
    ) -> None:
        """Cria e registra uma oferta a partir dos dados básicos."""
        self._offers.append(
            DiscountStrategyFactory.create_strategy(
                offer_type, products, argument
            )
        )

    def list_active_offers(self) -> tuple[DiscountStrategy, ...]:
        """Retorna uma cópia imutável das estratégias de desconto ativas."""
        return tuple(self._offers)
