# streamlit_app.py

import streamlit as st
import pandas as pd
import datetime
from random import sample

st.set_page_config(page_title="CP Tracker", layout="wide")

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

# ---------------------- HEADER --------------------- #
st.title("💻 Competitive Programming Tracker")
st.subheader("👋 Welcome, Samrudh2006")

# ------------------ DSA SHEET LINKS ------------------ #
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)")
st.sidebar.markdown("- [Neetcode 150](https://neetcode.io/)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")

# ------------------ PROBLEM LIST ------------------ #
st.header("🧠 Your 100 Practice Problems")

problems_data = [
    {"Problem Name": f"Problem {i+1}", "Link": "https://example.com", "Source": "Striver/Babbar/GFG"}
    for i in range(100)
]
problems = pd.DataFrame(problems_data)

if 'solved' not in st.session_state:
    st.session_state.solved = []

solved = st.multiselect("✅ Mark problems as solved", problems['Problem Name'], default=st.session_state.solved)
st.session_state.solved = solved

st.progress(len(solved) / len(problems))
st.write(f"**{len(solved)} / {len(problems)} problems solved**")

with st.expander("📄 View All Problems"):
    st.dataframe(problems[['Problem Name', 'Link', 'Source']], use_container_width=True)

# ------------------ GOAL SETTING ------------------ #
st.header("🎯 Weekly Goal")
if 'goal' not in st.session_state:
    st.session_state.goal = 10

goal = st.slider("Set your weekly goal (problems)", 5, 100, st.session_state.goal)
st.session_state.goal = goal
st.write(f"🎯 Your weekly goal is to solve **{goal}** problems!")

# ------------------ DAILY TRACKER ------------------ #
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
        st.success("✅ Entry added!")

if log:
    df = pd.DataFrame(log)
    st.line_chart(df.set_index('Date')['Solved'])
    with st.expander("📘 Daily Log Table"):
        st.dataframe(df)

# ------------------ FOOTER ------------------ #
st.markdown("---")
st.markdown("Created with ❤️ by [Samrudh2006](https://github.com/Samrudh2006)")
