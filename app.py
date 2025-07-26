import streamlit as st
import pandas as pd
import datetime
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")
import streamlit as st
from PIL import Image

# Sidebar layout
with st.sidebar:
    # --- Profile Submission Form ---
    with st.form("profile_form"):
        st.markdown("### 👤 Enter Profile Details")
        name_input = st.text_input("Your Name", value=st.session_state.get("user_name", ""))
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.user_name = name_input.strip() or "Coder"
            st.session_state.profile_pic = profile_pic

    # --- Display Profile after Submission ---
    if "user_name" in st.session_state:
        col1, col2 = st.columns([1, 3])
        with col1:
            if "profile_pic" in st.session_state and st.session_state.profile_pic:
                img = Image.open(st.session_state.profile_pic)
                st.image(img, width=50)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=50)  # default icon
        with col2:
            st.markdown(f"**{st.session_state.user_name}**")
        st.markdown("---")

    # --- App Menu (Styled Like LeetCode) ---
    st.markdown("### 📂 Menu")
    st.markdown("📊 [DSA Tracker](#dsa-tracker)")
    st.markdown("📘 [Submissions](#submissions)")
    st.markdown("📈 [Progress](#progress)")
    st.markdown("📚 [Problems](#problems)")
    st.markdown("💬 [Discuss](#discuss)")
    st.markdown("🏆 [Contests](#contests)")
    st.markdown("🎯 [Daily Goals](#daily-goals)")
    st.markdown("📝 [Notebook](#notebook)")
    st.markdown("🧪 [Try New Features](#try-new-features)")
    st.markdown("⚙️ [Settings](#settings)")
    st.markdown("🚪 [Sign Out](#sign-out)")

# --- Session State Setup ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "log" not in st.session_state:
    st.session_state.log = []
if "starred_notes" not in st.session_state:
    st.session_state.starred_notes = []

# --- Sidebar Theme Toggle ---
theme = st.sidebar.radio("🖌️ Theme", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown("<style>body { background-color: #1e1e1e; color: #f0f0f0; }</style>", unsafe_allow_html=True)

# --- User Profile ---

# --- User Profile Submission ---
with st.sidebar.form("profile_form"):
    st.header("👤 Profile")
    name_input = st.text_input("Enter your name", value=st.session_state.user_name)
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.user_name = name_input or "Coder"
        st.session_state.profile_pic = profile_pic
        st.success("✅ Profile submitted!")

# --- Show Submitted Info ---
if "profile_pic" in st.session_state and st.session_state.profile_pic:
    st.sidebar.image(st.session_state.profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# --- DSA Sheet Links ---
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("""
- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)
- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)
- [Neetcode](https://neetcode.io/)
- [Blind 75](https://blind75.io/)
""")

# --- Welcome Header ---
st.markdown(f"<h1>🚀 Welcome, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)

# --- Daily Practice Log ---
st.subheader("🔥 Daily Practice Log")
with st.form("log_form"):
    date = st.date_input("📅 Date", value=datetime.date.today())
    count = st.number_input("🔢 Problems Solved", min_value=0)
    notes = st.text_area("📝 Notes")
    starred = st.checkbox("⭐ Mark as Important")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        entry = {"Date": date, "Solved": count, "Notes": notes}
        st.session_state.log.append(entry)
        if starred:
            st.session_state.starred_notes.append(entry)
        st.success("Log Added!")

if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📘 View Log"):
        st.dataframe(df)

# --- Weekly Goal Tracker ---
st.subheader("🎯 Weekly Goal")
weekly_goal = st.slider("Set your goal", 0, 70, 35)
this_week = datetime.date.today().isocalendar()[1]
solved_this_week = sum(i["Solved"] for i in st.session_state.log if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week)
st.progress(min(solved_this_week / weekly_goal, 1.0))
st.write(f"**{solved_this_week} / {weekly_goal} solved this week**")

# --- Pomodoro Timer ---
st.subheader("⏱️ Focus Mode (Pomodoro)")
timer_min = st.selectbox("Focus Time (minutes)", [15, 25, 45])
if st.button("▶️ Start Timer"):
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("⏰ Done! Take a break.")

# --- Daily Random Challenge ---
st.subheader("📌 Daily Random Challenge")
sheet_links = [
    ("Striver SDE", "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"),
    ("Love Babbar", "https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view"),
    ("GFG Sheet", "https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/"),
    ("Neetcode", "https://neetcode.io/"),
    ("Blind 75", "https://blind75.io/")
]
rand = random.choice(sheet_links)
st.info(f"Try something new from: [{rand[0]} 🔗]({rand[1]})")

# --- Starred Notes Section ---
if st.session_state.starred_notes:
    st.subheader("⭐ Starred Notes")
    for n in st.session_state.starred_notes[-5:]:
        st.markdown(f"- **{n['Date']}**: {n['Notes']} ({n['Solved']} problems)")

# --- Motivational Quote ---
quotes = [
    "“Consistency is what transforms average into excellence.”",
    "“The expert in anything was once a beginner.”",
    "“Code more. Fear less.”",
    "“Success is the sum of small efforts repeated daily.”"
]
st.success(f"💡 {random.choice(quotes)}")

# --- Footer ---
st.markdown("---")
st.markdown("<center>✨ Built with ❤️ using Streamlit | Keep Coding ✨</center>", unsafe_allow_html=True)
