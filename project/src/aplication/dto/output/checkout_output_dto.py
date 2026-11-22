"""DTO de saída consolidado para o caso de uso de checkout."""

from dataclasses import dataclass

from src.aplication.dto.output.discount_output_dto import DiscountOutputDTO
from src.aplication.dto.output.receipt_item_output_dto import (
    ReceiptItemOutputDTO,
)


@dataclass(frozen=True)
class CheckoutOutputDTO:
    """Resultado consolidado do checkout pronto para o apresentador."""

    items: tuple[ReceiptItemOutputDTO, ...]
    discounts: tuple[DiscountOutputDTO, ...]
    subtotal: float
    total_discount: float
    total_price: float
