# Crypto VSA Analysis 📈

Ứng dụng phân tích Volume Spread Analysis (VSA) cho cryptocurrency sử dụng dữ liệu real-time từ Binance API.

## 🚀 Demo

🔗 **[Live Demo trên Streamlit Cloud](https://YOUR-APP-NAME.streamlit.app)** _(sau khi deploy)_

## ✨ Tính năng

- ✅ **Real-time Data**: Lấy dữ liệu trực tiếp từ Binance API
- ✅ **VSA Analysis**: Phân tích Volume Spread với màu sắc trực quan
- ✅ **Volume Change Tracking**: Theo dõi % thay đổi volume
- ✅ **Multi Timeframe**: Hỗ trợ 1h, 4h, 1d, 1w
- ✅ **10+ Cryptocurrencies**: BTC, ETH, BNB, SOL, ADA, XRP, DOGE, DOT, MATIC, AVAX

## 📊 VSA Color Coding

| Màu | Mức độ | Điều kiện |
|-----|--------|-----------|
| 🟣 | Ultra High | Volume > 2.2x MA |
| 🔴 | Very High | Volume > 1.8x MA |
| 🟠 | High | Volume > 1.2x MA |
| 🟢 | Normal | Volume > 0.8x MA |
| 🔵 | Low | Volume > 0.4x MA |
| ⚪ | Very Low | Volume < 0.4x MA |

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly
- **Data Processing**: Pandas, NumPy
- **API**: Binance Public API
- **Deployment**: Streamlit Cloud / Docker

## 📦 Cài đặt local

