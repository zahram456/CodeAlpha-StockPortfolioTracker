# CodeAlpha Stock Portfolio Tracker

A Python-based stock portfolio tracker with two interfaces:
- `CLI` for quick terminal workflows
- `GUI` for a richer desktop experience with portfolio analytics

The project uses a SQLite-backed persistence layer to track holdings, transactions, snapshots, and export history.

## Key Features

### Core Portfolio Logic
- Tracks holdings by stock name and quantity
- Aggregates duplicate stock names into a single position
- Calculates per-position and total portfolio value
- Formats values as currency for reports and UI
- Stores portfolio data in `portfolio.db` for reliable persistence
- Records holdings changes in a transaction log
- Captures portfolio snapshots for historical comparison

### Desktop GUI (`tkinter`)
- Professional dashboard layout with KPI cards:
  - Total portfolio value
  - Number of positions
  - Top holding by value
- Add mode and Set mode for flexible quantity updates
- Sortable portfolio table columns
- Live stock filtering
- Menu bar with export and portfolio management actions
- Keyboard shortcuts:
  - `Enter` save holding
  - `Delete` remove selected holding
  - `Ctrl+S` export TXT
  - `Ctrl+Shift+S` export CSV
  - `Ctrl+P` export PDF
- Allocation pie chart
- Top movers panel (enabled after at least two snapshots)
- Recent exports activity panel

### Reporting
- Text summary export to `portfolio_summary.txt`
- CSV export to `portfolio_summary.csv`
- PDF export to `portfolio_summary.pdf`
- Export actions recorded in database history

### Engineering Quality
- Unit tests covering portfolio calculations, persistence, snapshots, exports, validation, and edge cases
- Shared business logic used by both CLI and GUI
- GitHub Actions CI for lint + tests on push and pull request

## Tech Stack
- Python 3
- Tkinter (standard library)
- SQLite (`sqlite3` standard library)
- `unittest` for test automation
- Ruff for linting in CI

## Project Structure
- `stock_tracker.py` - core domain logic and CLI entrypoint
- `stock_tracker_gui.py` - desktop GUI entrypoint
- `test_stock_tracker.py` - unit test suite
- `.github/workflows/ci.yml` - CI pipeline (lint + tests)
- `.gitignore` - excludes generated/cache files

Generated runtime files:
- `portfolio.db` (SQLite persistence database)
- `portfolio_summary.txt` (text report)
- `portfolio_summary.csv` (CSV report)
- `portfolio_summary.pdf` (PDF report)

## Supported Stocks and Prices
Current implementation uses predefined prices:
- `Apple`: 180
- `Tesla`: 250
- `Alphabet`: 2800
- `Microsoft`: 320
- `Amazon`: 3500

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
Current suite: `15` passing tests.

## Design Notes
- Input is normalized to title case stock names.
- Invalid stock names are rejected safely.
- Database writes also validate stock names to prevent unsupported entries.
- Persistence uses SQLite tables: `holdings`, `transactions`, `snapshots`, `snapshot_items`, `export_history`.
- Export artifacts are intentionally local and excluded from source control.

## Roadmap
- Live market price integration (API with fallback)
- Historical performance tracking
- Portfolio allocation charts
- Packaging as a standalone desktop executable

## License
This project is intended for learning and practice.
