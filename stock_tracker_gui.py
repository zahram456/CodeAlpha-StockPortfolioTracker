import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

from stock_tracker import (
    STOCK_PRICES,
    PortfolioItem,
    calculate_portfolio_metrics,
    calculate_total_value,
    format_currency,
    generate_summary_lines,
    load_portfolio_json,
    save_portfolio_json,
    save_summary,
    save_summary_csv,
)

DATA_FILE = "portfolio_data.json"


class PortfolioTrackerGUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("940x620")
        self.root.minsize(860, 560)
        self.root.configure(bg="#f4f8ff")

        self.quantities = load_portfolio_json(DATA_FILE)
        self.sort_column = "symbol"
        self.sort_reverse = False

        self._setup_style()
        self._build_menu()
        self._build_layout()
        self._refresh_table()

    def _setup_style(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f4f8ff")
        style.configure(
            "Card.TFrame",
            background="#ffffff",
            relief="flat",
        )
        style.configure(
            "Title.TLabel",
            font=("Segoe UI Semibold", 20),
            background="#f4f8ff",
            foreground="#152238",
        )
        style.configure(
            "Sub.TLabel",
            font=("Segoe UI", 10),
            background="#f4f8ff",
            foreground="#425466",
        )
        style.configure(
            "CardTitle.TLabel",
            font=("Segoe UI Semibold", 11),
            background="#ffffff",
            foreground="#25364d",
        )
        style.configure(
            "KpiLabel.TLabel",
            font=("Segoe UI", 9),
            background="#ffffff",
            foreground="#56657a",
        )
        style.configure(
            "Value.TLabel",
            font=("Segoe UI Semibold", 14),
            background="#ffffff",
            foreground="#0f9d58",
        )
        style.configure(
            "Accent.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(14, 8),
        )
        style.map(
            "Accent.TButton",
            background=[("!disabled", "#1f6feb"), ("active", "#1859bb")],
            foreground=[("!disabled", "#ffffff")],
        )
        style.configure(
            "Danger.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(12, 8),
        )
        style.map(
            "Danger.TButton",
            background=[("!disabled", "#cc3a3a"), ("active", "#a82f2f")],
            foreground=[("!disabled", "#ffffff")],
        )
        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#1f2d3d",
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI Semibold", 10),
            background="#e7eefb",
            foreground="#203047",
        )

    def _build_menu(self) -> None:
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Export Summary (.txt)", command=self.export_summary)
        file_menu.add_command(label="Export CSV (.csv)", command=self.export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Remove Selected", command=self.remove_selected)
        edit_menu.add_command(label="Clear Portfolio", command=self.clear_portfolio)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menu_bar)

    def _build_layout(self) -> None:
        container = ttk.Frame(self.root, style="App.TFrame", padding=18)
        container.pack(fill="both", expand=True)

        header = ttk.Frame(container, style="App.TFrame")
        header.pack(fill="x", pady=(0, 14))
        ttk.Label(header, text="Stock Portfolio Tracker", style="Title.TLabel").pack(
            anchor="w"
        )
        ttk.Label(
            header,
            text="Track holdings, update quantities, and export a summary report.",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        top_row = ttk.Frame(container, style="App.TFrame")
        top_row.pack(fill="x", pady=(0, 12))

        input_card = ttk.Frame(top_row, style="Card.TFrame", padding=14)
        input_card.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Label(input_card, text="Add or Update Holding", style="CardTitle.TLabel").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(0, 10)
        )

        ttk.Label(input_card, text="Symbol").grid(row=1, column=0, sticky="w")
        ttk.Label(input_card, text="Quantity").grid(row=1, column=2, sticky="w", padx=(12, 0))

        self.symbol_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.entry_mode_var = tk.StringVar(value="add")

        self.symbol_combo = ttk.Combobox(
            input_card,
            textvariable=self.symbol_var,
            values=sorted(STOCK_PRICES.keys()),
            width=16,
        )
        self.symbol_combo.grid(row=2, column=0, sticky="w", pady=(4, 0))
        self.symbol_combo.set("AAPL")

        self.quantity_entry = ttk.Entry(
            input_card,
            textvariable=self.quantity_var,
            width=14,
        )
        self.quantity_entry.grid(row=2, column=2, sticky="w", padx=(12, 0), pady=(4, 0))

        mode_frame = ttk.Frame(input_card, style="Card.TFrame")
        mode_frame.grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 0))
        ttk.Radiobutton(
            mode_frame,
            text="Add Quantity",
            variable=self.entry_mode_var,
            value="add",
        ).pack(side="left")
        ttk.Radiobutton(
            mode_frame,
            text="Set Exact Quantity",
            variable=self.entry_mode_var,
            value="set",
        ).pack(side="left", padx=(12, 0))

        ttk.Button(
            input_card,
            text="Add / Update",
            style="Accent.TButton",
            command=self.add_or_update_holding,
        ).grid(row=2, column=3, sticky="w", padx=(12, 0), pady=(4, 0))

        for idx in range(4):
            input_card.grid_columnconfigure(idx, weight=1 if idx in (0, 2) else 0)

        summary_card = ttk.Frame(top_row, style="Card.TFrame", padding=14)
        summary_card.pack(side="right", fill="both")
        ttk.Label(summary_card, text="Portfolio Snapshot", style="CardTitle.TLabel").pack(
            anchor="w"
        )
        ttk.Label(summary_card, text="Total Value", style="KpiLabel.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        self.total_value_label = ttk.Label(
            summary_card,
            text=format_currency(0),
            style="Value.TLabel",
        )
        self.total_value_label.pack(anchor="w")

        ttk.Label(summary_card, text="Positions", style="KpiLabel.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        self.positions_value_label = ttk.Label(
            summary_card,
            text="0",
            style="Value.TLabel",
        )
        self.positions_value_label.pack(anchor="w")

        ttk.Label(summary_card, text="Top Holding", style="KpiLabel.TLabel").pack(
            anchor="w", pady=(8, 0)
        )
        self.top_holding_label = ttk.Label(
            summary_card,
            text="-",
            style="Value.TLabel",
        )
        self.top_holding_label.pack(anchor="w")

        table_card = ttk.Frame(container, style="Card.TFrame", padding=12)
        table_card.pack(fill="both", expand=True, pady=(0, 12))

        filter_row = ttk.Frame(table_card, style="Card.TFrame")
        filter_row.pack(fill="x", pady=(0, 8))
        ttk.Label(filter_row, text="Filter Symbol").pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(filter_row, textvariable=self.filter_var, width=20)
        self.filter_entry.pack(side="left", padx=(8, 0))
        ttk.Button(filter_row, text="Clear", command=self.clear_filter).pack(
            side="left", padx=(8, 0)
        )

        columns = ("symbol", "quantity", "price", "value", "weight")
        self.table = ttk.Treeview(table_card, columns=columns, show="headings")
        self.table.heading("symbol", text="Symbol", command=lambda: self.sort_by("symbol"))
        self.table.heading(
            "quantity", text="Quantity", command=lambda: self.sort_by("quantity")
        )
        self.table.heading("price", text="Price", command=lambda: self.sort_by("price"))
        self.table.heading(
            "value", text="Position Value", command=lambda: self.sort_by("value")
        )
        self.table.heading(
            "weight", text="Portfolio Weight", command=lambda: self.sort_by("weight")
        )

        self.table.column("symbol", anchor="center", width=90)
        self.table.column("quantity", anchor="center", width=90)
        self.table.column("price", anchor="e", width=140)
        self.table.column("value", anchor="e", width=160)
        self.table.column("weight", anchor="e", width=130)

        scrollbar = ttk.Scrollbar(table_card, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = ttk.Frame(container, style="App.TFrame")
        actions.pack(fill="x")

        ttk.Button(
            actions,
            text="Remove Selected",
            style="Danger.TButton",
            command=self.remove_selected,
        ).pack(side="left")

        ttk.Button(
            actions,
            text="Clear Portfolio",
            command=self.clear_portfolio,
        ).pack(side="left", padx=(8, 0))

        ttk.Button(
            actions,
            text="Export Summary",
            style="Accent.TButton",
            command=self.export_summary,
        ).pack(side="right")
        ttk.Button(
            actions,
            text="Export CSV",
            command=self.export_csv,
        ).pack(side="right", padx=(0, 8))

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(container, textvariable=self.status_var, style="Sub.TLabel")
        status_label.pack(anchor="w", pady=(8, 0))

        self.quantity_entry.bind("<Return>", self._on_enter_pressed)
        self.symbol_combo.bind("<Return>", self._on_enter_pressed)
        self.filter_entry.bind("<Return>", lambda _event: self._refresh_table())
        self.table.bind("<<TreeviewSelect>>", self._load_selected_into_form)
        self.filter_var.trace_add("write", self._on_filter_change)

    def _validated_inputs(self) -> tuple[str, int] | None:
        symbol = self.symbol_var.get().strip().upper()
        qty_raw = self.quantity_var.get().strip()

        if symbol not in STOCK_PRICES:
            messagebox.showerror(
                "Invalid Symbol",
                f"Symbol '{symbol}' is not in the supported list: {', '.join(STOCK_PRICES)}",
            )
            return None

        if not qty_raw.isdigit() or int(qty_raw) <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be a positive whole number.",
            )
            return None

        return symbol, int(qty_raw)

    def _portfolio_items(self) -> list[PortfolioItem]:
        return [
            PortfolioItem(symbol=symbol, quantity=qty, price=STOCK_PRICES[symbol])
            for symbol, qty in sorted(self.quantities.items())
        ]

    def _visible_items(self, items: list[PortfolioItem]) -> list[PortfolioItem]:
        filter_text = self.filter_var.get().strip().upper()
        visible = items
        if filter_text:
            visible = [item for item in items if filter_text in item.symbol]

        if self.sort_column == "symbol":
            key_fn = lambda item: item.symbol
        elif self.sort_column == "quantity":
            key_fn = lambda item: item.quantity
        elif self.sort_column == "price":
            key_fn = lambda item: item.price
        elif self.sort_column == "value":
            key_fn = lambda item: item.value
        else:
            key_fn = lambda item: item.value

        return sorted(visible, key=key_fn, reverse=self.sort_reverse)

    def _refresh_table(self) -> None:
        for row in self.table.get_children():
            self.table.delete(row)

        all_items = self._portfolio_items()
        visible_items = self._visible_items(all_items)
        total = calculate_total_value(all_items)

        for item in visible_items:
            weight = 0 if total == 0 else (item.value / total) * 100
            self.table.insert(
                "",
                "end",
                iid=item.symbol,
                values=(
                    item.symbol,
                    item.quantity,
                    format_currency(item.price),
                    format_currency(item.value),
                    f"{weight:.1f}%",
                ),
            )

        metrics = calculate_portfolio_metrics(all_items)
        self.total_value_label.configure(text=format_currency(metrics["total_value"]))
        self.positions_value_label.configure(text=str(metrics["positions"]))
        self.top_holding_label.configure(
            text=f'{metrics["top_symbol"]} ({format_currency(metrics["top_value"])})'
            if metrics["positions"] > 0
            else "-"
        )
        status_time = datetime.now().strftime("%H:%M:%S")
        self.status_var.set(
            f"Showing {len(visible_items)} of {metrics['positions']} holdings | Updated {status_time}"
        )

    def _persist_quantities(self) -> None:
        save_portfolio_json(DATA_FILE, self.quantities)

    def _on_enter_pressed(self, _event: tk.Event) -> None:
        self.add_or_update_holding()

    def _on_filter_change(self, *_: object) -> None:
        self._refresh_table()

    def clear_filter(self) -> None:
        self.filter_var.set("")

    def sort_by(self, column: str) -> None:
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False
        self._refresh_table()

    def show_about(self) -> None:
        messagebox.showinfo(
            "About",
            "Stock Portfolio Tracker\nProfessional GUI Edition\nBuilt with Python + Tkinter",
        )

    def _load_selected_into_form(self, _event: tk.Event) -> None:
        selected = self.table.selection()
        if not selected:
            return
        symbol = selected[0]
        quantity = self.quantities.get(symbol)
        if quantity is None:
            return
        self.symbol_var.set(symbol)
        self.quantity_var.set(str(quantity))
        self.entry_mode_var.set("set")

    def add_or_update_holding(self) -> None:
        parsed = self._validated_inputs()
        if parsed is None:
            return

        symbol, quantity = parsed
        if self.entry_mode_var.get() == "set":
            self.quantities[symbol] = quantity
        else:
            self.quantities[symbol] = self.quantities.get(symbol, 0) + quantity
        self._persist_quantities()
        self._refresh_table()
        self.quantity_var.set("")
        self.status_var.set(f"Updated {symbol}.")

    def remove_selected(self) -> None:
        selected = self.table.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Select a row to remove.")
            return

        for row_id in selected:
            self.quantities.pop(row_id, None)
        self._persist_quantities()
        self._refresh_table()
        self.status_var.set("Removed selected holding(s).")

    def clear_portfolio(self) -> None:
        if not self.quantities:
            return
        confirmed = messagebox.askyesno(
            "Clear Portfolio",
            "Remove all holdings from the portfolio?",
        )
        if confirmed:
            self.quantities.clear()
            self._persist_quantities()
            self._refresh_table()
            self.status_var.set("Portfolio cleared.")

    def export_summary(self) -> None:
        items = self._portfolio_items()
        total = calculate_total_value(items)
        lines = generate_summary_lines(items, total)
        save_summary("portfolio_summary.txt", lines)
        messagebox.showinfo("Saved", "Portfolio saved to 'portfolio_summary.txt'.")
        self.status_var.set("Exported summary text file.")

    def export_csv(self) -> None:
        items = self._portfolio_items()
        total = calculate_total_value(items)
        save_summary_csv("portfolio_summary.csv", items, total)
        messagebox.showinfo("Saved", "Portfolio saved to 'portfolio_summary.csv'.")
        self.status_var.set("Exported CSV file.")


def main() -> None:
    root = tk.Tk()
    PortfolioTrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
