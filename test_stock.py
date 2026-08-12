#!/usr/bin/env python3
"""Basic tests for stock_profit_loss.py — run by Jenkins on every push."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stock_profit_loss import StockProfitLossAnalyzer


def test_portfolio_names():
    assert 'stocks' in StockProfitLossAnalyzer.PORTFOLIO_NAMES
    assert StockProfitLossAnalyzer.PORTFOLIO_NAMES['stocks'] == 'portfolio1'
    assert StockProfitLossAnalyzer.PORTFOLIO_NAMES['stocks_new'] == 'portfolio2'
    print("✅ test_portfolio_names passed")


def test_date_range():
    analyzer = StockProfitLossAnalyzer.__new__(StockProfitLossAnalyzer)
    analyzer.yaml_file = 'stocks.yaml'
    analyzer.portfolio = []
    analyzer.settings = {}
    analyzer.stock_data = {}
    analyzer.profit_loss_data = {}
    start, end = analyzer.get_date_range()
    assert start < end, "start date must be before end date"
    print("✅ test_date_range passed")


def test_export_path_uses_env_or_home():
    import tempfile, os
    test_dir = tempfile.mkdtemp()
    os.environ['STOCK_MONITOR_DATA'] = test_dir

    analyzer = StockProfitLossAnalyzer.__new__(StockProfitLossAnalyzer)
    analyzer.yaml_file = 'stocks.yaml'
    analyzer.portfolio = []
    analyzer.settings = {}
    analyzer.stock_data = {}
    analyzer.profit_loss_data = {'TEST': {'current_value': 100.0}}

    analyzer.export_daily_total_value()
    expected = os.path.join(test_dir, 'daily_portfolio_value.csv')
    assert os.path.exists(expected), f"Expected file at {expected}"
    print("✅ test_export_path_uses_env_or_home passed")

    del os.environ['STOCK_MONITOR_DATA']


if __name__ == '__main__':
    test_portfolio_names()
    test_date_range()
    test_export_path_uses_env_or_home()
    print("\n✅ All tests passed!")
