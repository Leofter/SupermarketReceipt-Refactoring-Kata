"""Objeto para descontos aplicados no recibo."""

from dataclasses import dataclass

from src.domain.entities.product import Product


@dataclass(frozen=True)
class Discount:
    """Representa um desconto aplicado a um ou mais produtos no recibo.

    O atributo ``amount`` representa sempre a magnitude positiva do desconto
    a ser subtraída do subtotal da compra.
    """

    products: tuple[Product, ...]
    description: str
    amount: float

    def __post_init__(self) -> None:
        if not self.products or not isinstance(self.products, tuple):
            raise ValueError(
                "products deve ser uma tupla não vazia de Product."
            )
        if not all(isinstance(p, Product) for p in self.products):
            raise TypeError(
                "Todos os itens de products devem ser instâncias de Product."
            )
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("description deve ser uma string não vazia.")
        if isinstance(self.amount, bool) or not isinstance(
            self.amount, (int, float)
        ):
            raise TypeError("amount deve ser um valor numérico.")
        if self.amount < 0:
            raise ValueError("amount do desconto não pode ser negativo.")

    @classmethod
    def for_product(
        cls, product: Product, description: str, amount: float
    ) -> "Discount":
        """Cria um desconto associado a um único produto."""
        return cls(products=(product,), description=description, amount=amount)

    @property
    def primary_product(self) -> Product:
        """Retorna o primeiro produto associado ao desconto."""
        return self.products[0]
