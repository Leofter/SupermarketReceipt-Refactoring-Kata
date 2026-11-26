"""Interface gráfica PDV estilo anos 80/90 em Tkinter."""

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

BG = "#c0c0c0"
PANEL = "#d4d0c8"
NAVY = "#000080"
DARK = "#404040"
TX = "#000000"
PAPER = "#faf6e8"
TERM_BG = "#081408"
TERM_FG = "#33ff33"
FONT = "Helvetica"
MONO = "Courier"


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
    """PDV retrô anos 80/90 conectado ao CheckoutController e SQLite."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CIMATEC MARKET PDV v1.0 [1994]")
        self.root.geometry("1380x840")
        self.root.minsize(1120, 700)
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
            "Retro.TCombobox",
            fieldbackground="#ffffff",
            background=PANEL,
            foreground=TX,
            font=(MONO, 11, "bold"),
        )
        for name, bg, fg in [
            ("Retro.TButton", PANEL, TX),
            ("RetroOk.TButton", "#008080", "#ffffff"),
            ("RetroClear.TButton", "#800000", "#ffffff"),
        ]:
            style.configure(
                name,
                background=bg,
                foreground=fg,
                relief="raised",
                borderwidth=2,
                padding=(10, 7),
                font=(MONO, 11, "bold"),
            )
            style.map(
                name,
                relief=[("pressed", "sunken")],
                background=[("active", "#e4e0d8" if bg == PANEL else bg)],
            )

    def _build_ui(self) -> None:
        header = tk.Frame(self.root, bg=NAVY, relief="raised", bd=2)
        header.pack(fill="x", padx=14, pady=(12, 10))

        tk.Label(
            header,
            text=" [SENAI CIMATEC]  CIMATEC MARKET - TERMINAL PDV 1994 ",
            bg=NAVY,
            fg="#ffffff",
            font=(MONO, 15, "bold"),
            pady=8,
        ).pack(side="left", padx=8)

        self.bag_badge = tk.Label(
            header,
            text="SACOLA: 0 | TOTAL: R$ 0.00",
            bg=TERM_BG,
            fg=TERM_FG,
            font=(MONO, 13, "bold"),
            relief="sunken",
            bd=2,
            padx=12,
            pady=4,
        )
        self.bag_badge.pack(side="right", padx=10, pady=6)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        body.columnconfigure(0, weight=5)
        body.columnconfigure(1, weight=3)
        body.columnconfigure(2, weight=5)
        body.rowconfigure(0, weight=1)

        self._build_vitrine_panel(body)
        self._build_cart_panel(body)
        self._build_receipt_panel(body)

    def _card(self, parent: tk.Widget, title: str, col: int) -> tk.Frame:
        outer = tk.Frame(parent, bg=BG, relief="raised", bd=2, padx=10, pady=10)
        outer.grid(row=0, column=col, sticky="nsew", padx=6)
        tk.Label(
            outer,
            text=title,
            bg=NAVY,
            fg="#ffffff",
            font=(MONO, 12, "bold"),
            anchor="w",
            padx=8,
            pady=4,
        ).pack(fill="x", pady=(0, 10))
        return outer

    def _build_vitrine_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "1. CATALOGO DE PRODUTOS", 0)

        qty_bar = tk.Frame(card, bg=PANEL, relief="groove", bd=2, padx=8, pady=8)
        qty_bar.pack(fill="x", pady=(0, 8))
        tk.Label(
            qty_bar,
            text="QTD:",
            bg=PANEL,
            fg=TX,
            font=(MONO, 11, "bold"),
        ).pack(side="left")
        self.qty_entry = tk.Entry(
            qty_bar,
            bg="#ffffff",
            fg=TX,
            width=8,
            font=(MONO, 12, "bold"),
            relief="sunken",
            bd=2,
            justify="center",
        )
        self.qty_entry.insert(0, "1")
        self.qty_entry.pack(side="left", padx=8)
        tk.Label(
            qty_bar,
            text="(use decimal p/ KILO, ex: 2.5)",
            bg=PANEL,
            fg=DARK,
            font=(FONT, 10),
        ).pack(side="left")

        list_wrap = tk.Frame(card, bg=BG, relief="sunken", bd=2)
        list_wrap.pack(fill="both", expand=True)
        canvas = tk.Canvas(list_wrap, bg=PANEL, highlightthickness=0)
        scroll = ttk.Scrollbar(
            list_wrap, orient="vertical", command=canvas.yview
        )
        self.vitrine_frame = tk.Frame(canvas, bg=PANEL)
        self.vitrine_frame.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        win = canvas.create_window((0, 0), window=self.vitrine_frame, anchor="nw")
        canvas.bind(
            "<Configure>", lambda e: canvas.itemconfigure(win, width=e.width)
        )
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(
            card,
            text="ATALHOS DE DEMONSTRACAO:",
            bg=BG,
            fg=TX,
            font=(MONO, 10, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        presets = tk.Frame(card, bg=BG)
        presets.pack(fill="x")
        presets.columnconfigure(0, weight=1)
        presets.columnconfigure(1, weight=1)
        buttons = [
            ("[F1] Todas Estrategias", self._preset_all_strategies, 0, 0),
            ("[F2] Combo (1+1)", self._preset_combo_single, 0, 1),
            ("[F3] Excedente (2+1)", self._preset_combo_surplus, 1, 0),
            ("[F4] 3x2 + Combo (4+1)", self._preset_coexistence, 1, 1),
        ]
        for label, handler, r, c in buttons:
            ttk.Button(
                presets, text=label, style="Retro.TButton", command=handler
            ).grid(row=r, column=c, sticky="ew", padx=3, pady=3)

        tk.Label(
            card,
            text="CADASTRAR ITEM NO BANCO (SQLITE):",
            bg=BG,
            fg=TX,
            font=(MONO, 10, "bold"),
        ).pack(anchor="w", pady=(10, 4))

        form = tk.Frame(card, bg=PANEL, relief="groove", bd=2, padx=8, pady=8)
        form.pack(fill="x")
        self.new_name = tk.Entry(
            form, bg="#ffffff", fg=TX, font=(MONO, 11), relief="sunken", bd=2
        )
        self.new_name.insert(0, "soap")
        self.new_name.pack(side="left", fill="x", expand=True)

        self.new_unit = ttk.Combobox(
            form,
            values=["EACH", "KILO"],
            state="readonly",
            width=6,
            style="Retro.TCombobox",
            font=(MONO, 11),
        )
        self.new_unit.set("EACH")
        self.new_unit.pack(side="left", padx=6)

        self.new_price = tk.Entry(
            form,
            bg="#ffffff",
            fg=TX,
            width=7,
            font=(MONO, 11),
            relief="sunken",
            bd=2,
            justify="center",
        )
        self.new_price.insert(0, "2.50")
        self.new_price.pack(side="left", padx=(0, 6))

        ttk.Button(
            form,
            text="GRAVAR",
            style="RetroOk.TButton",
            command=self._save_new_product,
        ).pack(side="left")

    def _build_cart_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "2. TERMINAL DE COMPRAS", 1)

        tk.Label(
            card,
            text=f"{'PRODUTO':<17} {'QTD':>6}  {'UNIT.':>6}",
            bg=TERM_BG,
            fg=TERM_FG,
            font=(MONO, 11, "bold"),
            anchor="w",
            padx=8,
            pady=6,
        ).pack(fill="x")

        self.cart_list = tk.Listbox(
            card,
            bg=TERM_BG,
            fg=TERM_FG,
            font=(MONO, 12, "bold"),
            relief="sunken",
            bd=3,
            selectbackground="#008080",
            selectforeground="#ffffff",
        )
        self.cart_list.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(
            card,
            text="LIMPAR",
            style="RetroClear.TButton",
            command=self._clear_cart,
        ).pack(fill="x")

    def _build_receipt_panel(self, parent: tk.Widget) -> None:
        card = self._card(parent, "3. CUPOM MATRICIAL (40 COL.)", 2)

        self.receipt_text = tk.Text(
            card,
            bg=PAPER,
            fg="#111111",
            font=(MONO, 12),
            relief="sunken",
            bd=3,
            padx=12,
            pady=12,
            width=44,
        )
        self.receipt_text.pack(fill="both", expand=True)
        self.receipt_text.config(state="disabled")

    def _refresh_vitrine(self) -> None:
        for child in self.vitrine_frame.winfo_children():
            child.destroy()

        for product, price in self.catalog.list_products():
            row = tk.Frame(
                self.vitrine_frame,
                bg=BG,
                relief="raised",
                bd=2,
                padx=8,
                pady=6,
            )
            row.pack(fill="x", padx=4, pady=3)
            unit_lbl = "UN" if product.unit == ProductUnit.EACH else "KG"
            tk.Label(
                row,
                text=product.name.upper(),
                bg=BG,
                fg=TX,
                font=(MONO, 11, "bold"),
            ).pack(side="left")
            tk.Label(
                row,
                text=f"R$ {price:.2f}/{unit_lbl}",
                bg=BG,
                fg=NAVY,
                font=(MONO, 11, "bold"),
            ).pack(side="left", padx=10)
            ttk.Button(
                row,
                text="[+] ADD",
                style="Retro.TButton",
                command=lambda p=product: self._add_product(p),
            ).pack(side="right")

    def _add_product(self, product: Product) -> None:
        try:
            qty = float(self.qty_entry.get().replace(",", "."))
            if qty.is_integer() and product.unit == ProductUnit.EACH:
                qty = int(qty)
            self.cart.add_item_quantity(product, qty)
        except ValueError as exc:
            messagebox.showerror("ERRO DE ENTRADA", str(exc))
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
            messagebox.showerror("ERRO AO GRAVAR", str(exc))
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
                tk.END,
                f" {product.name.upper():<16} {qty_str:>6} x {unit_price:>5.2f}",
            )

        output = self.controller.checkout(self.cart)
        total_line = [ln for ln in output.splitlines() if ln.startswith("Total:")]
        total_txt = total_line[-1].split()[-1] if total_line else "0.00"
        self.bag_badge.config(
            text=f"ITENS: {len(quantities)} | TOTAL: R$ {total_txt}"
        )

        header = (
            "========================================\n"
            "      CIMATEC MARKET - CUPOM FISCAL     \n"
            "========================================\n"
        )
        self.receipt_text.config(state="normal")
        self.receipt_text.delete("1.0", tk.END)
        self.receipt_text.insert("1.0", header + output)
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
    """Inicia a interface PDV retrô em Tkinter."""
    root = tk.Tk()
    SupermarketGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
