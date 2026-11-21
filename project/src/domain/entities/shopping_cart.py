"""Entidade de carrinho de compras."""

from src.domain.entities.product import Product, ProductQuantity


class ShoppingCart:
    """Gerencia os itens e quantidades selecionados pelo cliente.

    Mantém exclusivamente o estado do carrinho, sem acoplamento a regras de
    precificação, catálogo ou emissão de recibos.
    """

    def __init__(self) -> None:
        self._items: list[ProductQuantity] = []

    @property
    def items(self) -> tuple[ProductQuantity, ...]:
        """Retorna os registros de adição em ordem cronológica."""
        return tuple(self._items)

    def add_item(self, product: Product) -> None:
        """Adiciona uma unidade padrão (1.0) de um produto ao carrinho."""
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        """Adiciona uma quantidade específica de um produto ao carrinho."""
        self._items.append(ProductQuantity(product=product, quantity=quantity))

    def product_quantities(self) -> dict[Product, float]:
        """Retorna o consolidado de quantidades por produto."""
        totals: dict[Product, float] = {}
        for item in self._items:
            totals[item.product] = totals.get(item.product, 0.0) + item.quantity
        return totals
