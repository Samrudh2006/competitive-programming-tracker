# streamlit_app.py (Original UI with Improvements, No Login, Samrudh Name Removed)

import streamlit as st
import pandas as pd
import datetime
from random import sample

st.set_page_config(page_title="CP Tracker", layout="wide")

# ------------------ User Info ------------------ #
st.sidebar.header("👤 My Profile")
name = st.sidebar.text_input("Enter your name", value="")
profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])

if profile_pic:
    st.sidebar.image(profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# ------------------ Sheet Links ------------------ #
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)")
st.sidebar.markdown("- [Neetcode](https://neetcode.io/)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")

# ------------------ Theme Toggle ------------------ #
theme_mode = st.sidebar.radio("Choose Theme", ["🌞 Light", "🌙 Dark"])

if theme_mode == "🌙 Dark":
    dark_css = """
    <style>
    body {
      background-color: #0f1117;
      color: #ffffff;
    }
    section[data-testid="stSidebar"] {
      background-color: #161a25;
    }
    .stButton>button {
      background-color: #008080;
      color: white;
    }
    .stProgress>div>div>div>div {
      background-color: #00c2c2;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)

# ------------------ Main UI ------------------ #
st.title("🚀 Competitive Programming Tracker")
if name:
    st.subheader(f"Welcome, {name}!")

# ------------------ Load Problems ------------------ #
st.header("🧠 Random 100 CP Problems")
problems = pd.read_csv("https://raw.githubusercontent.com/Samrudh2006/cp-problems-dataset/main/problems.csv")
random_100 = problems.sample(n=100)

solved = st.multiselect("✅ Tick solved problems:", random_100['Problem Name'])
st.progress(len(solved)/100)
st.write(f"**{len(solved)} / 100 problems solved**")

with st.expander("📄 View Problem List"):
    for index, row in random_100.iterrows():
        st.markdown(f"**🔹 {row['Problem Name']}**")
        st.markdown(f"[🔗 Go to Problem]({row['Link']})")
        st.markdown("---")

# ------------------ Daily Tracker ------------------ #
st.header("🔥 Daily Problem Tracker")
today = datetime.date.today()
log = st.session_state.get('log', [])

with st.form("daily_log"):
    date = st.date_input("📅 Date", value=today)
    count = st.number_input("How many problems solved today?", min_value=0, step=1)
    notes = st.text_area("📝 Notes")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        log.append({'Date': date, 'Solved': count, 'Notes': notes})
        st.session_state['log'] = log
        st.success("Entry added!")

if log:
    df = pd.DataFrame(log)
    st.line_chart(df.set_index('Date')['Solved'])
    with st.expander("📘 View Daily Log Table"):
        st.dataframe(df)

# ------------------ Footer ------------------ #
st.markdown("---")
st.markdown("Built for CP tracking with ❤️ by the community")
