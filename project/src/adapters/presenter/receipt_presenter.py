"""Apresentador responsável por formatar o recibo de checkout."""

from src.aplication.dto.output.checkout_output_dto import CheckoutOutputDTO


class ReceiptPresenter:
    """Formata o CheckoutOutputDTO em texto no padrão do recibo."""

    def __init__(self, columns: int = 40) -> None:
        self._columns = columns

    def present(self, output: CheckoutOutputDTO) -> str:
        """Gera a representação textual completa do recibo."""
        lines: list[str] = []

        for item in output.items:
            lines.append(
                self._format_line(item.product_name, f"{item.total_price:.2f}")
            )
            if item.quantity != 1:
                qty = (
                    int(item.quantity)
                    if item.unit == "EACH"
                    else f"{item.quantity:.3f}"
                )
                lines.append(f"  {item.unit_price:.2f} * {qty}\n")

        for discount in output.discounts:
            products = ", ".join(discount.product_names)
            name = f"{discount.description} ({products})"
            value = f"-{discount.amount:.2f}" if discount.amount > 0 else "0.00"
            lines.append(self._format_line(name, value))

        lines.append("\n")
        lines.append(self._format_line("Total: ", f"{output.total_price:.2f}"))
        return "".join(lines)

    def _format_line(self, name: str, value: str) -> str:
        spaces = " " * max(0, self._columns - len(name) - len(value))
        return f"{name}{spaces}{value}\n"
