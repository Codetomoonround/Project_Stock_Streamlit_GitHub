import streamlit as st
import pandas as pd
import os
import shutil
from data_utils import fetch_stock_data, calculate_indicators, check_alerts
from plot_utils import plot_chart

st.set_page_config(layout="wide")
st.title("📈 Phân tích kỹ thuật cổ phiếu")

symbol = st.text_input("Nhập mã cổ phiếu (ví dụ: HPG, SSI, VNM):", value="HPG").upper()
start_date = st.date_input("Ngày bắt đầu:", value=pd.to_datetime("2024-01-01"))

os.makedirs("data", exist_ok=True)
os.makedirs("charts", exist_ok=True)
os.makedirs("logs", exist_ok=True)

if symbol:
    st.subheader(f"📊 Phân tích: {symbol}")
    df = fetch_stock_data(symbol, start_date.strftime("%Y-%m-%d"))

    if df is not None and not df.empty:
        df = calculate_indicators(df)
        alerts = check_alerts(df)
        fig = plot_chart(df, symbol)
        st.pyplot(fig)

        if alerts:
            st.warning("⚠️ " + " | ".join(alerts))
        else:
            st.success("✅ Không có cảnh báo kỹ thuật")

        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Tải dữ liệu CSV", data=csv_data, file_name=f"{symbol}.csv", mime="text/csv")

        df.to_csv(f"data/{symbol}.csv", index=False)

        if st.button("📦 Tạo file nén ZIP"):
            zip_path = "data_output.zip"
            shutil.make_archive("data_output", 'zip', "data")
            with open(zip_path, "rb") as f:
                st.download_button("⬇️ Tải toàn bộ dữ liệu ZIP", data=f, file_name=zip_path, mime="application/zip")
    else:
        st.error("❌ Không lấy được dữ liệu cho mã cổ phiếu này.")
