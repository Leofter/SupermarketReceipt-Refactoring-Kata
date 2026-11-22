"""DTO de entrada para o caso de uso de checkout."""

from dataclasses import dataclass

from src.domain.entities.shopping_cart import ShoppingCart


@dataclass(frozen=True)
class CheckoutInputDTO:
    """Transporta o carrinho de compras selecionado para o checkout."""

    cart: ShoppingCart
