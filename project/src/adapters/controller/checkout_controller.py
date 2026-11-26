"""Controlador responsável por orquestrar a entrada e saída do checkout."""

from src.adapters.presenter.receipt_presenter import ReceiptPresenter
from src.aplication.dto.input.checkout_input_dto import CheckoutInputDTO
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.shopping_cart import ShoppingCart


class CheckoutController:
    """Recebe o carrinho, executa o caso de uso e retorna o recibo formatado."""

    def __init__(
        self, use_case: CheckoutUseCase, presenter: ReceiptPresenter
    ) -> None:
        self._use_case = use_case
        self._presenter = presenter

    def checkout(self, cart: ShoppingCart) -> str:
        """Processa o checkout do carrinho e retorna o texto do recibo."""
        input_dto = CheckoutInputDTO(cart=cart)
        output_dto = self._use_case.execute(input_dto)
        return self._presenter.present(output_dto)
