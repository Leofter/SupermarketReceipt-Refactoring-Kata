"""Contrato abstrato (Gateway) para gerenciamento de ofertas ativas."""

from abc import ABC, abstractmethod

from src.domain.interfaces.discount_strategy import DiscountStrategy


class IOfferGateway(ABC):
    """Define o contrato para registro e consulta de estratégias de desconto."""

    @abstractmethod
    def add_offer(self, strategy: DiscountStrategy) -> None:
        """Registra uma estratégia de desconto ativa."""

    @abstractmethod
    def list_active_offers(self) -> tuple[DiscountStrategy, ...]:
        """Retorna todas as estratégias de desconto ativas."""
