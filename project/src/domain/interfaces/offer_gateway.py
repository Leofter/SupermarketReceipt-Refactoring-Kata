"""Contrato abstrato (Gateway) para consulta de ofertas ativas."""

from abc import ABC, abstractmethod

from src.domain.interfaces.discount_strategy import DiscountStrategy


class IOfferGateway(ABC):
    """Define o contrato de leitura das estratégias de desconto ativas."""

    @abstractmethod
    def list_active_offers(self) -> tuple[DiscountStrategy, ...]:
        """Retorna todas as estratégias de desconto ativas."""
