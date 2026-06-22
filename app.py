from __future__ import annotations

import base64
import uuid
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from src.graph import build_graph


load_dotenv()


st.set_page_config(
    page_title="FinMentor AI",
    page_icon="📈",
    layout="wide"
)


# ======================
# LOAD CSS
# ======================

def load_css():
    css_path = Path("style.css")

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )


load_css()


# ======================
# HEADER
# ======================

st.markdown(
    """
    <div class="header">
        <h1>FinMentor AI Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# ======================
# SIDEBAR — nav with st.button (full-width, no leftover boxes)
# ======================

MENU_OPTIONS = ["Chat AI", "Market Chart", "Risk Analysis"]

if "menu" not in st.session_state:
    st.session_state.menu = MENU_OPTIONS[0]

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            FinMentor AI
        </div>
        """,
        unsafe_allow_html=True
    )

    for option in MENU_OPTIONS:
        is_active = st.session_state.menu == option

        if st.button(
            option,
            key=f"nav_{option}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.menu = option
            st.rerun()

menu = st.session_state.menu


# ======================
# SESSION
# ======================

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

if "risk_messages" not in st.session_state:
    st.session_state.risk_messages = []


@st.cache_resource
def get_graph():
    return build_graph()


@st.cache_resource
def get_vision_model():
    # qwen/qwen3.6-27b is Groq's current vision-capable model
    # (llama-4-scout, the older vision model, was deprecated by Groq
    # in June 2026 — switch the model id here if Groq's lineup changes again)
    return ChatGroq(model="qwen/qwen3.6-27b", temperature=0.3)


graph = get_graph()


# ======================
# CHAT AI
# ======================

if menu == "Chat AI":

    st.markdown(
        """
        <div class="card">
            <h1>FinMentor AI</h1>
            <p>Sistem bantuan belajar trading berbasis NLP + LLM</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # riwayat percakapan (tampil di atas, terbaru di bawah)
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # kotak input — otomatis nempel di bawah layar oleh Streamlit
    question = st.chat_input("Tulis pertanyaan tentang trading di sini...")

    if question:

        st.session_state.chat_messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("AI sedang menganalisis..."):
                result = graph.invoke(
                    {
                        "question": question
                    },
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }
                )

            answer = result.get("answer", "Tidak ada jawaban")
            st.markdown(answer)

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": answer}
        )


# ======================
# CHART — real TradingView widget (live, real-time)
# ======================

elif menu == "Market Chart":

    st.markdown(
        """
        <div class="card">
            <h1>Market Realtime</h1>
            <p>Chart real-time langsung dari TradingView</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    symbol_options = {
        "BTC/USDT (Binance)": "BINANCE:BTCUSDT",
        "ETH/USDT (Binance)": "BINANCE:ETHUSDT",
        "EUR/USD": "FX:EURUSD",
        "XAU/USD (Gold)": "OANDA:XAUUSD",
    }

    selected_label = st.selectbox(
        "Pilih instrumen",
        list(symbol_options.keys())
    )
    symbol = symbol_options[selected_label]

    tradingview_html = f"""
    <div class="tradingview-widget-container">
      <div id="tv_chart"></div>
      <script src="https://s3.tradingview.com/tv.js"></script>
      <script>
      new TradingView.widget({{
        "width": "100%",
        "height": 520,
        "symbol": "{symbol}",
        "interval": "15",
        "timezone": "Asia/Jakarta",
        "theme": "dark",
        "style": "1",
        "locale": "id",
        "toolbar_bg": "#0a0e16",
        "enable_publishing": false,
        "allow_symbol_change": true,
        "container_id": "tv_chart"
      }});
      </script>
    </div>
    """

    components.html(tradingview_html, height=560)

    st.markdown(
        """
        <div class="card" style="margin-top: 8px;">
            <h1 style="font-size: 1.05rem;">Informasi Harga Pasar</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    symbol_info_html = f"""
    <div class="tradingview-widget-container">
      <div class="tradingview-widget-container__widget"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-symbol-info.js" async>
      {{
      "symbol": "{symbol}",
      "width": "100%",
      "locale": "id",
      "colorTheme": "dark",
      "isTransparent": true
      }}
      </script>
    </div>
    """

    components.html(symbol_info_html, height=200)


# ======================
# RISK — upload chart, AI vision menentukan entry/close + pola
# ======================

else:

    st.markdown(
        """
        <div class="card">
            <h1>Risk Analysis</h1>
            <p>Upload screenshot chart trading, AI akan membaca entry, close, dan pola yang terlihat.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_image = st.file_uploader(
        "Upload screenshot chart",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image is not None:
        st.image(
            uploaded_image,
            caption="Chart yang diupload",
            use_container_width=True
        )

        if st.button("Analisis Chart", type="primary"):

            base64_image = base64.b64encode(uploaded_image.getvalue()).decode("utf-8")
            mime_type = uploaded_image.type or "image/png"

            prompt_text = (
                "Kamu adalah asisten analisis teknikal trading. Amati chart pada gambar ini "
                "dan jelaskan secara terstruktur dengan poin-poin: "
                "1) tren yang terlihat (naik/turun/sideways), "
                "2) area supply dan demand atau support-resistance yang relevan, "
                "3) pola candlestick atau chart pattern yang teridentifikasi jika ada "
                "(misalnya double top, double bottom, head and shoulders, dll), "
                "4) area entry dan close/exit yang masuk akal berdasarkan pola tersebut. "
                "Jawab dalam Bahasa Indonesia, dan tutup jawabanmu dengan satu kalimat "
                "pengingat bahwa ini analisis edukatif berbasis pola visual, bukan nasihat finansial."
            )

            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}"
                        }
                    }
                ]
            )

            with st.spinner("AI sedang membaca chart..."):
                vision_model = get_vision_model()
                response = vision_model.invoke([message])

            st.session_state.risk_messages.append(
                {"role": "assistant", "content": response.content}
            )

    # riwayat hasil analisis (terbaru di bawah)
    for msg in st.session_state.risk_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])