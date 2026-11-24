"""Entidades relacionadas ao recibo fiscal e seus itens faturados."""

from dataclasses import dataclass

from src.domain.entities.discount import Discount
from src.domain.entities.product import Product, validate_product_quantity


@dataclass(frozen=True)
class ReceiptItem:
    """Objeto de valor imutável representando uma linha de item no recibo."""

    product: Product
    quantity: float
    unit_price: float

    def __post_init__(self) -> None:
        validate_product_quantity(self.product, self.quantity)
        if type(self.unit_price) not in (int, float):
            raise TypeError("unit_price deve ser um valor numérico.")
        if self.unit_price < 0:
            raise ValueError("unit_price não pode ser negativo.")

    @property
    def total_price(self) -> float:
        """Calcula o preço bruto da linha garantindo consistência matemática."""
        return self.quantity * self.unit_price


class Receipt:
    """Agregado que consolida os itens comprados e descontos concedidos."""

    def __init__(self) -> None:
        self._items: list[ReceiptItem] = []
        self._discounts: list[Discount] = []

    @property
    def items(self) -> tuple[ReceiptItem, ...]:
        """Retorna uma cópia imutável dos itens registrados no recibo."""
        return tuple(self._items)

    @property
    def discounts(self) -> tuple[Discount, ...]:
        """Retorna uma cópia imutável dos descontos aplicados no recibo."""
        return tuple(self._discounts)

    def add_product(
        self, product: Product, quantity: float, unit_price: float
    ) -> None:
        """Adiciona um item faturado ao recibo."""
        self._items.append(
            ReceiptItem(
                product=product, quantity=quantity, unit_price=unit_price
            )
        )

    def add_discount(self, discount: Discount) -> None:
        """Registra um desconto válido no recibo."""
        if not isinstance(discount, Discount):
            raise TypeError("discount deve ser uma instância de Discount.")
        self._discounts.append(discount)

    def subtotal(self) -> float:
        """Retorna a soma bruta dos itens antes dos descontos."""
        return sum(item.total_price for item in self._items)

    def total_discount(self) -> float:
        """Retorna a soma das magnitudes de todos os descontos."""
        return sum(discount.amount for discount in self._discounts)

    def total_price(self) -> float:
        """Calcula o valor final líquido a pagar (subtotal menos descontos)."""
        return self.subtotal() - self.total_discount()