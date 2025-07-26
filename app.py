# streamlit_app.py (Enhanced Version with Theme Toggle + User Profile)

import streamlit as st
import pandas as pd
import datetime
from random import sample

st.set_page_config(page_title="Competitive Programming Tracker", layout="wide")

# ---------------------- THEME TOGGLE --------------------- #
theme = st.sidebar.radio("🎨 Choose Theme", ["Light", "Dark"])

if theme == "Dark":
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
      border-radius: 5px;
      margin: 5px;
    }

    .stProgress>div>div>div>div {
      background-color: #00c2c2;
    }
    </style>
    """
    st.markdown(dark_css, unsafe_allow_html=True)

# ---------------------- USER PROFILE ------------------------ #
st.sidebar.header("👤 My Profile")
user_name = st.sidebar.text_input("Enter your name", "Coder")
photo_choice = st.sidebar.radio("Choose a profile image option", ["Upload your own", "Choose from list"])

if photo_choice == "Upload your own":
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        st.sidebar.image(uploaded_file, width=150)
else:
    image_options = {
        "Avatar 1": "https://i.imgur.com/9J3GgG2.png",
        "Avatar 2": "https://i.imgur.com/MI9VQGZ.png",
        "Avatar 3": "https://i.imgur.com/mM3zJ5Y.png"
    }
    selected_avatar = st.sidebar.selectbox("Choose avatar", list(image_options.keys()))
    st.sidebar.image(image_options[selected_avatar], width=150)

# ------------------ MAIN HEADER ------------------ #
st.title("💻 Competitive Programming Tracker")
st.subheader(f"👋 Welcome, {user_name}")

# ------------------ SHEETS LINKS ------------------ #
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)")
st.sidebar.markdown("- [Neetcode](https://neetcode.io/)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")

# ------------------ PROBLEM LIST ------------------ #
problems = pd.read_csv("https://raw.githubusercontent.com/Samrudh2006/cp-problems-dataset/main/problems.csv")

st.subheader("🧠 Random 100 Problems")
random_100 = problems.sample(n=100)

solved = st.multiselect("✅ Mark problems as solved", random_100['Problem Name'])
st.progress(len(solved)/100)

st.write(f"**{len(solved)} / 100 problems solved**")

with st.expander("📄 View All Selected Problems"):
    st.dataframe(random_100[['Problem Name', 'Link', 'Source']], use_container_width=True)

# ------------------ DAILY STREAK TRACKER ------------------ #
st.header("🔥 Daily Tracker")
today = datetime.date.today()
log = st.session_state.get('log', [])

with st.form("daily_log"):
    date = st.date_input("Date", value=today)
    count = st.number_input("Problems Solved Today", min_value=0, max_value=100, step=1)
    notes = st.text_area("Any Notes")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        log.append({'Date': date, 'Solved': count, 'Notes': notes})
        st.session_state['log'] = log
        st.success("Entry added!")

if log:
    df = pd.DataFrame(log)
    st.line_chart(df.set_index('Date')['Solved'])
    with st.expander("📘 Daily Log Table"):
        st.dataframe(df)

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.markdown("Created with ❤️ by YourName")
