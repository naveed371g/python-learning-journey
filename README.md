# Python Portfolio Projects

Welcome to my Python portfolio! This repository showcases my skills in financial analysis, data visualization, and automation.

## 🚀 Projects

### 1. Stock Portfolio Profit/Loss Analyzer
**File:** `stock_profit_loss.py`

A comprehensive stock portfolio analysis tool that:
- Fetches real-time stock data using Yahoo Finance API
- Calculates daily profit/loss for multiple stocks
- Generates detailed summary tables with color coding
- Creates interactive charts for portfolio visualization
- Exports data to CSV for further analysis
- **NEW:** Weekly profit/loss calculations (Monday to current day)

**Technologies Used:**
- Python 3.x
- yfinance (stock data)
- pandas (data manipulation)
- matplotlib (visualization)
- tabulate (formatted tables)

**Features:**
- Multi-stock portfolio support via YAML configuration
- Day-over-day comparison with total changes
- Weekly performance tracking
- Professional output with color coding
- Chart generation and CSV export

### 2. Dell Stock Monitor
**File:** `dell_stock_monitor.py`

Real-time stock monitoring and alerting system for Dell Technologies.

**Features:**
- Live price tracking
- Price change alerts
- Historical data analysis
- Performance metrics

### 3. Python Learning Examples
**File:** `python_examples_collection.py`

Comprehensive collection of Python examples demonstrating:
- Variables and data types
- Control flow (if/else, loops)
- String operations and math functions
- Practice exercises and mini-projects

Perfect for beginners learning Python programming.

## 🛠️ Installation & Usage

### Prerequisites
```bash
pip install yfinance pandas matplotlib tabulate pyyaml
```

### Running the Stock Analyzer
```bash
python3 stock_profit_loss.py
```

### Configuration
Create a `stocks.yaml` file:
```yaml
portfolio:
  - symbol: "AAPL"
    shares: 10
    purchase_price: 150.00
  - symbol: "TSLA"
    shares: 5
    purchase_price: 200.00

settings:
  currency: "USD"
```

## 📊 Sample Output

The analyzer generates:
- Portfolio summary tables
- Daily profit/loss comparisons
- **Weekly performance tracking**
- Interactive charts
- CSV data exports

## 🎯 Skills Demonstrated

- **Python Programming:** Advanced concepts, OOP, error handling
- **Financial Analysis:** Stock calculations, portfolio management
- **Data Visualization:** Matplotlib charts, formatted tables
- **API Integration:** yfinance for real-time data
- **File Processing:** YAML configuration, CSV exports
- **Problem Solving:** Complex financial calculations and logic

## 🔗 Contact & Connect

- **LinkedIn:** [Your LinkedIn Profile]
- **Email:** [Your Email]
- **GitHub:** [Your GitHub Profile]

---

*Built with passion for financial technology and data analysis*
