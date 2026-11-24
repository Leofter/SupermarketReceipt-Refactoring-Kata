"""Implementação em memória do gateway de ofertas ativas."""

from src.domain.interfaces.discount_strategy import DiscountStrategy
from src.domain.interfaces.offer_gateway import IOfferGateway


class MemoryOfferRepository(IOfferGateway):
    """Armazena as estratégias de desconto ativas em memória."""

    def __init__(self) -> None:
        self._offers: list[DiscountStrategy] = []

    def add_offer(self, strategy: DiscountStrategy) -> None:
        """Adiciona uma estratégia de desconto à lista de ofertas ativas."""
        self._offers.append(strategy)

    def list_active_offers(self) -> tuple[DiscountStrategy, ...]:
        """Retorna uma cópia imutável das estratégias de desconto ativas."""
        return tuple(self._offers)
