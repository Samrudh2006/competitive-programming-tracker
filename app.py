import streamlit as st
import pandas as pd
import datetime
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

# --- Session State ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "log" not in st.session_state:
    st.session_state.log = []
if "starred_notes" not in st.session_state:
    st.session_state.starred_notes = []

# --- Custom CSS for Modern UI ---
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
        }
        .title {
            font-size: 48px;
            font-weight: 700;
            text-align: center;
            color: #007BFF;
            margin-bottom: 10px;
        }
        .sub {
            text-align: center;
            font-size: 18px;
            color: gray;
        }
        .section-title {
            font-size: 26px;
            margin-top: 40px;
            margin-bottom: 10px;
            color: #007BFF;
            font-weight: 600;
        }
        .card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 15px;
        }
        .nav-menu {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 30px;
        }
        .nav-button {
            background-color: #007BFF;
            color: white !important;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 500;
            text-decoration: none;
            transition: background-color 0.3s;
            display: inline-block;
        }
        .nav-button:hover {
            background-color: #0056b3;
        }
    </style>

    <div class="nav-menu">
        <a href="#log" class="nav-button">📘 Log</a>
        <a href="#goal" class="nav-button">🎯 Goals</a>
        <a href="#timer" class="nav-button">⏱️ Pomodoro</a>
        <a href="#challenge" class="nav-button">📌 Challenge</a>
        <a href="#notes" class="nav-button">📝 Starred Notes</a>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar Profile ---

st.markdown("## 👤 Profile Setup")

if not st.session_state.submitted:
    with st.form("profile_form"):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
        
        with col2:
            name = st.text_input("Enter Your Name")
        
        submit = st.form_submit_button("Submit")

        if submit:
            if name and uploaded_file:
                st.session_state.name = name
                st.session_state.uploaded_file = uploaded_file
                st.session_state.submitted = True
            else:
                st.warning("Please upload a picture and enter your name.")
else:
    # Display submitted profile
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(st.session_state.uploaded_file, width=100)
    with col2:
        st.markdown(f"### 👋 Hello, **{st.session_state.name}**!")

    st.success("✅ Profile submitted successfully!")

# --- Main Header ---
st.markdown(f"<div class='title'>🚀 Welcome, {st.session_state.user_name}!</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>Track your daily progress, stay consistent, and become a better coder.</div>", unsafe_allow_html=True)

# --- DSA Log Section ---
st.markdown("<h2 id='log' class='section-title'>📘 Daily Practice Log</h2>", unsafe_allow_html=True)
with st.form("log_form"):
    date = st.date_input("📅 Date", value=datetime.date.today())
    count = st.number_input("🔢 Problems Solved", min_value=0)
    notes = st.text_area("📝 Notes", placeholder="What did you learn today?")
    starred = st.checkbox("⭐ Mark as Important")
    submitted = st.form_submit_button("✅ Add Entry")
    if submitted:
        entry = {"Date": date, "Solved": count, "Notes": notes}
        st.session_state.log.append(entry)
        if starred:
            st.session_state.starred_notes.append(entry)
        st.success("Entry added to log!")

if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📜 View All Logs"):
        st.dataframe(df)

# --- Weekly Goal Section ---
st.markdown("<h2 id='goal' class='section-title'>🎯 Weekly Goal</h2>", unsafe_allow_html=True)
weekly_goal = st.slider("Set your weekly goal", 0, 70, 35)
this_week = datetime.date.today().isocalendar()[1]
solved_this_week = sum(i["Solved"] for i in st.session_state.log if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week)
st.progress(min(solved_this_week / weekly_goal, 1.0))
st.info(f"✅ {solved_this_week} / {weekly_goal} problems solved this week")

# --- Pomodoro Timer ---
st.markdown("<h2 id='timer' class='section-title'>⏱️ Focus Mode (Pomodoro)</h2>", unsafe_allow_html=True)
timer_min = st.selectbox("Select Focus Duration (minutes)", [15, 25, 45])
if st.button("▶️ Start Focus Timer"):
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("🎉 Time's up! Take a break.")

# --- Random Challenge ---
st.markdown("<h2 id='challenge' class='section-title'>📌 Daily Random Challenge</h2>", unsafe_allow_html=True)
sheet_links = [
    ("Striver SDE", "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"),
    ("Love Babbar Sheet", "https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view"),
    ("GFG Sheet", "https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/"),
    ("Neetcode", "https://neetcode.io/"),
    ("Blind 75", "https://blind75.io/")
]
rand = random.choice(sheet_links)
st.info(f"🎲 Today's suggestion: [{rand[0]} 🔗]({rand[1]})")

# --- Starred Notes ---
if st.session_state.starred_notes:
    st.markdown("<h2 id='notes' class='section-title'>⭐ Starred Notes</h2>", unsafe_allow_html=True)
    for note in reversed(st.session_state.starred_notes[-5:]):
        st.markdown(f"""
        <div class="card">
            <strong>{note['Date']}</strong><br>
            ✍️ {note['Notes']}<br>
            ✅ Solved: {note['Solved']} problems
        </div>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<center style='color: gray;'>
Built with ❤️ using Streamlit | Stay consistent, coder!<br><br>
👨‍💻 Created by <b>Dwivedula Venkata Satya Samrudh</b>
</center>
""", unsafe_allow_html=True)
