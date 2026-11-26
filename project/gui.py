"""Interface gráfica e-commerce em Tkinter no estilo visual da apresentação."""

from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from src.adapters.controller.checkout_controller import CheckoutController
from src.adapters.gateways.repositories.catalog_repository import (
    CatalogRepository,
)
from src.adapters.gateways.repositories.offer_repository import (
    OfferRepository,
)
from src.adapters.presenter.receipt_presenter import ReceiptPresenter
from src.aplication.service.discount_strategy_factory import OfferType
from src.aplication.use_cases.checkout_use_case import CheckoutUseCase
from src.domain.entities.product import Product, ProductUnit
from src.domain.entities.shopping_cart import ShoppingCart
from src.infrastructure.database.sqlite_db import create_sqlite_session

BG = "#0d1117"
PANEL = "#161b22"
PANEL2 = "#1c2330"
LINE = "#2b3445"
TX = "#e6edf3"
MUT = "#9aa7b8"
RED = "#e4002b"
BLUE = "#2f81f7"
GREEN = "#3fb950"
CODE = "#1e1e1e"


def _seed_defaults(
    catalog: CatalogRepository, offer_gateway: OfferRepository
) -> None:
    """Garante produtos e ofertas iniciais no banco SQLite."""
    if catalog.list_products():
        return

    toothbrush = Product("toothbrush", ProductUnit.EACH)
    apples = Product("apples", ProductUnit.KILO)
    toothpaste = Product("toothpaste", ProductUnit.EACH)
    tomatoes = Product("cherry tomatoes", ProductUnit.EACH)
    rice = Product("rice", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(apples, 1.99)
    catalog.add_product(toothpaste, 1.79)
    catalog.add_product(tomatoes, 0.69)
    catalog.add_product(rice, 2.49)

    if not offer_gateway.list_active_offers():
        offer_gateway.save_offer(OfferType.THREE_FOR_TWO, (toothbrush,))
        offer_gateway.save_offer(OfferType.TEN_PERCENT_DISCOUNT, (apples,))
        offer_gateway.save_offer(OfferType.TWO_FOR_AMOUNT, (tomatoes,), 0.99)
        offer_gateway.save_offer(OfferType.FIVE_FOR_AMOUNT, (rice,), 7.49)
        offer_gateway.save_offer(
            OfferType.COMBO_TEN_PERCENT, (toothbrush, toothpaste)
        )


class SupermarketGUI:
    """Aplicação e-commerce Tkinter conectada ao CheckoutController e SQLite."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CIMATEC Market — E-commerce & Checkout")
        self.root.geometry("1200x720")
        self.root.configure(bg=BG)

        db_path = Path(__file__).resolve().parent / "supermarket.db"
        self.session = create_sqlite_session(f"sqlite:///{db_path}")
        self.catalog = CatalogRepository(self.session)
        self.offer_gateway = OfferRepository(self.session, self.catalog)
        _seed_defaults(self.catalog, self.offer_gateway)

        use_case = CheckoutUseCase(
            catalog=self.catalog, offer_gateway=self.offer_gateway
        )
        self.controller = CheckoutController(
            use_case=use_case, presenter=ReceiptPresenter()
        )
        self.cart = ShoppingCart()

        self._setup_styles()
        self._build_ui()
        self._refresh_vitrine()
        self._refresh_cart_and_receipt()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dark.TCombobox",
            fieldbackground=PANEL2,
            background=PANEL2,
            foreground=TX,
            selectbackground=BLUE,
            selectforeground="#ffffff",
        )
        for name, bg, fg, active in [
            ("Primary.TButton", BLUE, "#ffffff", "#1f6feb"),
            ("Success.TButton", GREEN, "#0d1117", "#2ea043"),
            ("Danger.TButton", RED, "#ffffff", "#c90025"),
            ("Ghost.TButton", PANEL2, TX, "#263042"),
        ]:
            style.configure(
                name,
                background=bg,
                foreground=fg,
                borderwidth=0,
                padding=(10, 6),
                font=("Segoe UI", 9, "bold"),
            )
            style.map(
                name,
                background=[("active", active), ("pressed", active)],
                foreground=[("active", fg)],
            )

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=PANEL, height=60)
        header.pack(fill="x", padx=18, pady=(14, 10))

        left_h = tk.Frame(header, bg=PANEL)
        left_h.pack(side="left", padx=14, pady=10)
        tk.Label(
            left_h,
            text=" SENAI CIMATEC ",
            bg=RED,
            fg="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=3,
        ).pack(side="left")
        tk.Label(
            left_h,
            text="  CIMATEC Market",
            bg=PANEL,
            fg=TX,
            font=("Segoe UI", 15, "bold"),
        ).pack(side="left")

        self.bag_badge = tk.Label(
            header,
            text="Sacola: 0 itens  |  Total: R$ 0.00",
            bg=PANEL2,
            fg=GREEN,
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=5,
        )
        self.bag_badge.pack(side="right", padx=14, pady=10)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        body.columnconfigure(0, weight=5)
        body.columnconfigure(1, weight=3)
        body.columnconfigure(2, weight=4)
        body.rowconfigure(0, weight=1)

        self._build_vitrine_panel(body)
        self._build_cart_panel(body)
        self._build_receipt_panel(body)

    def _card(self, parent: tk.Widget, title: str, col: int) -> tk.Frame:
        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightbackground=LINE,
            highlightthickness=1,
            padx=14,
            pady=12,
        )
        frame.grid(row=0, column=col, sticky="nsew", padx=6)
        tk.Label(
            frame,
            text=title,
            bg=PANEL,
            fg=TX,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", pady=(0, 10))
        return frame

    def _build_vitrine_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "Vitrine de Produtos", 0)

        qty_bar = tk.Frame(card, bg=PANEL2, padx=10, pady=8)
        qty_bar.pack(fill="x", pady=(0, 10))
        tk.Label(
            qty_bar,
            text="Quantidade ao adicionar:",
            bg=PANEL2,
            fg=MUT,
            font=("Segoe UI", 9),
        ).pack(side="left")
        self.qty_entry = tk.Entry(
            qty_bar, bg=BG, fg=TX, insertbackground=TX, width=8
        )
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=8)
        tk.Label(
            qty_bar,
            text="(ex.: 1, 2.5 para KILO)",
            bg=PANEL2,
            fg=MUT,
            font=("Segoe UI", 8),
        ).pack(side="left")

        self.vitrine_frame = tk.Frame(card, bg=PANEL)
        self.vitrine_frame.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="Combos & Cenários Rápidos",
            bg=PANEL,
            fg=MUT,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        presets = tk.Frame(card, bg=PANEL)
        presets.pack(fill="x")
        presets.columnconfigure(0, weight=1)
        presets.columnconfigure(1, weight=1)
        buttons = [
            ("Todas as Estratégias", self._preset_all_strategies, 0, 0),
            ("Combo Completo (1+1)", self._preset_combo_single, 0, 1),
            ("Combo + Excedente (2+1)", self._preset_combo_surplus, 1, 0),
            ("3x2 + Combo (4+1)", self._preset_coexistence, 1, 1),
        ]
        for label, handler, r, c in buttons:
            ttk.Button(
                presets, text=label, style="Ghost.TButton", command=handler
            ).grid(row=r, column=c, sticky="ew", padx=2, pady=2)

        tk.Label(
            card,
            text="Cadastrar Produto no Catálogo (SQLite)",
            bg=PANEL,
            fg=MUT,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        form = tk.Frame(card, bg=PANEL)
        form.pack(fill="x")
        self.new_name = tk.Entry(form, bg=PANEL2, fg=TX, insertbackground=TX)
        self.new_name.insert(0, "soap")
        self.new_name.pack(side="left", fill="x", expand=True)

        self.new_unit = ttk.Combobox(
            form,
            values=["EACH", "KILO"],
            state="readonly",
            width=6,
            style="Dark.TCombobox",
        )
        self.new_unit.set("EACH")
        self.new_unit.pack(side="left", padx=4)

        self.new_price = tk.Entry(
            form, bg=PANEL2, fg=TX, insertbackground=TX, width=7
        )
        self.new_price.insert(0, "2.50")
        self.new_price.pack(side="left", padx=(0, 4))

        ttk.Button(
            form,
            text="Salvar",
            style="Success.TButton",
            command=self._save_new_product,
        ).pack(side="left")

    def _build_cart_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "Sacola de Compras", 1)

        self.cart_list = tk.Listbox(
            card,
            bg=CODE,
            fg=TX,
            font=("Menlo", 10),
            highlightthickness=0,
            borderwidth=0,
            selectbackground=BLUE,
        )
        self.cart_list.pack(fill="both", expand=True, pady=(0, 10))

        btns = tk.Frame(card, bg=PANEL)
        btns.pack(fill="x")
        ttk.Button(
            btns,
            text="Limpar Sacola",
            style="Danger.TButton",
            command=self._clear_cart,
        ).pack(side="left")
        ttk.Button(
            btns,
            text="Finalizar Compra",
            style="Success.TButton",
            command=self._refresh_cart_and_receipt,
        ).pack(side="right")

    def _build_receipt_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "Cupom Fiscal (40 colunas)", 2)

        self.receipt_text = tk.Text(
            card,
            bg=CODE,
            fg="#d4d4d4",
            font=("Menlo", 10),
            highlightthickness=0,
            borderwidth=0,
            padx=10,
            pady=10,
            width=42,
        )
        self.receipt_text.pack(fill="both", expand=True)
        self.receipt_text.config(state="disabled")

    def _refresh_vitrine(self) -> None:
        for child in self.vitrine_frame.winfo_children():
            child.destroy()

        for idx, (product, price) in enumerate(self.catalog.list_products()):
            row = tk.Frame(
                self.vitrine_frame,
                bg=PANEL2,
                highlightbackground=LINE,
                highlightthickness=1,
                padx=10,
                pady=7,
            )
            row.pack(fill="x", pady=3)
            unit_lbl = "UN" if product.unit == ProductUnit.EACH else "KG"
            tk.Label(
                row,
                text=product.name,
                bg=PANEL2,
                fg=TX,
                font=("Segoe UI", 10, "bold"),
            ).pack(side="left")
            tk.Label(
                row,
                text=f"  R$ {price:.2f} / {unit_lbl}",
                bg=PANEL2,
                fg=GREEN,
                font=("Segoe UI", 9, "bold"),
            ).pack(side="left", padx=6)
            ttk.Button(
                row,
                text="+ Adicionar",
                style="Primary.TButton",
                command=lambda p=product: self._add_product(p),
            ).pack(side="right")

    def _add_product(self, product: Product) -> None:
        try:
            qty = float(self.qty_entry.get().replace(",", "."))
            if qty.is_integer() and product.unit == ProductUnit.EACH:
                qty = int(qty)
            self.cart.add_item_quantity(product, qty)
        except ValueError as exc:
            messagebox.showerror("Entrada inválida", str(exc))
            return
        self._refresh_cart_and_receipt()

    def _save_new_product(self) -> None:
        try:
            product = Product(
                self.new_name.get().strip(),
                ProductUnit[self.new_unit.get()],
            )
            price = float(self.new_price.get().replace(",", "."))
            self.catalog.add_product(product, price)
        except ValueError as exc:
            messagebox.showerror("Erro ao salvar", str(exc))
            return
        self._refresh_vitrine()

    def _clear_cart(self) -> None:
        self.cart = ShoppingCart()
        self._refresh_cart_and_receipt()

    def _refresh_cart_and_receipt(self) -> None:
        self.cart_list.delete(0, tk.END)
        quantities = self.cart.product_quantities()
        for product, qty in quantities.items():
            unit_price = self.catalog.unit_price(product)
            qty_str = (
                str(int(qty))
                if product.unit == ProductUnit.EACH
                else f"{qty:.3f}"
            )
            self.cart_list.insert(
                tk.END, f"{product.name:<18} {qty_str:>6} x {unit_price:.2f}"
            )

        output = self.controller.checkout(self.cart)
        total_line = [ln for ln in output.splitlines() if ln.startswith("Total:")]
        total_txt = total_line[-1].split()[-1] if total_line else "0.00"
        self.bag_badge.config(
            text=f"Sacola: {len(quantities)} produtos  |  Total: R$ {total_txt}"
        )

        self.receipt_text.config(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert("1.0", output)
        self.receipt_text.config(state="disabled")

    def _load_preset(self, items: list[tuple[str, float]]) -> None:
        self.cart = ShoppingCart()
        for name, qty in items:
            product = self.catalog.find_by_name(name)
            if product is not None:
                self.cart.add_item_quantity(product, qty)
        self._refresh_cart_and_receipt()

    def _preset_all_strategies(self) -> None:
        self._load_preset(
            [
                ("toothbrush", 4),
                ("apples", 2.5),
                ("toothpaste", 1),
                ("cherry tomatoes", 2),
                ("rice", 5),
            ]
        )

    def _preset_combo_single(self) -> None:
        self._load_preset([("toothbrush", 1), ("toothpaste", 1)])

    def _preset_combo_surplus(self) -> None:
        self._load_preset([("toothbrush", 2), ("toothpaste", 1)])

    def _preset_coexistence(self) -> None:
        self._load_preset([("toothbrush", 4), ("toothpaste", 1)])

    def _on_close(self) -> None:
        self.session.close()
        self.root.destroy()


def main() -> None:
    """Inicia a interface e-commerce Tkinter."""
    root = tk.Tk()
    SupermarketGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
