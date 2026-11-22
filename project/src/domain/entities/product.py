"""Entidades e objetos relacionados a produtos do supermercado."""

from dataclasses import dataclass
from enum import Enum


class ProductUnit(Enum):
    """Unidade de medida utilizada para comercialização de um produto."""

    EACH = 1
    KILO = 2


@dataclass(frozen=True)
class Product:
    """Representa um produto comercializado no catálogo do supermercado."""

    name: str
    unit: ProductUnit

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("O nome do produto deve ser uma string não vazia.")
        if not isinstance(self.unit, ProductUnit):
            raise TypeError("A unidade do produto deve ser um ProductUnit válido.")


def validate_product_quantity(product: Product, quantity: float) -> None:
    """Valida se o produto e a quantidade respeitam as invariantes de domínio."""
    if not isinstance(product, Product):
        raise TypeError("product deve ser uma instância de Product.")
    if type(quantity) not in (int, float):
        raise TypeError("quantity deve ser um valor numérico.")
    if quantity <= 0:
        raise ValueError("quantity deve ser maior que zero.")
    if product.unit == ProductUnit.EACH and not float(quantity).is_integer():
        raise ValueError(
            "Produtos com unidade EACH não aceitam quantidade fracionária."
        )


@dataclass(frozen=True)
class ProductQuantity:
    """Objeto de valor imutável que associa um produto à sua quantidade."""

    product: Product
    quantity: float

    def __post_init__(self) -> None:
        validate_product_quantity(self.product, self.quantity)
