import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# إعدادات الصفحة
st.set_page_config(page_title="داشبورد حالة الطقس", page_icon="🌤️", layout="wide")

# مفتاح API الخاص بك
API_KEY = "5da7da237f333dbf1062901caae4754c"

st.title("🌤️ لوحة تحكم حالة الطقس العالمية")
st.markdown("---")

# الشريط الجانبي لإدخال المدن
st.sidebar.header("إعدادات البحث")
default_cities = "Dubai, Abu Dhabi, Cairo, London, New York, Tokyo"
cities_input = st.sidebar.text_area("أدخل أسماء المدن (مفصولة بفواصل):", default_cities)
cities = [c.strip() for c in cities_input.split(",") if c.strip()]

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ar"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# جلب البيانات وإعداد الجدول
data_list = []
with st.spinner("جاري جلب بيانات الطقس..."):
    for city in cities:
        res = get_weather_data(city)
        if res:
            data_list.append({
                "المدينة": res["name"],
                "الدولة": res["sys"]["country"],
                "درجة الحرارة (°C)": res["main"]["temp"],
                "المحسوسة (°C)": res["main"]["feels_like"],
                "الرطوبة (%)": res["main"]["humidity"],
                "سرعة الرياح (m/s)": res["wind"]["speed"],
                "الحالة": res["weather"][0]["description"]
            })

if data_list:
    df = pd.DataFrame(data_list)

    # عرض البطاقات الإحصائية لأول مدينة في القائمة
    st.subheader(f"📊 نظرة عامة: {df['المدينة'].iloc[0]}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("درجة الحرارة", f"{df['درجة الحرارة (°C)'].iloc[0]} °C")
    col2.metric("الحرارة المحسوسة", f"{df['المحسوسة (°C)'].iloc[0]} °C")
    col3.metric("الرطوبة", f"{df['الرطوبة (%)'].iloc[0]}%")
    col4.metric("سرعة الرياح", f"{df['سرعة الرياح (m/s)'].iloc[0]} m/s")

    st.markdown("---")

    # الرسوم البيانية التفاعلية
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("🌡️ مقارنة درجات الحرارة بين المدن")
        fig_temp = px.bar(
            df, 
            x="المدينة", 
            y="درجة الحرارة (°C)", 
            color="درجة الحرارة (°C)",
            color_continuous_scale="Viridis",
            text="درجة الحرارة (°C)"
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_right:
        st.subheader("💧 نسبة الرطوبة حسب المدينة")
        fig_hum = px.pie(
            df, 
            names="المدينة", 
            values="الرطوبة (%)", 
            hole=0.4
        )
        st.plotly_chart(fig_hum, use_container_width=True)

    # عرض جدول البيانات الكامل
    st.subheader("📋 جدول البيانات التفصيلي")
    st.dataframe(df, use_container_width=True)

else:
    st.error("لم يتم العثور على بيانات. يرجى التأكد من تفعيل مفتاح الـ API الخاص بك على موقع OpenWeatherMap أو مراجعة أسماء المدن.")
