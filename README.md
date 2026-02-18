# CodeAlpha Stock Portfolio Tracker

A simple Python CLI project that tracks stock investments using predefined stock prices.

## Features
- Accepts multiple stock entries from user input
- Calculates per-stock investment value (`quantity x price`)
- Computes total portfolio investment value
- Prints a portfolio summary in the terminal
- Saves summary to `portfolio_summary.txt`

## Tech Stack
- Python 3

## Project Files
- `stock_tracker.py` - main script for portfolio tracking
- `portfolio_summary.txt` - generated output file with portfolio summary

## Predefined Stock Prices
The script currently uses hardcoded prices for:
- `AAPL`: 180
- `TSLA`: 250
- `GOOGL`: 2800
- `MSFT`: 320
- `AMZN`: 3500

## How to Run
1. Open terminal in this project folder.
2. Run:

```bash
python stock_tracker.py
```

## Example Flow
- Enter number of stocks to add
- For each stock, enter symbol and quantity
- View portfolio summary and total investment
- Find saved report in `portfolio_summary.txt`

## Notes
- Stock symbols are case-insensitive in input (converted to uppercase).
- If a symbol is not in the predefined list, it is skipped with a warning.

## License
This project is for learning and practice.
