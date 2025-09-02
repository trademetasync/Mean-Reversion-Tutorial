import pandas as pd
import numpy as np
from config import config

class BollingerBandsStrategy:
    def __init__(self):
        self.period = config.BB_PERIOD
        self.deviation = config.BB_DEVIATION

    def calculate_bollinger_bands(self, df):
        """Calculates SMA, Upper Band, and Lower Band"""
        df = df.copy()
        df['sma'] = df['close'].rolling(window=self.period).mean()
        df['std'] = df['close'].rolling(window=self.period).std()
        df['bb_upper'] = df['sma'] + (self.deviation * df['std'])
        df['bb_lower'] = df['sma'] - (self.deviation * df['std'])
        return df

    def generate_signals(self, df):
        """Generates BUY/SELL signals based on band touches"""
        df = df.copy()
        df['signal'] = 'HOLD'  # Default: no action

        # Only analyze where we have calculated bands
        valid_data = df['bb_upper'].notna()
        
        for i in range(len(df)):
            if not valid_data.iloc[i]:
                continue
                
            close = df['close'].iloc[i]
            upper = df['bb_upper'].iloc[i]
            lower = df['bb_lower'].iloc[i]
            
            # BUY if price touches or crosses below lower band
            if close <= lower:
                df.loc[i, 'signal'] = 'BUY'
            # SELL if price touches or crosses above upper band
            elif close >= upper:
                df.loc[i, 'signal'] = 'SELL'
                
        return df

    def get_latest_signal(self, df):
        """Returns the most recent signal from the data"""
        if df.empty:
            return 'HOLD', {}
        latest = df.iloc[-1]
        return latest['signal'], latest

# Global strategy instance
strategy = BollingerBandsStrategy()