import streamlit as st
import urllib.request
import json
import pandas as pd

st.set_page_config(page_title="Advanced Live FX Dashboard", layout="wide")

st.title("💱 لائیو عالمی فاریکس ڈیش بورڈ (Live FX Board)")
st.write("دنیا بھر کی کرنسیوں کو تبدیل کریں اور لائیو مارکیٹ ریٹس کا پورا ٹیبل دیکھیں۔")

# دو کالمز کا لے آؤٹ بنانا
col_left, col_right = st.columns([1, 1])

# بڑی کرنسیاں جن کا ڈیٹا ٹریک کرنا ہے
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
    st.subheader("🔁 فوری متبادل (Instant Converter)")
    amount = st.number_input("رقم لکھیں (Amount):", min_value=1.0, value=1.0, step=1.0)
    
    from_currency = st.selectbox("کس کرنسی سے (From):", list(major_currencies.keys()), index=0)
    to_currency = st.selectbox("کس کرنسی میں (To):", list(major_currencies.keys()), index=2)
    
    if st.button("تبدیل کریں", use_container_width=True):
        try:
            url = f"https://open.er-api.com/v6/latest/{from_currency}"
            response = urllib.request.urlopen(url)
            data = json.loads(response.read().decode())
            
            if "rates" in data and to_currency in data["rates"]:
                rate = data["rates"][to_currency]
                res = amount * rate
                st.success(f"### {amount} {from_currency} = {res:,.2f} {to_currency}")
                st.caption(f"🕒 لائیو ریٹ اپڈیٹ: {data['time_last_update_utc']}")
        except Exception as e:
            st.error(f"کنکشن میں مسئلہ آیا: {e}")

with col_right:
    st.subheader("📊 عمانی ریال (OMR) عالمی مارکیٹ بورڈ")
    st.write("1 عمانی ریال کے مقابلے میں دیگر کرنسیوں کے لائیو ریٹس:")
    
    try:
        # لائیو کلاؤڈ او پی آئی سے ڈیٹا کھینچنا
        omr_url = "https://er-api.com"
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
                        "1 عمانی ریال (OMR) کی قیمت": f"{current_rate:,.2f}"
                    })
            
            # پائتھن ڈیٹا فریم (DataFrame) کے ذریعے خوبصورت ٹیبل بنانا
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.success("✅ کلاؤڈ مارکیٹ بورڈ لائیو اپڈیٹ ہو چکا ہے۔")
    except Exception as e:
        st.info("لائیو ٹیبل لوڈ کرنے کے لیے انٹرنیٹ چیک کریں۔")
