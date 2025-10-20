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


Ứng dụng sẽ chạy tại: `http://localhost:8501`

## 🎯 Cách sử dụng

1. Chọn cryptocurrency từ dropdown (BTC, ETH, BNB...)
2. Chọn khung thời gian (1h, 4h, 1d, 1w)
3. Điều chỉnh tham số VSA:
   - Volume MA Length
   - Strong/Spike thresholds
4. Nhấn **"Tải dữ liệu"** để vẽ biểu đồ

## 📸 Screenshots

_TODO: Thêm screenshots sau khi deploy_

## 🔑 API Key

Không cần API key! Ứng dụng sử dụng Binance Public API (miễn phí).

## 📝 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

## 👨‍💻 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

## 🙏 Acknowledgments

- Dữ liệu từ [Binance API](https://binance-docs.github.io/apidocs/)
- Framework: [Streamlit](https://streamlit.io/)
- Charts: [Plotly](https://plotly.com/)


