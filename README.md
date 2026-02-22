# CodeAlpha Stock Portfolio Tracker

A Python-based stock portfolio tracker with two interfaces:
- `CLI` for quick terminal workflows
- `GUI` for a richer desktop experience with portfolio analytics

The project is structured to keep portfolio logic reusable across both interfaces.

## Key Features

### Core Portfolio Logic
- Tracks holdings by symbol and quantity
- Aggregates duplicate symbols into a single position
- Calculates per-position and total portfolio value
- Formats values as currency for reports and UI

### Desktop GUI (`tkinter`)
- Professional dashboard layout with KPI cards:
  - Total portfolio value
  - Number of positions
  - Top holding by value
- Add mode and Set mode for flexible quantity updates
- Sortable portfolio table columns
- Live symbol filtering
- Menu bar with export and portfolio management actions
- Auto-save and auto-load of local portfolio state

### Reporting
- Text summary export to `portfolio_summary.txt`
- CSV export to `portfolio_summary.csv`

### Engineering Quality
- Unit tests covering portfolio calculations, validation, persistence, and export
- Shared business logic used by both CLI and GUI

## Tech Stack
- Python 3
- Tkinter (standard library)
- `unittest` for test automation

## Project Structure
- `stock_tracker.py` - core domain logic and CLI entrypoint
- `stock_tracker_gui.py` - desktop GUI entrypoint
- `test_stock_tracker.py` - unit test suite
- `.gitignore` - excludes generated/cache files

Generated runtime files:
- `portfolio_data.json` (GUI auto-save)
- `portfolio_summary.txt` (text report)
- `portfolio_summary.csv` (CSV report)

## Supported Symbols and Prices
Current implementation uses predefined prices:
- `AAPL`: 180
- `TSLA`: 250
- `GOOGL`: 2800
- `MSFT`: 320
- `AMZN`: 3500

## Getting Started

### 1. Clone and enter the project
```bash
git clone https://github.com/zahram456/CodeAlpha-StockPortfolioTracker.git
cd CodeAlpha-StockPortfolioTracker
```

### 2. Run CLI
```bash
python stock_tracker.py
```

### 3. Run GUI
```bash
python stock_tracker_gui.py
```

## Testing
Run the full test suite:
```bash
python -m unittest -v
```

## Design Notes
- Input is normalized to uppercase symbols.
- Invalid symbols are rejected safely.
- Portfolio state persists locally for GUI sessions.
- Export artifacts are intentionally local and excluded from source control.

## Roadmap
- Live market price integration (API with fallback)
- Historical performance tracking
- Portfolio allocation charts
- Packaging as a standalone desktop executable

## License
This project is intended for learning and practice.
