import streamlit as st

st.set_page_config(page_title="Google Search UI", layout="centered")

# گوگل کے رنگ برنگے لوگو کا ڈیزائن (HTML/CSS)
st.markdown(
    "<h1 style='text-align: center; font-size: 55px; font-family: Arial, sans-serif; font-weight: bold; margin-bottom: 20px;'>"
    "<span style='color: #4285F4;'>G</span>"
    "<span style='color: #EA4335;'>o</span>"
    "<span style='color: #FBBC05;'>o</span>"
    "<span style='color: #4285F4;'>g</span>"
    "<span style='color: #34A853;'>l</span>"
    "<span style='color: #EA4335;'>e</span>"
    "<span style='font-size: 20px; color: #5f6368; font-weight: normal; margin-left: 10px;'>اسٹائل</span>"
    "</h1>", 
    unsafe_allow_html=True
)

# گوگل جیسا سرچ باکس
query = st.text_input("", placeholder="یہاں سرچ کریں یا ویب سائٹ کا لنک لکھیں...", label_visibility="collapsed")

# گوگل کے دو روایتی بٹن
col1, col2 = st.columns([1, 1])
with col1:
    search_pressed = st.button("Google Search", use_container_width=True)
with col2:
    lucky_pressed = st.button("I'm Feeling Lucky", use_container_width=True)

# جب صارف سرچ کا بٹن دبائے گا
if (search_pressed or query == "https://wikipedia.org") and query:
    st.markdown("---")
    st.write(f"🔍 آپ نے سرچ کیا ہے: **{query}**")
    st.markdown(f"### 🌐 سرچ کے نتائج (Simulated Results)")
    st.info("یہ آپ کے گوگل ڈیزائن کا پہلا خوبصورت نمونہ ہے۔")
