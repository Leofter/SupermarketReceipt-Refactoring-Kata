"""Caso de uso responsável por orquestrar o checkout de compras."""

from src.aplication.dto.input.checkout_input_dto import CheckoutInputDTO
from src.aplication.dto.output.checkout_output_dto import CheckoutOutputDTO
from src.aplication.dto.output.discount_output_dto import DiscountOutputDTO
from src.aplication.dto.output.receipt_item_output_dto import (
    ReceiptItemOutputDTO,
)
from src.aplication.service.strategies.combo_discount_strategy import (
    ComboDiscountStrategy,
)
from src.domain.entities.product import Product
from src.domain.entities.receipt import Receipt
from src.domain.entities.shopping_cart import ShoppingCart
from src.domain.interfaces.catalog import PriceCatalog
from src.domain.interfaces.offer_gateway import IOfferGateway


class CheckoutUseCase:
    """Orquestra o fechamento da compra, aplicando ofertas e gerando saída."""

    def __init__(
        self, catalog: PriceCatalog, offer_gateway: IOfferGateway
    ) -> None:
        self._catalog = catalog
        self._offer_gateway = offer_gateway

    def execute(self, input_dto: CheckoutInputDTO) -> CheckoutOutputDTO:
        """Processa os itens do carrinho e retorna os dados do recibo."""
        receipt = Receipt()

        for item in input_dto.cart.items:
            unit_price = self._catalog.unit_price(item.product)
            receipt.add_product(item.product, item.quantity, unit_price)

        strategies = sorted(
            self._offer_gateway.list_active_offers(),
            key=lambda s: isinstance(s, ComboDiscountStrategy),
        )
        remaining = input_dto.cart.product_quantities()

        for strategy in strategies:
            remaining_cart = self._build_remaining_cart(remaining)
            discount = strategy.calculate_discount(
                remaining_cart, self._catalog
            )
            if discount is not None:
                receipt.add_discount(discount)
                for product, used in strategy.consumed_quantities(
                    remaining_cart
                ).items():
                    remaining[product] = max(
                        0.0, remaining.get(product, 0.0) - used
                    )

        return self._build_output(receipt)

    @staticmethod
    def _build_remaining_cart(
        remaining: dict[Product, float],
    ) -> ShoppingCart:
        """Monta um carrinho temporário apenas com itens ainda não consumidos."""
        cart = ShoppingCart()
        for product, qty in remaining.items():
            if qty > 0:
                cart.add_item_quantity(product, qty)
        return cart

    @staticmethod
    def _build_output(receipt: Receipt) -> CheckoutOutputDTO:
        """Converte a entidade Receipt no DTO de saída para apresentação."""
        items = tuple(
            ReceiptItemOutputDTO(
                product_name=item.product.name,
                unit=item.product.unit.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                total_price=item.total_price,
            )
            for item in receipt.items
        )
        discounts = tuple(
            DiscountOutputDTO(
                description=discount.description,
                product_names=tuple(p.name for p in discount.products),
                amount=discount.amount,
            )
            for discount in receipt.discounts
        )
        return CheckoutOutputDTO(
            items=items,
            discounts=discounts,
            subtotal=receipt.subtotal(),
            total_discount=receipt.total_discount(),
            total_price=receipt.total_price(),
        )
