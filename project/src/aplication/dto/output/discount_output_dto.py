"""DTO de saída para um desconto aplicado no recibo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DiscountOutputDTO:
    """Dados de um desconto aplicado (unitário ou combo) para apresentação."""

    description: str
    product_names: tuple[str, ...]
    amount: float
