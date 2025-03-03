import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Apply Enhanced Theme & UI
st.set_page_config(page_title="Ramadan 2025 Calendar", layout="wide")
st.markdown("""
    <style>
        body { background-color: #121212; color: #e0e0e0; }
        .stApp { background-color: #121212; }
        .stTitle, .stHeader, .stSubheader { color: #ffcc00; text-align: center; }
        .stTable, .stDataFrame { background-color: #1e1e2e; color: #ffcc00; border-radius: 10px; padding: 10px; }
        .stButton>button { background-color: #0f3460; color: white; border: 1px solid #ffcc00; border-radius: 10px; padding: 10px; font-size: 16px; width: 100%; }
        .stButton>button:hover { background-color: #ffcc00; color: black; }
        .stTextInput>div>div>input { background-color: #1e1e2e; color: white; border-radius: 5px; }
        .css-1d391kg { background-color: #1e1e2e !important; }
        .css-145kmo2 { color: #e0e0e0 !important; }
        h1, h2, h3, h4, h5, h6 { color: #ffcc00 !important; text-align: center; }
        .highlight-box { background-color: #0f3460; color: #ffcc00; padding: 15px; border-radius: 10px; text-align: center; font-size: 18px; }
        .arabic-text { color: #ffcc00; font-size: 20px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Function to fetch Ramadan 2025 Sehri and Iftar timings
def get_ramadan_timings(city="Karachi", country="Pakistan"):
    timings = []
    for month in [3, 4]:  # March and April 2025
        api_url = f"https://api.aladhan.com/v1/calendarByCity?city={city}&country={country}&method=2&year=2025&month={month}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            for day in data['data']:
                hijri_month = int(day['date']['hijri']['month']['number'])
                if hijri_month == 9:  # Ensure only Ramadan dates are included
                    date = day['date']['gregorian']['date']
                    sehri = day['timings']['Fajr'].split(" ")[0]
                    iftar = datetime.strptime(day['timings']['Maghrib'].split(" ")[0], "%H:%M").strftime("%I:%M %p")
                    timings.append([date, sehri, iftar])
    if timings:
        return pd.DataFrame(timings, columns=["Date", "Sehri", "Iftar"])
    else:
        st.error("Failed to fetch Ramadan timings. Please try again.")
        return pd.DataFrame(columns=["Date", "Sehri", "Iftar"])

# Function to display Dua
def display_dua():
    with st.expander("✨ Click to View Sehri & Iftar Duas ✨"):
        st.markdown('<div class="highlight-box">Sehri Dua</div>', unsafe_allow_html=True)
        st.markdown('<div class="arabic-text">وَبِصَوْمِ غَدٍ نَّوَيْتُ مِنْ شَهْرِ رَمَضَانَ</div>', unsafe_allow_html=True)
        st.audio("https://www.prayerstimings.com/data/audio/0/4-e55e9bba4621cb00b6c62b8dc2f0b0e4.mp3")
        
        st.markdown('<div class="highlight-box">Iftar Dua</div>', unsafe_allow_html=True)
        st.markdown('<div class="arabic-text">اللَّهُمَّ إِنِّي لَكَ صُمْتُ وَبِكَ آمَنْتُ وَعَلَيْكَ تَوَكَّلْتُ وَعَلَى رِزْقِكَ أَفْطَرْتُ</div>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/10-e7f3cee2e94f103917366f88a6f16a4b.mp3")
    
    with st.expander("✨ Click to View Three Ashra Duas ✨"):
        st.markdown('<div class="highlight-box">First Ashra Dua (رحمت)</div>', unsafe_allow_html=True)
        st.markdown('<div class="arabic-text">يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ</div>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/14-6a4644a7fa0262324c53ad354aeecfb2.mp3")
        
        st.markdown('<div class="highlight-box">Second Ashra Dua (مغفرت)</div>', unsafe_allow_html=True)
        st.markdown('<div class="arabic-text">أَسْتَغْفِرُ اللَّهَ رَبِّي مِنْ كُلِّ ذَنْبٍ وَأَتُوبُ إِلَيْهِ</div>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/12-ac2fcc54eeb8a0930ed412dfbde1352a.mp3")
        
        st.markdown('<div class="highlight-box">Third Ashra Dua (نجات)</div>', unsafe_allow_html=True)
        st.markdown('<div class="arabic-text">اللَّهُمَّ أَجِرْنِي مِنَ النَّارِ</div>', unsafe_allow_html=True)
        st.audio("https://islamictimedate.com/apps/data/audio/0/16-9b2365379ac6eb329409d0ad21393613.mp3")

# Streamlit UI
st.title("🌙 Ramadan 2025 Calendar")
st.subheader("Developed by Ashfa Khan")
st.sidebar.header("Settings")

# Dropdown for Cities and Countries
cities = ["Karachi", "Lahore", "Islamabad", "Mumbai", "Delhi", "Dhaka", "Istanbul", "Jeddah", "Makkah", "Madina", "New York", "London"]
countries = ["Pakistan", "India", "Bangladesh", "Turkey", "Saudi Arabia", "United States", "United Kingdom"]
city = st.sidebar.selectbox("City", cities)
country = st.sidebar.selectbox("Country", countries)

if st.sidebar.button("Get Timings"):
    timings_df = get_ramadan_timings(city, country)
    if not timings_df.empty:
        st.write("## 🕌 Ramadan 2025 Sehri & Iftar Timings")
        st.markdown('<div class="highlight-box">Sehri & Iftar Timings</div>', unsafe_allow_html=True)
        st.table(timings_df.style.set_properties(**{'background-color': '#1e1e2e', 'color': '#ffcc00'}))
    else:
        st.write("⚠ No data available. Please check city and country name.")

display_dua()
