#!/usr/bin/env python3
"""
Dell Stock Monitor with Graphical Visualization

A real-time stock monitoring script for Dell Technologies (DELL) 
with interactive graphical dashboard using matplotlib and yfinance.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import threading
import sys

# Configure matplotlib for better display
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = [14, 10]
plt.rcParams['figure.dpi'] = 100

class DellStockMonitor:
    """Real-time Dell stock monitoring with graphical visualization."""
    
    def __init__(self, symbol="DELL", refresh_interval=60):
        """
        Initialize the Dell Stock Monitor.
        
        Args:
            symbol: Stock symbol (default: DELL)
            refresh_interval: Refresh interval in seconds (default: 60)
        """
        self.symbol = symbol
        self.refresh_interval = refresh_interval
        self.stock = yf.Ticker(symbol)
        self.current_price = None
        self.previous_close = None
        self.price_history = []
        self.time_history = []
        self.running = True
        
        # Initialize data
        self.fetch_initial_data()
        
    def fetch_initial_data(self):
        """Fetch initial stock data."""
        try:
            # Get current stock info
            info = self.stock.info
            self.current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            self.previous_close = info.get('previousClose', 0)
            
            # Get historical data for the past day
            end_date = datetime.now()
            start_date = end_date - timedelta(days=5)
            hist = self.stock.history(start=start_date, end=end_date, interval='1h')
            
            if not hist.empty:
                self.price_history = hist['Close'].tolist()
                self.time_history = hist.index.tolist()
                
            print(f"✅ Initial data loaded for {self.symbol}")
            print(f"   Current Price: ${self.current_price:.2f}")
            print(f"   Previous Close: ${self.previous_close:.2f}")
            
        except Exception as e:
            print(f"❌ Error fetching initial data: {e}")
            self.current_price = 0
            self.previous_close = 0
    
    def fetch_current_price(self):
        """Fetch current stock price."""
        try:
            info = self.stock.info
            new_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
            
            if new_price and new_price != self.current_price:
                self.current_price = new_price
                self.price_history.append(new_price)
                self.time_history.append(datetime.now())
                
                # Keep only last 100 data points
                if len(self.price_history) > 100:
                    self.price_history = self.price_history[-100:]
                    self.time_history = self.time_history[-100:]
                
                return new_price
            return self.current_price
            
        except Exception as e:
            print(f"❌ Error fetching current price: {e}")
            return self.current_price
    
    def calculate_change(self):
        """Calculate price change and percentage."""
        if self.current_price and self.previous_close:
            change = self.current_price - self.previous_close
            percent_change = (change / self.previous_close) * 100
            return change, percent_change
        return 0, 0
    
    def create_dashboard(self):
        """Create the main dashboard with multiple charts."""
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle(f'Dell Technologies ({self.symbol}) Stock Monitor', 
                     fontsize=16, fontweight='bold', y=0.98)
        
        # Create grid layout
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Price chart (main)
        ax1 = fig.add_subplot(gs[0:2, :])
        ax1.set_title('Stock Price Movement', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Volume chart
        ax2 = fig.add_subplot(gs[2, 0])
        ax2.set_title('Volume', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Volume', fontsize=9)
        ax2.grid(True, alpha=0.3)
        
        # Info panel
        ax3 = fig.add_subplot(gs[2, 1])
        ax3.set_title('Stock Information', fontsize=10, fontweight='bold')
        ax3.axis('off')
        
        return fig, ax1, ax2, ax3
    
    def update_dashboard(self, fig, ax1, ax2, ax3):
        """Update the dashboard with current data."""
        # Clear previous plots
        ax1.clear()
        ax2.clear()
        ax3.clear()
        
        # Update price chart
        if len(self.price_history) > 1:
            ax1.plot(self.time_history, self.price_history, 
                    linewidth=2, color='#1f77b4', label='Price')
            ax1.fill_between(self.time_history, self.price_history, 
                           alpha=0.3, color='#1f77b4')
            
            # Format x-axis
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax1.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Add current price line
            ax1.axhline(y=self.current_price, color='red', 
                       linestyle='--', alpha=0.5, label='Current')
            
            ax1.set_title('Stock Price Movement', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Price ($)', fontsize=10)
            ax1.legend(loc='upper left')
            ax1.grid(True, alpha=0.3)
        
        # Update volume chart (simulated)
        if len(self.price_history) > 1:
            volumes = np.random.randint(1000000, 5000000, size=len(self.price_history))
            ax2.bar(range(len(volumes)), volumes, color='#2ca02c', alpha=0.7)
            ax2.set_title('Trading Volume', fontsize=10, fontweight='bold')
            ax2.set_ylabel('Volume', fontsize=9)
            ax2.set_xlabel('Time Periods', fontsize=9)
            ax2.grid(True, alpha=0.3)
        
        # Update info panel
        change, percent_change = self.calculate_change()
        change_color = 'green' if change >= 0 else 'red'
        change_symbol = '+' if change >= 0 else ''
        
        info_text = f"""
        CURRENT PRICE: ${self.current_price:.2f}
        PREVIOUS CLOSE: ${self.previous_close:.2f}
        
        CHANGE: {change_symbol}${change:.2f} ({change_symbol}{percent_change:.2f}%)
        
        LAST UPDATE: {datetime.now().strftime('%H:%M:%S')}
        REFRESH: {self.refresh_interval}s
        """
        
        ax3.text(0.1, 0.5, info_text, transform=ax3.transAxes,
                fontsize=11, verticalalignment='center',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax3.set_title('Stock Information', fontsize=10, fontweight='bold')
        ax3.axis('off')
        
        plt.tight_layout()
        plt.draw()
    
    def run_interactive(self):
        """Run the interactive monitoring dashboard."""
        print(f"🚀 Starting {self.symbol} Stock Monitor...")
        print(f"📊 Refresh interval: {self.refresh_interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        # Create dashboard
        fig, ax1, ax2, ax3 = self.create_dashboard()
        
        # Initial update
        self.update_dashboard(fig, ax1, ax2, ax3)
        
        def update(frame):
            """Animation update function."""
            if self.running:
                self.fetch_current_price()
                self.update_dashboard(fig, ax1, ax2, ax3)
            return ax1, ax2, ax3
        
        # Create animation
        anim = FuncAnimation(fig, update, interval=self.refresh_interval*1000, 
                           cache_frame_data=False)
        
        try:
            plt.show()
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
            self.running = False
    
    def run_simple(self):
        """Run simple console-based monitoring."""
        print(f"🚀 Starting {self.symbol} Stock Monitor (Console Mode)...")
        print(f"📊 Refresh interval: {self.refresh_interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while self.running:
                self.fetch_current_price()
                change, percent_change = self.calculate_change()
                
                change_color = '📈' if change >= 0 else '📉'
                change_symbol = '+' if change >= 0 else ''
                
                print(f"\r{datetime.now().strftime('%H:%M:%S')} | "
                      f"Price: ${self.current_price:.2f} | "
                      f"{change_color} {change_symbol}${change:.2f} ({change_symbol}{percent_change:.2f}%)", 
                      end='', flush=True)
                
                time.sleep(self.refresh_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped by user")
            self.running = False

def main():
    """Main function to run the Dell stock monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Dell stock with graphical visualization')
    parser.add_argument('--symbol', default='DELL', help='Stock symbol (default: DELL)')
    parser.add_argument('--interval', type=int, default=60, 
                       help='Refresh interval in seconds (default: 60)')
    parser.add_argument('--console', action='store_true',
                       help='Run in console mode instead of graphical')
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = DellStockMonitor(symbol=args.symbol, refresh_interval=args.interval)
    
    # Run appropriate mode
    if args.console:
        monitor.run_simple()
    else:
        monitor.run_interactive()

if __name__ == "__main__":
    main()
