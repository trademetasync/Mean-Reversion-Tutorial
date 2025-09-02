from datetime import datetime, timedelta
import time
from config import config
from utils import client
from strategy import strategy
from visualization import plot_bollinger_bands

def run_bot():
    print("🤖 Starting Mean Reversion Bot...")
    print(f"API Key: {config.RAPIDAPI_KEY[:10]}...")  # Show first 10 chars for verification
    
    # 1. Fetch historical data (CORRECT date format)
    print("📊 Fetching market data...")
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=48)
    
    # CORRECT: Use the exact format expected by the API
    date_from = start_time.strftime("%Y-%m-%d %H:%M:%S")
    date_to = end_time.strftime("%Y-%m-%d %H:%M:%S")
    
    df = client.get_ohlc_data(
        config.SYMBOL, 
        config.TIMEFRAME,
        date_from,
        date_to
    )
    
    if df is None or df.empty:
        print("❌ Failed to get OHLC data. Possible issues:")
        print("   - Check your RAPIDAPI_KEY in .env file")
        print("   - Verify the API key is active on RapidAPI")
        print("   - Check API documentation for correct parameter formats")
        return

    # Rest of the code remains the same...
    print("📈 Calculating Bollinger Bands...")
    df_with_bb = strategy.calculate_bollinger_bands(df)
    df_with_signals = strategy.generate_signals(df_with_bb)
    
    print("📊 Generating chart...")
    plot_bollinger_bands(df_with_signals, "trading_chart.png")
    
    latest_signal, details = strategy.get_latest_signal(df_with_signals)
    print(f"🎯 Latest Signal: {latest_signal}")
    print(f"   Price: {details.get('close', 'N/A'):.5f}")

if __name__ == "__main__":
    run_bot()