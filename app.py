import streamlit as st
import urllib.request
import json
import pandas as pd

st.set_page_config(page_title="Advanced Live FX Dashboard", layout="wide")

# 🎨 سمارٹ سی ایس ایس (CSS) بیک گراؤنڈ تبدیل کرنے کے لیے
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
    }
    div[data-testid="stMetricValue"] {
        color: #FBBC05 !important;
    }
    .stDataFrame {
        background-color: #1E1E1E !important;
        border-radius: 10px;
    }
    h1, h2, h3 {
        font-family: 'Arial', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# گوگل کے رنگ برنگے لوگو کا ڈیزائن (HTML/CSS)
st.markdown(
    "<h1 style='text-align: center; font-size: 55px; font-family: Arial, sans-serif; font-weight: bold; margin-bottom: 20px;'>"
    "<span style='color: #4285F4;'>G</span>"
    "<span style='color: #EA4335;'>o</span>"
    "<span style='color: #FBBC05;'>o</span>"
    "<span style='color: #4285F4;'>g</span>"
    "<span style='color: #34A853;'>l</span>"
    "<span style='color: #EA4335;'>e</span>"
    "<span style='font-size: 20px; color: #888888; font-weight: normal; margin-left: 10px;'>ڈیش بورڈ</span>"
    "</h1>", 
    unsafe_allow_html=True
)

st.markdown("<p style='text-align: center; color: #AAAAAA;'>دنیا بھر کی کرنسیوں کو تبدیل کریں اور لائیو مارکیٹ ریٹس کا پورا ٹیبل دیکھیں۔</p>", unsafe_allow_html=True)
st.markdown("---")

col_left, col_right = st.columns(2)

major_currencies = {
    "OMR": "عمانی ریال",
    "USD": "امریکی ڈالر",
    "PKR": "پاکستانی روپیہ",
    "INR": "بھارتی روپیہ",
    "AED": "اماراتی درہم",
    "SAR": "سعودی ریال",
    "EUR": "یورو",
    "GBP": "برطانوی پاؤنڈ"
}

with col_left:
    st.markdown("<h3 style='color: #4285F4;'>🔁 فوری متبادل (Converter)</h3>", unsafe_allow_html=True)
    amount = st.number_input("رقم لکھیں (Amount):", min_value=1.0, value=1.0, step=1.0)
    
    from_currency = st.selectbox("کس کرنسی سے (From):", list(major_currencies.keys()), index=0)
    to_currency = st.selectbox("کس کرنسی میں (To):", list(major_currencies.keys()), index=2)
    
    if st.button("تبدیل کریں", use_container_width=True):
        try:
            url = f"https://er-api.com{from_currency}"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            
            if "rates" in data and to_currency in data["rates"]:
                rate = data["rates"][to_currency]
                res = amount * rate
                st.markdown(f"<h2 style='color: #34A853;'>{amount} {from_currency} = {res:,.2f} {to_currency}</h2>", unsafe_allow_html=True)
                st.caption(f"🕒 لائیو ریٹ اپڈیٹ: {data['time_last_update_utc']}")
        except Exception as e:
            st.error(f"کنکشن میں مسئلہ آیا: {e}")

with col_right:
    st.markdown("<h3 style='color: #FBBC05;'> Bars 📊 عمانی ریال (OMR) مارکیٹ</h3>", unsafe_allow_html=True)
    st.write("1 عمانی ریال کے مقابلے میں دیگر کرنسیوں کے لائیو ریٹس:")
    
    try:
        omr_url = "https://er-api.comOMR"
        omr_response = urllib.request.urlopen(omr_url)
        omr_data = json.loads(omr_response.read().decode())
        
        if "rates" in omr_data:
            table_data = []
            for code, name in major_currencies.items():
                if code != "OMR" and code in omr_data["rates"]:
                    current_rate = omr_data["rates"][code]
                    table_data.append({
                        "کرنسی کوڈ": code,
                        "کرنسی کا نام": name,
                        "1 OMR کی قیمت": f"{current_rate:,.2f}"
                    })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown("<p style='color: #34A853;'>✅ کلاؤڈ مارکیٹ بورڈ لائیو اپڈیٹ ہو چکا ہے۔</p>", unsafe_allow_html=True)
    except Exception as e:
        st.info("لائیو ٹیبل لوڈ کرنے کے لیے انٹرنیٹ چیک کریں۔")
