import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import gspread
from google.oauth2.service_account import Credentials

# ================================================================================
# CẤU HÌNH STREAMLIT
# ================================================================================

st.set_page_config(
    page_title="Crypto VSA Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Crypto VSA Analysis - Volume Spread Analysis")
st.markdown("---")

# ================================================================================
# SIDEBAR - CONFIGURATION
# ================================================================================

st.sidebar.header("⚙️ Cấu hình Google Sheets")

# Google Sheets ID
sheet_id = st.sidebar.text_input(
    "📋 Google Sheets ID:",
    value="https://docs.google.com/spreadsheets/d/18R0gJQmJjEjxUyYMiM2oKN9SpV0qHmzvXJKsPSyGcbA/edit?usp=sharing",  # ← PASTE SHEET_ID VÀO ĐÂY
    help="Lấy từ URL Google Sheets: https://docs.google.com/spreadsheets/d/SHEET_ID/edit"
)

sheet_name = st.sidebar.text_input(
    "📄 Tên Google Sheets:",
    value="DEFI",
    help="Tên Google Sheets (VD: DEFI, BTC, ETH...)"
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Cấu hình VSA")

# VSA Config
length_ma = st.sidebar.slider("Volume MA Length:", 10, 50, 20)
vol_strong = st.sidebar.slider("Strong threshold (%):", 20, 100, 50)
vol_spike = st.sidebar.slider("Spike threshold (%):", 10, 50, 20)
show_volume_ma = st.sidebar.checkbox("Hiển thị Volume MA", value=True)
chart_height = st.sidebar.slider("Chiều cao biểu đồ:", 600, 1200, 900, 50)

# ================================================================================
# CẤU HÌNH VSA
# ================================================================================

VSA_CONFIG = {
    'length_ma': length_ma,
    'ratio_ultra': 2.2,
    'ratio_very_high': 1.8,
    'ratio_high': 1.2,
    'ratio_normal': 0.8,
    'ratio_low': 0.4,
}

VOLUME_CHG_THRESHOLD = {
    'extreme': 100,
    'strong': vol_strong,
    'spike': vol_spike,
    'drop': -30,
}

# ================================================================================
# FUNCTIONS - ĐỌC TỪ GOOGLE SHEETS
# ================================================================================

@st.cache_data(ttl=600)
def get_google_sheets_data(sheet_id, sheet_name):
    """Đọc dữ liệu từ Google Sheets công khai"""
    try:
        # Dùng public access (không cần credentials)
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
        
        df = pd.read_csv(url)
        
        # Kiểm tra các cột cần thiết
        required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_cols):
            st.error(f"❌ Sheet thiếu các cột cần thiết: {required_cols}")
            return None
        
        return df
        
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc Google Sheets: {e}")
        st.info("💡 Đảm bảo Google Sheets đã được chia sẻ công khai (Anyone with the link)")
        return None

def format_volume(volume):
    if pd.isna(volume):
        return "0"
    volume = float(volume)
    if volume >= 1_000_000_000:
        return f"{volume/1_000_000_000:.1f}B"
    elif volume >= 1_000_000:
        return f"{volume/1_000_000:.1f}M"
    elif volume >= 1_000:
        return f"{volume/1_000:.1f}K"
    else:
        return f"{volume:.0f}"

def process_dataframe(df):
    """Xử lý và làm sạch dữ liệu"""
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(',', '')
                .str.replace('$', '')
                .str.replace(' ', '')
                .replace('', np.nan)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['Vol Chg'] = df['Volume'].pct_change() * 100
    df = df.dropna(subset=['Open', 'High', 'Low', 'Close', 'Volume'])
    
    return df.reset_index(drop=True)

def analyze_vsa_volume(df, config):
    """Phân loại volume theo VSA"""
    df['Volume_MA'] = df['Volume'].rolling(window=config['length_ma'], min_periods=1).mean()
    cond = [
        df['Volume'] >= df['Volume_MA'] * config['ratio_ultra'],
        df['Volume'] >= df['Volume_MA'] * config['ratio_very_high'],
        df['Volume'] >= df['Volume_MA'] * config['ratio_high'],
        df['Volume'] >= df['Volume_MA'] * config['ratio_normal'],
        df['Volume'] >= df['Volume_MA'] * config['ratio_low'],
    ]
    colors = ['#9C27B0', '#F44336', '#FF9800', '#4CAF50', '#2196F3', '#9E9E9E']
    levels = ['Ultra High','Very High','High','Normal','Low','Very Low']
    df['VSA_Level'] = np.select(cond, levels[:-1], default='Very Low')
    df['VSA_Color'] = np.select(cond, colors[:-1], default='#9E9E9E')
    return df

def analyze_volume_change(df, threshold):
    """Phân loại màu sắc cho volume change"""
    def classify_vol_chg(vol_chg):
        if pd.isna(vol_chg):
            return '#808080'
        elif vol_chg >= threshold['extreme']:
            return '#FF00FF'
        elif vol_chg >= threshold['strong']:
            return '#FF0000'
        elif vol_chg >= threshold['spike']:
            return '#FFA500'
        elif vol_chg > -20:
            return '#00FF00'
        elif vol_chg >= threshold['drop']:
            return '#87CEEB'
        else:
            return '#0000FF'
    df['Vol_Chg_Color'] = df['Vol Chg'].apply(classify_vol_chg)
    return df

def create_candlestick_chart(df, title, config, vol_threshold, show_ma, height):
    """Vẽ biểu đồ 3 panels"""
    df = analyze_vsa_volume(df, config)
    df = analyze_volume_change(df, vol_threshold)

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=(f'Giá {title}', 'Volume Change %', 'Volume (VSA)')
    )

    # Panel 1: Nến VSA
    for vsa_level, color in [
        ('Ultra High', '#9C27B0'), ('Very High', '#F44336'),
        ('High', '#FF9800'), ('Normal', '#4CAF50'),
        ('Low', '#2196F3'), ('Very Low', '#9E9E9E')
    ]:
        df_level = df[df['VSA_Level'] == vsa_level]
        if len(df_level) == 0:
            continue
        
        hover_text = [
            f"<b>Ngày:</b> {row['Date'].strftime('%Y-%m-%d')}<br>"
            f"<b>Open:</b> ${row['Open']:,.2f}<br>"
            f"<b>High:</b> ${row['High']:,.2f}<br>"
            f"<b>Low:</b> ${row['Low']:,.2f}<br>"
            f"<b>Close:</b> ${row['Close']:,.2f}<br>"
            f"<b>Volume:</b> {format_volume(row['Volume'])}<br>"
            f"<b>Vol Chg:</b> {row['Vol Chg']:.1f}%"
            for idx, row in df_level.iterrows()
        ]
        
        fig.add_trace(go.Candlestick(
            x=df_level['Date'], open=df_level['Open'],
            high=df_level['High'], low=df_level['Low'],
            close=df_level['Close'],
            increasing_line_color=color, decreasing_line_color=color,
            increasing_fillcolor=color, decreasing_fillcolor=color,
            text=hover_text, hoverinfo='text', showlegend=False
        ), row=1, col=1)

    # Panel 2: Volume Change %
    fig.add_trace(go.Bar(
        x=df['Date'], y=df['Vol Chg'],
        marker_color=df['Vol_Chg_Color'],
        showlegend=False,
        hovertemplate='<b>Vol Chg:</b> %{y:.1f}%<extra></extra>'
    ), row=2, col=1)
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1, row=2, col=1)
    fig.add_hline(
        y=vol_threshold['strong'], 
        line_dash="dot", line_color="red", line_width=1,
        annotation_text=f"+{vol_threshold['strong']}%",
        annotation_position="right",
        row=2, col=1
    )

    # Panel 3: Volume VSA
    fig.add_trace(go.Bar(
        x=df['Date'], y=df['Volume'],
        marker_color=df['VSA_Color'],
        showlegend=False,
        hovertemplate='<b>Volume:</b> %{y:,.0f}<extra></extra>'
    ), row=3, col=1)
    
    if show_ma:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Volume_MA'],
            line=dict(color='rgba(255, 255, 255, 0.8)', width=2, dash='dash'),
            showlegend=False, hoverinfo='skip',
        ), row=3, col=1)

    fig.update_layout(
        template='plotly_white',
        height=height,
        xaxis_rangeslider_visible=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='cursor',
                     spikecolor='rgba(128, 128, 128, 0.5)', spikethickness=1)
    fig.update_yaxes(showspikes=True, spikemode='across+marker', spikesnap='cursor',
                     spikecolor='rgba(255, 152, 0, 0.5)', spikethickness=1)
    
    fig.update_yaxes(title_text='Giá (USD)', row=1, col=1)
    fig.update_yaxes(title_text='Vol Chg %', row=2, col=1)
    fig.update_yaxes(title_text='Volume', row=3, col=1)
    fig.update_xaxes(title_text='Thời gian', row=3, col=1)
    
    return fig

# ================================================================================
# MAIN APP
# ================================================================================

if st.sidebar.button("🔄 Tải dữ liệu", type="primary"):
    if not sheet_id:
        st.warning("⚠️ Vui lòng nhập Google Sheets ID")
    else:
        with st.spinner(f"Đang tải dữ liệu từ Google Sheets '{sheet_name}'..."):
            df = get_google_sheets_data(sheet_id, sheet_name)
            
            if df is not None and len(df) > 0:
                df = process_dataframe(df)
                
                if len(df) > 0:
                    # Thống kê
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("💰 Giá hiện tại", f"${df['Close'].iloc[-1]:,.2f}")
                    with col2:
                        st.metric("📈 Vol Chg", f"{df['Vol Chg'].iloc[-1]:.1f}%")
                    with col3:
                        st.metric("📊 Cao nhất", f"${df['High'].max():,.2f}")
                    with col4:
                        st.metric("📉 Thấp nhất", f"${df['Low'].min():,.2f}")
                    
                    st.markdown("---")
                    
                    # Vẽ biểu đồ
                    fig = create_candlestick_chart(
                        df, sheet_name,
                        VSA_CONFIG, VOLUME_CHG_THRESHOLD,
                        show_volume_ma, chart_height
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Bảng dữ liệu
                    with st.expander("📋 Xem dữ liệu chi tiết"):
                        st.dataframe(df.tail(50), use_container_width=True)
                else:
                    st.error("❌ Không có dữ liệu hợp lệ sau khi xử lý")

# Hướng dẫn sử dụng
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Hướng dẫn")
st.sidebar.markdown("""
1. Nhập **Google Sheets ID**
2. Nhập **Tên Sheet** (VD: DEFI)
3. Điều chỉnh tham số VSA
4. Nhấn **Tải dữ liệu**

**Lưu ý:**
- Google Sheets phải được chia sẻ công khai
- Sheet phải có đủ cột: Date, Open, High, Low, Close, Volume
""")

st.sidebar.markdown("---")
st.sidebar.info("💡 Dữ liệu từ Google Sheets của bạn")
