from dataclasses import dataclass
import csv
import json
from typing import Callable, Dict, List, TypedDict

# Hardcoded stock prices (can be moved to JSON/API later)
STOCK_PRICES = {
    "AAPL": 180.0,
    "TSLA": 250.0,
    "GOOGL": 2800.0,
    "MSFT": 320.0,
    "AMZN": 3500.0,
}


@dataclass
class PortfolioItem:
    symbol: str
    quantity: int
    price: float

    @property
    def value(self) -> float:
        return self.quantity * self.price


class PortfolioMetrics(TypedDict):
    total_value: float
    positions: int
    top_symbol: str
    top_value: float


def format_currency(amount: float) -> str:
    return f"${amount:,.2f}"


def get_positive_int(
    prompt: str,
    input_fn: Callable[[str], str] = input,
    allow_zero: bool = False,
    print_fn: Callable[[str], None] = print,
) -> int:
    while True:
        raw = input_fn(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print_fn("Invalid input. Please enter a whole number.")
            continue

        if value < 0 or (value == 0 and not allow_zero):
            if allow_zero:
                print_fn("Please enter 0 or a positive whole number.")
            else:
                print_fn("Please enter a positive whole number.")
            continue
        return value


def build_portfolio(
    stock_prices: Dict[str, float],
    num_entries: int,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> List[PortfolioItem]:
    quantities: Dict[str, int] = {}

    for _ in range(num_entries):
        symbol = input_fn("Enter stock symbol (e.g., AAPL): ").strip().upper()

        if symbol not in stock_prices:
            print_fn("Stock not found in price list. Entry skipped.\n")
            continue

        quantity = get_positive_int(
            "Enter quantity: ",
            input_fn=input_fn,
            print_fn=print_fn,
        )
        quantities[symbol] = quantities.get(symbol, 0) + quantity

        entry_value = quantity * stock_prices[symbol]
        print_fn(f"Added {quantity} shares of {symbol}")
        print_fn(f"Investment value: {format_currency(entry_value)}\n")

    items = [
        PortfolioItem(symbol=symbol, quantity=qty, price=stock_prices[symbol])
        for symbol, qty in sorted(quantities.items())
    ]
    return items


def calculate_total_value(items: List[PortfolioItem]) -> float:
    return sum(item.value for item in items)


def calculate_portfolio_metrics(items: List[PortfolioItem]) -> PortfolioMetrics:
    total_value = calculate_total_value(items)
    if not items:
        return {
            "total_value": 0.0,
            "positions": 0,
            "top_symbol": "-",
            "top_value": 0.0,
        }

    top_item = max(items, key=lambda item: item.value)
    return {
        "total_value": total_value,
        "positions": len(items),
        "top_symbol": top_item.symbol,
        "top_value": top_item.value,
    }


def generate_summary_lines(items: List[PortfolioItem], total_value: float) -> List[str]:
    lines = ["Stock Portfolio Summary", "------------------------"]
    for item in items:
        lines.append(
            f"{item.symbol} - {item.quantity} shares - {format_currency(item.value)}"
        )
    lines.append("")
    lines.append(f"Total Investment Value: {format_currency(total_value)}")
    return lines


def save_summary(filename: str, lines: List[str]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def save_summary_csv(filename: str, items: List[PortfolioItem], total_value: float) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Symbol", "Quantity", "Price", "Position Value"])
        for item in items:
            writer.writerow(
                [
                    item.symbol,
                    item.quantity,
                    f"{item.price:.2f}",
                    f"{item.value:.2f}",
                ]
            )
        writer.writerow([])
        writer.writerow(["Total Investment Value", "", "", f"{total_value:.2f}"])


def save_portfolio_json(filename: str, quantities: Dict[str, int]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(quantities, file, indent=2, sort_keys=True)


def load_portfolio_json(filename: str) -> Dict[str, int]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

    clean_data: Dict[str, int] = {}
    if not isinstance(data, dict):
        return clean_data

    for symbol, quantity in data.items():
        if (
            isinstance(symbol, str)
            and symbol in STOCK_PRICES
            and isinstance(quantity, int)
            and quantity > 0
        ):
            clean_data[symbol] = quantity
    return clean_data


def main() -> None:
    print("Welcome to Stock Portfolio Tracker\n")
    num_entries = get_positive_int(
        "How many different stocks do you want to add? ",
        allow_zero=True,
    )

    portfolio_items = build_portfolio(STOCK_PRICES, num_entries)
    total_value = calculate_total_value(portfolio_items)
    summary_lines = generate_summary_lines(portfolio_items, total_value)

    print("----- Portfolio Summary -----")
    for line in summary_lines[2:]:
        print(line)

    output_file = "portfolio_summary.txt"
    save_summary(output_file, summary_lines)
    print(f"\nPortfolio saved to '{output_file}'")


if __name__ == "__main__":
    main()
