import os
import pandas as pd
from vnstock import Vnstock
from datetime import datetime
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator
from ta.trend import SMAIndicator, MACD
import logging

def setup_logger():
    log_folder = "logs"
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, f"{datetime.today().date()}.log")
    logger = logging.getLogger("stock_logger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()

def fetch_stock_data(symbol, start_date="2024-01-01"):
    try:
        df = Vnstock().stock(symbol=symbol, source="VCI").quote.history(
            start=start_date,
            end=str(datetime.today().date())
        )
        df["time"] = pd.to_datetime(df["time"])
        return df
    except Exception as e:
        logger.error(f"Lỗi lấy dữ liệu {symbol}: {e}")
        return None

def calculate_indicators(df):
    df["MA20"] = SMAIndicator(df["close"], window=20).sma_indicator()
    df["MA50"] = SMAIndicator(df["close"], window=50).sma_indicator()
    df["MA100"] = SMAIndicator(df["close"], window=100).sma_indicator()
    df["RSI14"] = RSIIndicator(df["close"], window=14).rsi()
    df["MFI14"] = MFIIndicator(df["high"], df["low"], df["close"], df["volume"], window=14).money_flow_index()
    macd = MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_signal"] = macd.macd_signal()
    return df

def check_alerts(df):
    latest = df.iloc[-1]
    alerts = []
    if latest["RSI14"] > 70:
        alerts.append("📈 RSI14 > 70 (Quá mua)")
    elif latest["RSI14"] < 30:
        alerts.append("📉 RSI14 < 30 (Quá bán)")
    if df["MACD"].iloc[-2] < df["MACD_signal"].iloc[-2] and latest["MACD"] > latest["MACD_signal"]:
        alerts.append("🔼 MACD cắt lên tín hiệu (Mua)")
    elif df["MACD"].iloc[-2] > df["MACD_signal"].iloc[-2] and latest["MACD"] < latest["MACD_signal"]:
        alerts.append("🔽 MACD cắt xuống tín hiệu (Bán)")
    cross = df["MA20"] > df["MA50"]
    if cross.iloc[-1] and not cross.shift(1).iloc[-1]:
        alerts.append("📈 MA20 cắt lên MA50 → BUY")
    elif not cross.iloc[-1] and cross.shift(1).iloc[-1]:
        alerts.append("📉 MA20 cắt xuống MA50 → SELL")
    return alerts
