# streamlit_app.py (Updated with 100 Individual Trackable Problems)

import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Competitive Programming Tracker", layout="wide")

# ---------------------- DARK MODE CSS --------------------- #
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

# ---------------------- USER LOGIN ------------------------ #
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if username != "" and password != "":
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Please enter both username and password")
    st.stop()

# ------------------ USER LOGGED IN VIEW ------------------ #
st.title("💻 Competitive Programming Tracker")
st.subheader(f"👋 Welcome, {st.session_state.username}")

# ------------------ SHEETS LINKS ------------------ #
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)")
st.sidebar.markdown("- [Neetcode](https://neetcode.io/)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")

# ------------------ 100 PROBLEMS LIST ------------------ #
problems_data = pd.read_csv("https://raw.githubusercontent.com/Samrudh2006/cp-problems-dataset/main/problems.csv")

st.subheader("🧠 Track 100 Problems")

if 'solved_problems' not in st.session_state:
    st.session_state['solved_problems'] = []

for i, row in problems_data.iterrows():
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        checked = st.checkbox("", key=row['Problem Name'], value=row['Problem Name'] in st.session_state['solved_problems'])
        if checked and row['Problem Name'] not in st.session_state['solved_problems']:
            st.session_state['solved_problems'].append(row['Problem Name'])
        elif not checked and row['Problem Name'] in st.session_state['solved_problems']:
            st.session_state['solved_problems'].remove(row['Problem Name'])
    with col2:
        st.markdown(f"[{row['Problem Name']}]({row['Link']}) — `{row['Source']}`")

progress = len(st.session_state['solved_problems']) / len(problems_data)
st.progress(progress)
st.write(f"✅ {len(st.session_state['solved_problems'])} / {len(problems_data)} problems solved")

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
st.markdown("Created with ❤️ by [Samrudh](https://github.com/Samrudh2006)")
