#!/usr/bin/env python3
"""
Stock Portfolio Profit/Loss Analyzer

Reads stock portfolio from YAML file and calculates daily profit/loss
for each stock over a specified time period.
"""

import yfinance as yf
import yaml
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tabulate import tabulate
import argparse
import sys

# NOTE: matplotlib is imported lazily inside plot_profit_loss_chart() so that
# importing this module (e.g. from the web app) does not pull in matplotlib and
# trigger its slow font-cache build. It is only needed for chart generation.


class StockProfitLossAnalyzer:
    """Analyze profit/loss for stock portfolio from YAML configuration."""

    def __init__(self, yaml_file='stocks.yaml'):
        """
        Initialize analyzer with YAML configuration.

        Args:
            yaml_file: Path to YAML configuration file
        """
        self.yaml_file = yaml_file
        self.portfolio = []
        self.settings = {}
        self.stock_data = {}
        self.profit_loss_data = {}

        # Load configuration
        self.load_config()

    def load_config(self):
        """Load stock portfolio and settings from YAML file."""
        try:
            with open(self.yaml_file, 'r') as f:
                config = yaml.safe_load(f)

            self.portfolio = config.get('portfolio', [])
            self.settings = config.get('settings', {})

            print(
                f"✅ Loaded {len(self.portfolio)} stocks from {self.yaml_file}")

        except FileNotFoundError:
            print(f"❌ Error: File {self.yaml_file} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            sys.exit(1)

    def get_date_range(self):
        """Calculate date range for analysis (get last 10 trading days to ensure we have a full week of data)."""
        # Get 10 days to ensure we have at least a full week of trading days (accounting for weekends/holidays)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=10)

        # Set end_date to end of today to include today's data
        end_date = end_date.replace(hour=23, minute=59, second=59)

        return start_date, end_date

    def fetch_stock_data(self):
        """Fetch historical stock data for all stocks in portfolio."""
        start_date, end_date = self.get_date_range()

        print(
            f"📊 Fetching stock data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

        for stock in self.portfolio:
            symbol = stock['symbol']
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='10d')

                if not hist.empty:
                    self.stock_data[symbol] = hist
                    print(f"   ✅ {symbol}: {len(hist)} days of data")
                else:
                    print(f"   ❌ {symbol}: No data available")

            except Exception as e:
                print(f"   ❌ {symbol}: Error fetching data - {e}")

    def calculate_daily_profit_loss(self):
        """Calculate daily profit/loss for each stock."""
        print(f"\n💰 Calculating daily profit/loss...")

        for stock in self.portfolio:
            symbol = stock['symbol']
            shares = stock['shares']
            purchase_price = stock['purchase_price']

            if symbol not in self.stock_data:
                continue

            hist = self.stock_data[symbol]

            # Calculate daily profit/loss
            daily_pnl = []
            daily_values = []

            for date, row in hist.iterrows():
                current_price = row['Close']
                daily_value = current_price * shares
                daily_pl = (current_price - purchase_price) * shares
                daily_pl_percent = (
                    (current_price - purchase_price) / purchase_price) * 100

                daily_pnl.append({
                    'date': date,
                    'price': current_price,
                    'value': daily_value,
                    'profit_loss': daily_pl,
                    'profit_loss_percent': daily_pl_percent
                })
                daily_values.append(daily_value)

            self.profit_loss_data[symbol] = {
                'symbol': symbol,
                'shares': shares,
                'purchase_price': purchase_price,
                'daily_pnl': daily_pnl,
                'daily_values': daily_values,
                'current_price': hist['Close'].iloc[-1],
                'current_value': daily_values[-1],
                'total_profit_loss': daily_pnl[-1]['profit_loss'],
                'total_profit_loss_percent': daily_pnl[-1]['profit_loss_percent']
            }

            print(
                f"   ✅ {symbol}: ${daily_pnl[-1]['profit_loss']:,.2f} ({daily_pnl[-1]['profit_loss_percent']:.2f}%)")

    def calculate_weekly_change(self):
        """Calculate weekly change (Monday to current day) for all stocks."""
        print(f"\n📅 Calculating weekly change (Monday to current day)...")

        total_weekly_change = 0
        weekly_data = {}
        current_date = datetime.now()

        for symbol, data in self.profit_loss_data.items():
            daily_pnl = data['daily_pnl']

            if len(daily_pnl) < 2:
                continue

            # Find Monday of the current week
            monday_data = None
            current_day_data = None

            # Get current week's Monday
            days_since_monday = current_date.weekday()  # 0=Monday, 4=Friday
            current_week_monday = current_date - \
                timedelta(days=days_since_monday)

            # Find Monday data in current week
            for day in daily_pnl:
                day_date = day['date']
                if day_date.weekday() == 0 and day_date.date() >= current_week_monday.date():
                    monday_data = day
                    break

            # Find the most recent data (current day or latest available)
            current_day_data = daily_pnl[-1]

            # If no Monday found in current week, use the earliest day in data
            if not monday_data:
                monday_data = daily_pnl[0]

            # Calculate weekly change from Monday to current day
            weekly_change = current_day_data['profit_loss'] - \
                monday_data['profit_loss']
            weekly_percent_change = current_day_data['profit_loss_percent'] - \
                monday_data['profit_loss_percent']

            weekly_data[symbol] = {
                'weekly_change': weekly_change,
                'weekly_percent_change': weekly_percent_change,
                'monday_date': monday_data['date'],
                'current_date': current_day_data['date'],
                'is_full_week': current_date.weekday() >= 4  # Friday or later
            }

            total_weekly_change += weekly_change

            # Determine week status for display
            if current_date.weekday() >= 4:  # Friday or weekend
                week_status = "Full Week"
            else:
                week_status = f"Week to {current_date.strftime('%A')}"

            print(
                f"   ✅ {symbol}: ${weekly_change:,.2f} ({weekly_percent_change:+.2f}%) - {week_status}")

        self.weekly_data = weekly_data
        return total_weekly_change

    def generate_weekly_change_table(self):
        """Generate weekly change table for all stocks."""
        if not hasattr(self, 'weekly_data'):
            return

        current_date = datetime.now()

        # Determine table title based on current day
        if current_date.weekday() >= 4:  # Friday or weekend
            table_title = "📊 TOTAL WEEKLY CHANGE ACROSS ALL STOCKS (Monday to Friday)"
        else:
            table_title = f"📊 TOTAL WEEKLY CHANGE ACROSS ALL STOCKS (Monday to {current_date.strftime('%A')})"

        print(f"\n{table_title}")
        print("=" * 80)

        # ANSI color codes
        GREEN = '\033[92m'
        RED = '\033[91m'
        RESET = '\033[0m'

        weekly_summary = []
        total_weekly_change = 0

        for symbol, data in self.weekly_data.items():
            weekly_change = data['weekly_change']
            weekly_percent = data['weekly_percent_change']

            total_weekly_change += weekly_change

            # Color coding
            color = GREEN if weekly_change >= 0 else RED
            emoji = '📈' if weekly_change >= 0 else '📉'

            weekly_summary.append([
                symbol,
                data['monday_date'].strftime('%Y-%m-%d'),
                data['current_date'].strftime('%Y-%m-%d'),
                f"{color}{emoji} ${weekly_change:,.2f}{RESET}",
                f"{color}{weekly_percent:+.2f}%{RESET}"
            ])

        # Add total row
        total_color = GREEN if total_weekly_change >= 0 else RED
        total_emoji = '📈' if total_weekly_change >= 0 else '📉'

        weekly_summary.append([
            'TOTAL',
            '-',
            '-',
            f"{total_color}{total_emoji} ${total_weekly_change:,.2f}{RESET}",
            f"{total_color}{(total_weekly_change/abs(total_weekly_change)*100 if total_weekly_change != 0 else 0):+.2f}%{RESET}"
        ])

        # Determine headers based on current day
        if current_date.weekday() >= 4:  # Friday or weekend
            headers = ['Symbol', 'Monday', 'Friday', 'Weekly P/L', 'Weekly %']
        else:
            headers = ['Symbol', 'Monday', current_date.strftime(
                '%A'), 'Weekly P/L', 'Weekly %']

        print(tabulate(weekly_summary, headers=headers, tablefmt='grid'))

        # Add week status information
        if current_date.weekday() < 4:  # Monday to Thursday
            print(f"\n📅 Week Status: Trading week in progress")
            print(
                f"   Current date: {current_date.strftime('%Y-%m-%d')} ({current_date.strftime('%A')})")
            print(f"   Week ends: Friday")
        elif current_date.weekday() == 4:  # Friday
            print(f"\n📅 Week Status: Trading week complete!")
            print(
                f"   Current date: {current_date.strftime('%Y-%m-%d')} ({current_date.strftime('%A')})")
        else:  # Weekend
            print(f"\n📅 Week Status: Weekend - Trading week complete")
            print(
                f"   Current date: {current_date.strftime('%Y-%m-%d')} ({current_date.strftime('%A')})")

    def generate_summary_table(self):
        """Generate summary table of profit/loss for all stocks."""
        print(f"\n📈 Portfolio Summary")
        print("=" * 80)

        summary_data = []
        total_investment = 0
        total_current_value = 0
        total_profit_loss = 0

        for symbol, data in self.profit_loss_data.items():
            investment = data['shares'] * data['purchase_price']
            current_value = data['current_value']
            profit_loss = data['total_profit_loss']
            profit_loss_percent = data['total_profit_loss_percent']

            total_investment += investment
            total_current_value += current_value
            total_profit_loss += profit_loss

            pl_color = '📈' if profit_loss >= 0 else '📉'

            summary_data.append([
                symbol,
                data['shares'],
                f"${data['purchase_price']:.2f}",
                f"${investment:,.2f}",
                f"${data['current_price']:.2f}",
                f"${current_value:,.2f}",
                f"{pl_color} ${profit_loss:,.2f}",
                f"{profit_loss_percent:.2f}%"
            ])

        # Add total row
        total_pl_percent = (total_profit_loss / total_investment) * \
            100 if total_investment > 0 else 0
        total_pl_color = '📈' if total_profit_loss >= 0 else '📉'

        summary_data.append([
            'TOTAL',
            '-',
            '-',
            f"${total_investment:,.2f}",
            '-',
            f"${total_current_value:,.2f}",
            f"{total_pl_color} ${total_profit_loss:,.2f}",
            f"{total_pl_percent:.2f}%"
        ])

        headers = ['Symbol', 'Shares', 'Purchase Price', 'Investment', 'Current Price',
                   'Current Value', 'Profit/Loss', '% Change']

        print(tabulate(summary_data, headers=headers, tablefmt='grid'))

        return summary_data

    def generate_daily_profit_loss_table(self):
        """Generate day-over-day profit/loss comparison for each stock."""
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(f"\n📅 Day-over-Day Comparison (as of {current_date})")
        print("=" * 80)

        # ANSI color codes
        GREEN = '\033[92m'
        RED = '\033[91m'
        RESET = '\033[0m'

        # Track totals for all stocks
        total_daily_price_change = 0
        total_daily_value_change = 0
        total_daily_pl_change = 0

        for symbol, data in self.profit_loss_data.items():
            print(
                f"\n{symbol} ({data['shares']} shares @ ${data['purchase_price']:.2f})")
            print("-" * 80)

            if len(data['daily_pnl']) >= 2:
                # Get last 2 trading days (accounting for weekends/holidays)
                previous_day = data['daily_pnl'][-2]
                latest_trading_day = data['daily_pnl'][-1]

                # Calculate day-over-day change
                daily_change = latest_trading_day['price'] - \
                    previous_day['price']
                daily_change_percent = (
                    daily_change / previous_day['price']) * 100 if previous_day['price'] > 0 else 0

                daily_pl_color = '📈' if daily_change >= 0 else '📉'
                total_pl_color = '📈' if latest_trading_day['profit_loss'] >= 0 else '📉'

                # Colorize daily change values
                color_change = GREEN if daily_change >= 0 else RED
                color_value_change = GREEN if (
                    latest_trading_day['value'] - previous_day['value']) >= 0 else RED
                color_pl_change = GREEN if (
                    latest_trading_day['profit_loss'] - previous_day['profit_loss']) >= 0 else RED
                color_percent = GREEN if daily_change_percent >= 0 else RED

                # Use actual trading dates, not "Today"
                comparison_data = [
                    ['Previous Trading Day', previous_day['date'].strftime('%Y-%m-%d'), data['shares'],
                     f"${previous_day['price']:.2f}", f"${previous_day['value']:,.2f}",
                     f"{total_pl_color} ${previous_day['profit_loss']:,.2f}", f"{previous_day['profit_loss_percent']:.2f}%"],
                    ['Latest Trading Day', latest_trading_day['date'].strftime('%Y-%m-%d'), data['shares'],
                     f"${latest_trading_day['price']:.2f}", f"${latest_trading_day['value']:,.2f}",
                     f"{total_pl_color} ${latest_trading_day['profit_loss']:,.2f}", f"{latest_trading_day['profit_loss_percent']:.2f}%"],
                    ['Daily Change', '-', '-',
                     f"{color_change}{daily_pl_color} ${daily_change:.2f}{RESET}",
                     f"{color_value_change}{daily_pl_color} ${latest_trading_day['value'] - previous_day['value']:,.2f}{RESET}",
                     f"{color_pl_change}{daily_pl_color} ${latest_trading_day['profit_loss'] - previous_day['profit_loss']:,.2f}{RESET}",
                     f"{color_percent}{daily_change_percent:.2f}%{RESET}"]
                ]

                headers = ['Period', 'Date', 'Shares',
                           'Price', 'Value', 'Total P/L', '% Change']
                print(tabulate(comparison_data, headers=headers, tablefmt='grid'))

                # Accumulate totals
                total_daily_price_change += daily_change
                total_daily_value_change += (
                    latest_trading_day['value'] - previous_day['value'])
                total_daily_pl_change += (
                    latest_trading_day['profit_loss'] - previous_day['profit_loss'])
            else:
                print("Not enough data for comparison")

        # Print total daily change summary
        print(f"\n" + "=" * 80)
        print(f"📊 TOTAL DAILY CHANGE ACROSS ALL STOCKS")
        print("=" * 80)

        total_color = GREEN if total_daily_value_change >= 0 else RED
        total_pl_color = GREEN if total_daily_pl_change >= 0 else RED
        total_emoji = '📈' if total_daily_value_change >= 0 else '📉'

        total_data = [
            ['Total Price Change',
                f"{total_color}{total_emoji} ${total_daily_price_change:.2f}{RESET}"],
            ['Total Value Change',
                f"{total_color}{total_emoji} ${total_daily_value_change:,.2f}{RESET}"],
            ['Total P/L Change',
                f"{total_pl_color}{total_emoji} ${total_daily_pl_change:,.2f}{RESET}"]
        ]

        print(tabulate(total_data, headers=[
              'Metric', 'Value'], tablefmt='grid'))

    def plot_profit_loss_chart(self):
        """Create profit/loss chart for all stocks."""
        import matplotlib.pyplot as plt

        # Configure matplotlib (done here to keep import lazy)
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.rcParams['figure.figsize'] = [14, 8]
        plt.rcParams['figure.dpi'] = 100

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

        # Plot 1: Daily profit/loss over time
        for symbol, data in self.profit_loss_data.items():
            dates = [day['date'] for day in data['daily_pnl']]
            pnl = [day['profit_loss'] for day in data['daily_pnl']]
            ax1.plot(dates, pnl, label=symbol, linewidth=2)

        ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax1.set_title('Daily Profit/Loss by Stock',
                      fontsize=14, fontweight='bold')
        ax1.set_ylabel('Profit/Loss ($)', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # Plot 2: Portfolio value over time
        portfolio_values = []
        dates = None

        # Calculate total portfolio value for each day
        if self.profit_loss_data:
            first_symbol = list(self.profit_loss_data.keys())[0]
            dates = [day['date']
                     for day in self.profit_loss_data[first_symbol]['daily_pnl']]

            for i, date in enumerate(dates):
                total_value = 0
                for symbol, data in self.profit_loss_data.items():
                    if i < len(data['daily_pnl']):
                        total_value += data['daily_pnl'][i]['value']
                portfolio_values.append(total_value)

        if dates and portfolio_values:
            ax2.plot(dates, portfolio_values, linewidth=3,
                     color='darkblue', label='Total Portfolio')
            ax2.fill_between(dates, portfolio_values,
                             alpha=0.3, color='darkblue')
            ax2.set_title('Total Portfolio Value Over Time',
                          fontsize=14, fontweight='bold')
            ax2.set_ylabel('Portfolio Value ($)', fontsize=12)
            ax2.legend(loc='upper left')
            ax2.grid(True, alpha=0.3)
            ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('stock_profit_loss_chart.png',
                    dpi=150, bbox_inches='tight')
        print(f"\n📊 Chart saved as 'stock_profit_loss_chart.png'")
        plt.show()

    def export_to_csv(self):
        """Export profit/loss data to CSV file."""
        all_data = []

        for symbol, data in self.profit_loss_data.items():
            for day in data['daily_pnl']:
                all_data.append({
                    'Symbol': symbol,
                    'Date': day['date'].strftime('%Y-%m-%d'),
                    'Shares': data['shares'],
                    'Price': day['price'],
                    'Value': day['value'],
                    'Profit_Loss': day['profit_loss'],
                    'Profit_Loss_Percent': day['profit_loss_percent']
                })

        df = pd.DataFrame(all_data)
        df.to_csv('stock_profit_loss.csv', index=False)
        print(f"📄 Data exported to 'stock_profit_loss.csv'")

    # Map each YAML config to a friendly portfolio name for monitoring
    PORTFOLIO_NAMES = {
        'stocks': 'portfolio1',
        'stocks_new': 'portfolio2',
    }

    def export_daily_total_value(
        self,
        csv_file=None
    ):
        """Record today's total Current Value into a daily monitoring table.

        The CSV is a wide table: one row per day, one column per portfolio
        (portfolio1, portfolio2). If the script runs multiple times in the
        same day, that day's value for the portfolio is overwritten.
        """
        import os
        if csv_file is None:
            base_dir = os.environ.get(
                'STOCK_MONITOR_DATA', os.path.expanduser('~'))
            csv_file = os.path.join(base_dir, 'daily_portfolio_value.csv')

        # Compute total current value from the Portfolio Summary data
        total_current_value = round(sum(
            data['current_value'] for data in self.profit_loss_data.values()
        ), 2)

        # Friendly portfolio name (falls back to the YAML file stem)
        stem = os.path.splitext(os.path.basename(self.yaml_file))[0]
        portfolio_name = self.PORTFOLIO_NAMES.get(stem, stem)
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

        # Companion machine-readable data file used to reliably update values
        data_file = os.path.join(
            os.path.dirname(csv_file), '.daily_portfolio_value.data.csv')

        # Load existing data if present
        if os.path.exists(data_file):
            df = pd.read_csv(data_file)
        else:
            df = pd.DataFrame(columns=['Date'])

        # Ensure required columns exist
        for col in (portfolio_name, 'Last_Updated'):
            if col not in df.columns:
                df[col] = pd.NA

        # Update today's row (create it if it doesn't exist), overwriting value
        if today in df['Date'].values:
            df.loc[df['Date'] == today, portfolio_name] = total_current_value
            df.loc[df['Date'] == today, 'Last_Updated'] = timestamp
        else:
            new_row = {col: pd.NA for col in df.columns}
            new_row['Date'] = today
            new_row[portfolio_name] = total_current_value
            new_row['Last_Updated'] = timestamp
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Keep column order stable: Date, portfolios (sorted), then Last_Updated
        portfolio_cols = sorted(
            [c for c in df.columns if c not in ('Date', 'Last_Updated')])
        df = df[['Date'] + portfolio_cols + ['Last_Updated']]
        df = df.sort_values('Date').reset_index(drop=True)

        # Persist raw data (companion file) and the visual grid table (main file)
        df.to_csv(data_file, index=False)

        # Build the display table with a weekday name column after Date
        display_df = df.copy()
        display_df.insert(
            1, 'Day', pd.to_datetime(display_df['Date']).dt.strftime('%A'))
        table_str = tabulate(display_df, headers='keys', tablefmt='grid',
                             showindex=False, floatfmt=',.2f')
        with open(csv_file, 'w') as f:
            f.write(table_str + '\n')

        print(
            f"📄 Daily monitoring table updated ({portfolio_name}: ${total_current_value:,.2f}) at '{csv_file}'")
        print(table_str)

    def run_analysis(self, show_chart=True, export_csv=True):
        """Run complete profit/loss analysis."""
        print("🚀 Starting Stock Portfolio Profit/Loss Analysis")
        print("=" * 80)

        # Fetch data
        self.fetch_stock_data()

        if not self.stock_data:
            print("❌ No stock data available. Exiting.")
            return

        # Calculate profit/loss
        self.calculate_daily_profit_loss()

        if not self.profit_loss_data:
            print("❌ No profit/loss data calculated. Exiting.")
            return

        # Calculate weekly change
        self.calculate_weekly_change()

        # Generate reports
        self.generate_summary_table()
        self.generate_weekly_change_table()
        self.generate_daily_profit_loss_table()

        # Optional: Generate chart and export
        if show_chart:
            self.plot_profit_loss_chart()

        if export_csv:
            self.export_to_csv()

        # Always record the daily total current value (one row per day per portfolio)
        self.export_daily_total_value()

        print(f"\n✅ Analysis complete!")


def main():
    """Main function to run stock profit/loss analyzer."""
    parser = argparse.ArgumentParser(
        description='Analyze stock portfolio profit/loss from YAML file')
    parser.add_argument('--yaml', default='stocks.yaml',
                        help='Path to YAML configuration file')
    parser.add_argument('--no-chart', action='store_true',
                        help='Skip chart generation')
    parser.add_argument('--no-csv', action='store_true',
                        help='Skip CSV export')

    args = parser.parse_args()

    # Install required packages if needed
    try:
        import tabulate
    except ImportError:
        print("Installing required package: tabulate")
        import subprocess
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '--user', 'tabulate'])

    # Run analysis
    analyzer = StockProfitLossAnalyzer(yaml_file=args.yaml)
    analyzer.run_analysis(show_chart=not args.no_chart,
                          export_csv=not args.no_csv)


if __name__ == "__main__":
    main()
