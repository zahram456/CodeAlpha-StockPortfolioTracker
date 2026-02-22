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
        prices = {"AAPL": 100.0, "TSLA": 200.0}
        values = iter(["aapl", "2", "AAPL", "3", "TSLA", "1"])

        def fake_input(_):
            return next(values)

        items = stock_tracker.build_portfolio(
            prices, 3, input_fn=fake_input, print_fn=lambda _: None
        )
        as_dict = {item.symbol: item.quantity for item in items}

        self.assertEqual(as_dict["AAPL"], 5)
        self.assertEqual(as_dict["TSLA"], 1)

    def test_build_portfolio_skips_unknown_symbol(self):
        prices = {"AAPL": 100.0}
        values = iter(["XXXX", "AAPL", "2"])

        def fake_input(_):
            return next(values)

        items = stock_tracker.build_portfolio(
            prices, 2, input_fn=fake_input, print_fn=lambda _: None
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].symbol, "AAPL")
        self.assertEqual(items[0].quantity, 2)

    def test_calculate_total_value(self):
        items = [
            stock_tracker.PortfolioItem("AAPL", 2, 100.0),
            stock_tracker.PortfolioItem("TSLA", 1, 250.0),
        ]
        self.assertEqual(stock_tracker.calculate_total_value(items), 450.0)

    def test_generate_summary_lines(self):
        items = [
            stock_tracker.PortfolioItem("AAPL", 2, 100.0),
            stock_tracker.PortfolioItem("TSLA", 1, 250.0),
        ]
        lines = stock_tracker.generate_summary_lines(items, 450.0)
        self.assertIn("AAPL - 2 shares - $200.00", lines)
        self.assertIn("TSLA - 1 shares - $250.00", lines)
        self.assertEqual(lines[-1], "Total Investment Value: $450.00")

    def test_calculate_portfolio_metrics(self):
        items = [
            stock_tracker.PortfolioItem("AAPL", 2, 100.0),
            stock_tracker.PortfolioItem("TSLA", 1, 250.0),
            stock_tracker.PortfolioItem("MSFT", 1, 150.0),
        ]
        metrics = stock_tracker.calculate_portfolio_metrics(items)
        self.assertEqual(metrics["total_value"], 600.0)
        self.assertEqual(metrics["positions"], 3)
        self.assertEqual(metrics["top_symbol"], "TSLA")
        self.assertEqual(metrics["top_value"], 250.0)

    def test_calculate_portfolio_metrics_empty(self):
        metrics = stock_tracker.calculate_portfolio_metrics([])
        self.assertEqual(metrics["total_value"], 0.0)
        self.assertEqual(metrics["positions"], 0)
        self.assertEqual(metrics["top_symbol"], "-")
        self.assertEqual(metrics["top_value"], 0.0)

    def test_save_and_load_portfolio_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "portfolio_data.json")
            quantities = {"AAPL": 5, "TSLA": 2}
            stock_tracker.save_portfolio_json(filename, quantities)
            loaded = stock_tracker.load_portfolio_json(filename)
            self.assertEqual(loaded, quantities)

    def test_load_portfolio_json_filters_bad_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "portfolio_data.json")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(
                    '{"AAPL": 4, "INVALID": 5, "TSLA": -1, "MSFT": "7", "AMZN": 1}'
                )
            loaded = stock_tracker.load_portfolio_json(filename)
            self.assertEqual(loaded, {"AAPL": 4, "AMZN": 1})

    def test_save_summary_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "summary.csv")
            items = [
                stock_tracker.PortfolioItem("AAPL", 2, 100.0),
                stock_tracker.PortfolioItem("TSLA", 1, 250.0),
            ]
            stock_tracker.save_summary_csv(filename, items, 450.0)
            with open(filename, "r", encoding="utf-8", newline="") as file:
                rows = list(csv.reader(file))

            self.assertEqual(rows[0], ["Symbol", "Quantity", "Price", "Position Value"])
            self.assertEqual(rows[1], ["AAPL", "2", "100.00", "200.00"])
            self.assertEqual(rows[2], ["TSLA", "1", "250.00", "250.00"])
            self.assertEqual(rows[4], ["Total Investment Value", "", "", "450.00"])


if __name__ == "__main__":
    unittest.main()
