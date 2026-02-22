# CodeAlpha Stock Portfolio Tracker

A Python stock portfolio tracker with both CLI and desktop GUI modes.

## Features
- Accepts multiple stock entries from user input
- Validates numeric input to prevent crashes
- Aggregates duplicate symbols into one portfolio position
- Calculates per-stock investment value (`quantity x price`)
- Computes total portfolio investment value
- Prints a formatted portfolio summary in the terminal
- Saves summary to `portfolio_summary.txt`
- Includes a styled GUI built with `tkinter`
- Saves portfolio state automatically in `portfolio_data.json`
- Supports both text and CSV export (`portfolio_summary.txt`, `portfolio_summary.csv`)
- Provides Add mode and Set mode in GUI for faster quantity updates
- Adds a professional menu bar (File/Edit/Help)
- Includes portfolio KPI cards (total value, position count, top holding)
- Supports live symbol filtering and sortable table columns
- Includes unit tests for core behavior

## Tech Stack
- Python 3
- Tkinter (Python standard library)

## Project Files
- `stock_tracker.py` - CLI script and shared portfolio logic
- `stock_tracker_gui.py` - desktop GUI app
- `portfolio_summary.txt` - generated output file with portfolio summary
- `portfolio_summary.csv` - generated CSV report
- `portfolio_data.json` - auto-saved GUI portfolio state

## Predefined Stock Prices
The script currently uses hardcoded prices for:
- `AAPL`: 180
- `TSLA`: 250
- `GOOGL`: 2800
- `MSFT`: 320
- `AMZN`: 3500

## How to Run
1. Open terminal in this project folder.
2. Run CLI:

```bash
python stock_tracker.py
```

3. Run GUI:

```bash
python stock_tracker_gui.py
```

## Run Tests
```bash
python -m unittest -v
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
