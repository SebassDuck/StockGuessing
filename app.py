from flask import Flask, jsonify, render_template
import yfinance as yf
from datetime import datetime, timedelta
import random


app = Flask(__name__)

# Extended list of popular stocks with their symbols and names
STOCKS = [
    # Technology
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "AMZN", "name": "Amazon.com Inc."},
    {"symbol": "META", "name": "Meta Platforms Inc."},
    {"symbol": "NVDA", "name": "NVIDIA Corporation"},
    {"symbol": "TSLA", "name": "Tesla Inc."},
    {"symbol": "AVGO", "name": "Broadcom Inc."},
    {"symbol": "ADBE", "name": "Adobe Inc."},
    {"symbol": "CRM", "name": "Salesforce Inc."},
    {"symbol": "AMD", "name": "Advanced Micro Devices"},
    {"symbol": "INTC", "name": "Intel Corporation"},
    {"symbol": "CSCO", "name": "Cisco Systems Inc."},
    {"symbol": "ORCL", "name": "Oracle Corporation"},
    {"symbol": "QCOM", "name": "Qualcomm Inc."},
    
    # Financial Services
    {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
    {"symbol": "V", "name": "Visa Inc."},
    {"symbol": "MA", "name": "Mastercard Inc."},
    {"symbol": "BAC", "name": "Bank of America Corp."},
    {"symbol": "WFC", "name": "Wells Fargo & Co."},
    {"symbol": "MS", "name": "Morgan Stanley"},
    {"symbol": "GS", "name": "Goldman Sachs Group"},
    {"symbol": "BLK", "name": "BlackRock Inc."},
    
    # Healthcare
    {"symbol": "JNJ", "name": "Johnson & Johnson"},
    {"symbol": "UNH", "name": "UnitedHealth Group"},
    {"symbol": "PFE", "name": "Pfizer Inc."},
    {"symbol": "ABBV", "name": "AbbVie Inc."},
    {"symbol": "MRK", "name": "Merck & Co."},
    {"symbol": "LLY", "name": "Eli Lilly & Co."},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific"},
    
    # Consumer Goods & Retail
    {"symbol": "WMT", "name": "Walmart Inc."},
    {"symbol": "PG", "name": "Procter & Gamble Co."},
    {"symbol": "KO", "name": "The Coca-Cola Company"},
    {"symbol": "PEP", "name": "PepsiCo Inc."},
    {"symbol": "COST", "name": "Costco Wholesale"},
    {"symbol": "NKE", "name": "Nike Inc."},
    {"symbol": "MCD", "name": "McDonald's Corporation"},
    {"symbol": "SBUX", "name": "Starbucks Corporation"},
    {"symbol": "TGT", "name": "Target Corporation"},
    
    # Entertainment & Media
    {"symbol": "DIS", "name": "The Walt Disney Company"},
    {"symbol": "NFLX", "name": "Netflix Inc."},
    {"symbol": "CMCSA", "name": "Comcast Corporation"},
    {"symbol": "PARA", "name": "Paramount Global"},
    {"symbol": "WBD", "name": "Warner Bros. Discovery"},
    
    # Telecommunications
    {"symbol": "VZ", "name": "Verizon Communications"},
    {"symbol": "T", "name": "AT&T Inc."},
    {"symbol": "TMUS", "name": "T-Mobile US Inc."},
    
    # Industrial & Manufacturing
    {"symbol": "CAT", "name": "Caterpillar Inc."},
    {"symbol": "BA", "name": "Boeing Company"},
    {"symbol": "GE", "name": "General Electric Co."},
    {"symbol": "HON", "name": "Honeywell International"},
    {"symbol": "MMM", "name": "3M Company"},
    {"symbol": "DE", "name": "Deere & Company"},
    
    # Energy
    {"symbol": "XOM", "name": "Exxon Mobil Corporation"},
    {"symbol": "CVX", "name": "Chevron Corporation"},
    {"symbol": "COP", "name": "ConocoPhillips"},
    
    # Real Estate & Construction
    {"symbol": "HD", "name": "Home Depot Inc."},
    {"symbol": "LOW", "name": "Lowe's Companies"},
    
    # Automotive
    {"symbol": "F", "name": "Ford Motor Company"},
    {"symbol": "GM", "name": "General Motors Company"},
    
    # Airlines
    {"symbol": "AAL", "name": "American Airlines Group"},
    {"symbol": "DAL", "name": "Delta Air Lines Inc."},
    {"symbol": "UAL", "name": "United Airlines Holdings"},
    {"symbol": "LUV", "name": "Southwest Airlines Co."},
    
    # E-commerce & Internet Services
    {"symbol": "PYPL", "name": "PayPal Holdings Inc."},
    {"symbol": "UBER", "name": "Uber Technologies Inc."},
    {"symbol": "ABNB", "name": "Airbnb Inc."},
    {"symbol": "BKNG", "name": "Booking Holdings Inc."},
    
    # Semiconductor Equipment
    {"symbol": "AMAT", "name": "Applied Materials Inc."},
    {"symbol": "KLAC", "name": "KLA Corporation"},
    {"symbol": "LRCX", "name": "Lam Research Corp."},
    
    # Others
    {"symbol": "BRK-B", "name": "Berkshire Hathaway Inc."},
    {"symbol": "UPS", "name": "United Parcel Service"},
    {"symbol": "RTX", "name": "Raytheon Technologies"},
    {"symbol": "NEE", "name": "NextEra Energy Inc."},
    {"symbol": "LIN", "name": "Linde plc"}
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/random-stock')
def get_random_stock():
    try:
        # Pick a random stock from the list
        stock = random.choice(STOCKS)
        
        # Get data for the last 5 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1825)  # 5 years of data
        
        ticker = yf.Ticker(stock["symbol"])
        df = ticker.history(start=start_date, end=end_date, interval='1d')
        
        if len(df) < 20:
            return jsonify({
                'success': False,
                'error': f'Not enough data available for {stock["symbol"]}'
            })
            
        # Select a random 30-day window
        max_start_idx = len(df) - 30
        if max_start_idx <= 0:
            return jsonify({
                'success': False,
                'error': f'Not enough data available for {stock["symbol"]}'
            })
            
        random_start_idx = random.randint(0, max_start_idx)
        window_df = df.iloc[random_start_idx:random_start_idx + 30]
        
        # Get historical data for indicator calculations
        # We need:
        # - 21 days for EMA
        # - 20 days for Bollinger Bands
        lookback_days = 30  # Safety margin for calculations
        historical_start_idx = max(0, random_start_idx - lookback_days)
        historical_df = df.iloc[historical_start_idx:random_start_idx]
        
        # Convert the data to the format needed for TradingView's charts
        candles = []
        historical_candles = []
        
        # Convert historical data
        for index, row in historical_df.iterrows():
            historical_candles.append({
                'time': index.timestamp(),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close'])
            })
        
        # Convert window data
        for index, row in window_df.iterrows():
            candles.append({
                'time': index.timestamp(),
                'open': float(row['Open']),
                'high': float(row['High']),
                'low': float(row['Low']),
                'close': float(row['Close'])
            })
        
        return jsonify({
            'success': True,
            'data': {
                'stock': stock,
                'candles': candles,
                'historicalCandles': historical_candles
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True) 