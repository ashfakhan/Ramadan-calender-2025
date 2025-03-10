import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests

# Streamlit UI Configuration
st.set_page_config(page_title="Ramadan 2025 Calendar", layout="wide")
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #e0e0e0; }
        table { width: 100%; border-collapse: collapse; }
        th { background-color: #ffcc00 !important; color: black !important; text-align: center !important; padding: 10px; border: 2px solid #ffcc00 !important; }
        td { padding: 10px; border: 1px solid #ffcc00 !important; text-align: center; color: #ffcc00; }
        tbody tr:nth-child(odd) { background-color: #2a2a3a !important; }
        tbody tr:nth-child(even) { background-color: #1e1e2e !important; }
        thead th { font-size: 18px; font-weight: bold; }
        tbody td:first-child { font-weight: bold; color: #ffcc00; }
        .arabic-text, h3, .highlight-box, h2, label, .stButton button { color: #ffcc00 !important; }
        h1, h2 { color: #ffcc00 !important; }
        .stButton button { background-color: black !important; border: 2px solid #ffcc00 !important; }
        .stSelectbox label { color: #ffcc00 !important; }
        .stSidebar { background-color: black !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🌙 Ramadan 2025 Calendar")
st.subheader("Developed by Ashfa Khan")

cities = ["Karachi", "Lahore", "Islamabad", "Mumbai", "Delhi", "Dhaka", "Istanbul", "Jeddah", "Makkah", "Madina", "New York", "London"]
countries = ["Pakistan", "India", "Bangladesh", "Turkey", "Saudi Arabia", "United States", "United Kingdom"]
city = st.selectbox("City", cities)
country = st.selectbox("Country", countries)

# Function to get Ramadan Timings
def get_ramadan_timings(city, country):
    api_url = f"https://api.aladhan.com/v1/calendarByCity?city={city}&country={country}&method=2&school=1&year=2025&month=3"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        timings = []
        
        for day in data['data']:
            hijri_month = int(day['date']['hijri']['month']['number'])
            if hijri_month == 9:
                date = day['date']['gregorian']['date']
                sehri = (datetime.strptime(day['timings']['Fajr'].split(" ")[0], "%H:%M") - timedelta(minutes=16)).strftime("%I:%M %p")
                iftar = (datetime.strptime(day['timings']['Maghrib'].split(" ")[0], "%H:%M") + timedelta(minutes=2)).strftime("%I:%M %p")
                timings.append([date, sehri, iftar])
        
        df = pd.DataFrame(timings, columns=["Date", "Sehri", "Iftar"])
        df.index = df.index + 1
        return df
    else:
        st.error("⚠ API Error! Timings not available.")
        return None

if st.button("Get Timings"):
    timings_df = get_ramadan_timings(city, country)
    if timings_df is not None:
        st.markdown("<h2>🕌 Ramadan 2025 Sehri & Iftar Timings</h2>", unsafe_allow_html=True)
        st.dataframe(timings_df.style.set_properties(**{'background-color': '#1e1e2e', 'color': '#ffcc00', 'text-align': 'center'}))

def display_dua():
    with st.expander("✨ Click to View Sehri & Iftar Duas ✨"):
        st.markdown('<h3>Dua e Sehri</h3>', unsafe_allow_html=True)
        st.markdown('<p class="arabic-text">وَبِصَوْمِ غَدٍ نَّوَيْتُ مِنْ شَهْرِ رَمَضَانَ</p>', unsafe_allow_html=True)
        st.audio("https://www.prayerstimings.com/data/audio/0/4-e55e9bba4621cb00b6c62b8dc2f0b0e4.mp3")
        
        st.markdown('<h3>Dua e Iftar</h3>', unsafe_allow_html=True)
        st.markdown('<p class="arabic-text">اللَّهُمَّ إِنِّي لَكَ صُمْتُ وَبِكَ آمَنْتُ وَعَلَيْكَ تَوَكَّلْتُ وَعَلَى رِزْقِكَ أَفْطَرْتُ</p>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/10-e7f3cee2e94f103917366f88a6f16a4b.mp3")
        
    with st.expander("✨ Click to View Three Ashra Duas ✨"):
        st.markdown('<div class="highlight-box">First Ashra Dua (رحمت)</div>', unsafe_allow_html=True)
        st.markdown('<p class="arabic-text">رَّبِّ ٱغۡفِرۡ وَٱرۡحۡمۡ وَأَنتَ خَيۡرُ ٱلرَّٰحِمِينَ</p>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/14-6a4644a7fa0262324c53ad354aeecfb2.mp3")
        
        st.markdown('<div class="highlight-box">Second Ashra Dua (مغفرت)</div>', unsafe_allow_html=True)
        st.markdown('<p class="arabic-text">أَسْتَغْفِرُ اللَّهَ رَبِّي مِنْ كُلِّ ذَنْبٍ وَأَتُوبُ إِلَيْهِ</p>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/12-ac2fcc54eeb8a0930ed412dfbde1352a.mp3")
        
        st.markdown('<div class="highlight-box">Third Ashra Dua (نجات)</div>', unsafe_allow_html=True)
        st.markdown('<p class="arabic-text">اللَّهُمَّ أَجِرْنِي مِنَ النَّارِ</p>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/16-9b2365379ac6eb329409d0ad21393613.mp3")

display_dua()
