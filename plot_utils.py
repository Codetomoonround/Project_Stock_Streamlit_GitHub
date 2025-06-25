import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc

def plot_chart(df, symbol):
    df["time_num"] = df["time"].map(mdates.date2num)
    fig, axs = plt.subplots(4, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1, 1, 1]})
    ax1, ax2, ax3, ax4 = axs

    candlestick_ohlc(ax1, df[['time_num', 'open', 'high', 'low', 'close']].values, width=0.6, colorup='g', colordown='r')
    ax1.plot(df["time_num"], df["MA20"], label="MA20", color="blue")
    ax1.plot(df["time_num"], df["MA50"], label="MA50", color="orange")
    ax1.plot(df["time_num"], df["MA100"], label="MA100", color="purple")
    ax1.set_title(f"{symbol} – Đến {df['time'].iloc[-1].date()}")
    ax1.legend()

    df["volume_MA20"] = df["volume"].rolling(window=20).mean()
    ax2.plot(df["time_num"], df["volume_MA20"], color="green", label="MA20_volume", linewidth=1.5)
    ax2.bar(df["time_num"], df["volume"], color="blue")
    ax2.set_title("Khối lượng giao dịch")

    ax3.plot(df["time_num"], df["RSI14"], label="RSI14", color="blue")
    ax3.plot(df["time_num"], df["MFI14"], label="MFI14", color="orange")
    ax3.axhline(70, color='red', linestyle='--')
    ax3.axhline(30, color='blue', linestyle='--')
    ax3.set_title("RSI & MFI")
    ax3.legend()

    ax4.plot(df["time_num"], df["MACD"], label="MACD", color="blue")
    ax4.plot(df["time_num"], df["MACD_signal"], label="Signal", color="orange")
    ax4.axhline(0, color='red', linestyle='--')
    ax4.set_title("MACD")
    ax4.legend()

    for ax in axs:
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    fig.autofmt_xdate()
    plt.tight_layout()
    return fig
