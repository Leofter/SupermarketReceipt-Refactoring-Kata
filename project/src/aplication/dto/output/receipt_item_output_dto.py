"""DTO de saída para uma linha de item faturado no recibo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ReceiptItemOutputDTO:
    """Dados de uma linha de item faturado para apresentação."""

    product_name: str
    unit: str
    quantity: float
    unit_price: float
    total_price: float
