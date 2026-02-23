import csv
import os
import tempfile
import unittest

import stock_tracker


class TestStockTracker(unittest.TestCase):
    def test_format_currency(self):
        self.assertEqual(stock_tracker.format_currency(1234.5), "$1,234.50")

    def test_get_positive_int_retries_until_valid(self):
        values = iter(["abc", "-1", "0", "3"])

        def fake_input(_):
            return next(values)

        result = stock_tracker.get_positive_int(
            "Enter: ",
            input_fn=fake_input,
            allow_zero=False,
            print_fn=lambda _: None,
        )
        self.assertEqual(result, 3)

    def test_build_portfolio_aggregates_duplicate_symbols(self):
        prices = {"Apple": 100.0, "Tesla": 200.0}
        values = iter(["apple", "2", "Apple", "3", "Tesla", "1"])

        def fake_input(_):
            return next(values)

        items = stock_tracker.build_portfolio(
            prices, 3, input_fn=fake_input, print_fn=lambda _: None
        )
        as_dict = {item.symbol: item.quantity for item in items}
        self.assertEqual(as_dict["Apple"], 5)
        self.assertEqual(as_dict["Tesla"], 1)

    def test_build_portfolio_skips_unknown_symbol(self):
        prices = {"Apple": 100.0}
        values = iter(["XXXX", "Apple", "2"])

        def fake_input(_):
            return next(values)

        items = stock_tracker.build_portfolio(
            prices, 2, input_fn=fake_input, print_fn=lambda _: None
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].symbol, "Apple")
        self.assertEqual(items[0].quantity, 2)

    def test_calculate_total_value(self):
        items = [
            stock_tracker.PortfolioItem("Apple", 2, 100.0),
            stock_tracker.PortfolioItem("Tesla", 1, 250.0),
        ]
        self.assertEqual(stock_tracker.calculate_total_value(items), 450.0)

    def test_calculate_portfolio_metrics_empty(self):
        metrics = stock_tracker.calculate_portfolio_metrics([])
        self.assertEqual(metrics["total_value"], 0.0)
        self.assertEqual(metrics["positions"], 0)
        self.assertEqual(metrics["top_symbol"], "-")
        self.assertEqual(metrics["top_value"], 0.0)

    def test_calculate_allocation_percentages(self):
        items = [
            stock_tracker.PortfolioItem("Apple", 1, 100.0),
            stock_tracker.PortfolioItem("Tesla", 1, 300.0),
        ]
        allocations = dict(stock_tracker.calculate_allocation_percentages(items))
        self.assertAlmostEqual(allocations["Apple"], 25.0)
        self.assertAlmostEqual(allocations["Tesla"], 75.0)

    def test_calculate_top_movers(self):
        items = [
            stock_tracker.PortfolioItem("Apple", 2, 100.0),  # 200 (prev 100 => +100)
            stock_tracker.PortfolioItem("Tesla", 1, 250.0),  # 250 (prev 450 => -200)
            stock_tracker.PortfolioItem("Microsoft", 1, 100.0),  # 100 (prev 0 => +100)
        ]
        movers = stock_tracker.calculate_top_movers(
            items,
            {"Apple": 100.0, "Tesla": 450.0},
            top_n=2,
        )
        self.assertEqual(movers[0], ("Tesla", -200.0))
        self.assertIn(movers[1][0], {"Apple", "Microsoft"})

    def test_save_summary_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "summary.csv")
            items = [
                stock_tracker.PortfolioItem("Apple", 2, 100.0),
                stock_tracker.PortfolioItem("Tesla", 1, 250.0),
            ]
            stock_tracker.save_summary_csv(filename, items, 450.0)
            with open(filename, "r", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(rows[0], ["Stock Name", "Quantity", "Price", "Position Value"])
            self.assertEqual(rows[1], ["Apple", "2", "100.00", "200.00"])
            self.assertEqual(rows[4], ["Total Investment Value", "", "", "450.00"])

    def test_save_summary_pdf(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "summary.pdf")
            lines = ["Stock Portfolio Summary", "AAPL - 2 shares - $200.00"]
            stock_tracker.save_summary_pdf(filename, lines)
            with open(filename, "rb") as file:
                header = file.read(5)
            self.assertEqual(header, b"%PDF-")

    def test_portfolio_db_holdings_and_transactions(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "portfolio.db")
            db = stock_tracker.PortfolioDB(db_path)
            db.initialize()
            db.add_holding("Apple", 2, 180.0)
            db.add_holding("Apple", 3, 180.0)
            db.set_holding("Tesla", 1, 250.0)
            db.remove_holding("Tesla")
            holdings = db.load_holdings()
            self.assertEqual(holdings, {"Apple": 5})

    def test_portfolio_db_snapshots_and_top_mover_reference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "portfolio.db")
            db = stock_tracker.PortfolioDB(db_path)
            db.initialize()
            db.set_holding("Apple", 1, stock_tracker.STOCK_PRICES["Apple"])
            db.record_snapshot(stock_tracker.STOCK_PRICES)
            db.set_holding("Apple", 3, stock_tracker.STOCK_PRICES["Apple"])
            db.record_snapshot(stock_tracker.STOCK_PRICES)
            previous_values = db.get_previous_snapshot_values()
            self.assertEqual(previous_values["Apple"], 180.0)

    def test_portfolio_db_export_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "portfolio.db")
            db = stock_tracker.PortfolioDB(db_path)
            db.initialize()
            db.record_export("txt", "portfolio_summary.txt")
            db.record_export("pdf", "portfolio_summary.pdf")
            history = db.get_export_history(limit=2)
            self.assertEqual(len(history), 2)
            self.assertEqual(history[0]["export_format"], "pdf")
            self.assertEqual(history[1]["export_format"], "txt")

    def test_portfolio_db_clear(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "portfolio.db")
            db = stock_tracker.PortfolioDB(db_path)
            db.initialize()
            db.add_holding("Apple", 4, 180.0)
            db.clear_holdings()
            self.assertEqual(db.load_holdings(), {})


if __name__ == "__main__":
    unittest.main()
