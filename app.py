import streamlit as st
import pandas as pd
import datetime
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

# --- Session State Setup ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "log" not in st.session_state:
    st.session_state.log = []
if "starred_notes" not in st.session_state:
    st.session_state.starred_notes = []
if "code_snippets" not in st.session_state:
    st.session_state.code_snippets = []

# --- Sidebar Theme Toggle ---
theme = st.sidebar.radio("🖌️ Theme", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown("<style>body { background-color:                                                             

                      
st.sidebar.header("#1e1e1e; color: #f0f0f0; }</style>", unsafe_allow_html=True)

# --- User Profile ---
st.sidebar.header("👤 Profile")
name_input = st.sidebar.text_input("Enter your name", value=st.session_state.user_name or "Coder")
st.session_state.user_name = name_input or "Coder"
profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])
if profile_pic:
    st.sidebar.image(profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

                         
st.sidebar.header("# --- DSA Sheet Links ---
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown(                                                                                                                                                                                                                                                                                                                                                                  )

                        
st.markdown(f""""
- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)
- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)
- [Neetcode](https://neetcode.io/)
- [Blind 75](https://blind75.io/)
""")

# --- Welcome Header ---
st.markdown(f"<h1>🚀 Welcome, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)

                            
st.subheader("# --- Daily Practice Log ---
st.subheader("🔥 Daily Practice Log")
with st.form("log_form"):
    date = st.date_input("📅 Date", value=datetime.date.today())
    count = st.number_input("🔢 Problems Solved", min_value=0)
    notes = st.text_area("📝 Notes")
    starred = st.checkbox("⭐ Mark as Important")
    code_snippet = st.text_area("💻 Code Snippet")
    submitted = st.form_submit_button("Add Entry")
if submitted:
    entry = {"Date": date, "Solved": count, "Notes": notes, "Code Snippet": code_snippet}
    st.session_state.log.append(entry)
    if starred:
        st.session_state.starred_notes.append(entry)
    if code_snippet:
        st.session_state.code_snippets.append(code_snippet)
    st.success("Log Added!")

if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📘 View Log"):
        st.dataframe(df)

                             
st.subheader("# --- Weekly Goal Tracker ---
st.subheader("🎯 Weekly Goal")
weekly_goal = st.slider("Set your goal", 0, 70, 35)
this_week = datetime.date.today().isocalendar()[1]
solved_this_week = sum(i["Solved"] for i in st.session_state.log if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week)
st.progress(min(solved_this_week / weekly_goal, 1.0))
st.write(f"**{solved_this_week} / {weekly_goal} solved this week**")

                        
st.subheader("# --- Pomodoro Timer ---
st.subheader("⏱️ Focus Mode (Pomodoro)")
timer_min = st.selectbox("Focus Time (minutes)", [15, 25, 45])
if st.button("▶️ Start Timer"):
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
    st.success("⏰ Done! Take a break.")

                                
st.subheader("# --- Daily Random Challenge ---
st.subheader("📌 Daily Random Challenge")
sheet_links = [
    ("Striver SDE", "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"),
    ("
