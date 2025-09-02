import matplotlib.pyplot as plt
import pandas as pd
from config import config

def plot_bollinger_bands(df, save_path=None):
    """Creates a professional candlestick chart with Bollinger Bands and signals"""
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot Candlesticks (simplified)
    for i, row in df.iterrows():
        color = 'green' if row['close'] >= row['open'] else 'red'
        # Plot high-low line
        ax.plot([i, i], [row['low'], row['high']], color=color, linewidth=1)
        # Plot open-close body
        body_width = 0.4
        ax.bar(i, abs(row['close']-row['open']), bottom=min(row['open'], row['close']), 
               width=body_width, color=color, alpha=0.7)

    # Plot Bollinger Bands
    ax.plot(df['sma'], label='SMA', color='blue', linewidth=2)
    ax.plot(df['bb_upper'], label='Upper Band', color='orange', linestyle='--')
    ax.plot(df['bb_lower'], label='Lower Band', color='orange', linestyle='--')
    ax.fill_between(df.index, df['bb_upper'], df['bb_lower'], alpha=0.1, color='orange')

    # Plot BUY/SELL signals
    buy_signals = df[df['signal'] == 'BUY']
    sell_signals = df[df['signal'] == 'SELL']
    ax.scatter(buy_signals.index, buy_signals['low'] * 0.999, marker='^', color='green', s=100, label='BUY', zorder=5)
    ax.scatter(sell_signals.index, sell_signals['high'] * 1.001, marker='v', color='red', s=100, label='SELL', zorder=5)

    ax.set_title(f"{config.SYMBOL} - Bollinger Bands Mean Reversion Strategy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=100, bbox_inches='tight')
    plt.show()