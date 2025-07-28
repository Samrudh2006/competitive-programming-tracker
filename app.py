import streamlit as st
import pandas as pd
import datetime
import random
import time
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")
import streamlit as st
from PIL import Image

# 
# --- Session State Setup ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "profile_pic" not in st.session_state:
    st.session_state.profile_pic = None
if "log" not in st.session_state:
    st.session_state.log = []
if "starred_notes" not in st.session_state:
    st.session_state.starred_notes = []

# --- Sidebar ---
with st.sidebar:
    # Profile form
    with st.form("profile_form"):
        st.markdown("### 👤 Enter Profile Details")
        name_input = st.text_input("Your Name", value=st.session_state.user_name)
        profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.session_state.user_name = name_input.strip() or "Coder"
            st.session_state.profile_pic = profile_pic
            st.success("✅ Profile Updated!")

    # Display Profile
    if st.session_state.user_name:
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.session_state.profile_pic:
                img = Image.open(st.session_state.profile_pic)
                st.image(img, width=50)
            else:
                st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=50)
        with col2:
            st.markdown(f"**{st.session_state.user_name}**")
        st.markdown("---")

    # Sidebar Menu
# --- Navigation Menu ---
# --- Navigation Menu ---
st.sidebar.header("📂 Menu")

menu = st.sidebar.radio("Navigate to", [
    "🏁 DSA Tracker",
    "📊 Submissions",
    "📈 Progress",
    "💬 Discuss",
    "🏆 Contests",
    "📝 Notebook"
])

# --- Handle Menu Navigation with External Links ---
query_params = st.query_params

if menu == "🏁 DSA Tracker":
    query_params["section"] = "dsa-tracker"
    st.markdown("[🔗 Go to DSA 30 Days (Unstop)](https://unstop.com/competitions/30-days-dsa-challenge-unstop-632056)", unsafe_allow_html=True)

elif menu == "📊 Submissions":
    query_params["section"] = "submissions"
    st.markdown("[🔗 Open LeetCode Dashboard](https://leetcode.com/progress/)", unsafe_allow_html=True)

elif menu == "📈 Progress":
    query_params["section"] = "progress"
    st.markdown("📆 Your daily/weekly stats are shown below ⬇️")

elif menu == "💬 Discuss":
    query_params["section"] = "discuss"
    st.markdown("[🔗 Ask doubts on GFG Discuss](https://practice.geeksforgeeks.org/discuss)", unsafe_allow_html=True)

elif menu == "🏆 Contests":
    query_params["section"] = "contests"
    st.markdown("[🔗 LeetCode Contests Page](https://leetcode.com/contest/)", unsafe_allow_html=True)

elif menu == "📝 Notebook":
    query_params["section"] = "notebook"
    st.text_area("🧠 Personal Notes / Scratchpad", height=200)

    



    
# --- Sidebar Theme Toggle ---
theme = st.sidebar.radio("🖌️ Choose Theme", ["🌞 Light", "🌙 Dark"])

if theme == "🌙 Dark":
    st.markdown("""
        <style>
        body {
            background-color: #0e1117;
            color: #f5f6fa;
        }
        .stApp {
            background-color: #0e1117;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .stApp {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

    # DSA Sheets
    st.header("📚 DSA Sheets")
    st.markdown("""
    - [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
    - [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)
    - [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)
    - [Neetcode](https://neetcode.io/)
    - [Blind 75](https://blind75.io/)
    """)

# --- Main Area ---

# Welcome
st.markdown(f"<h1>🚀 Welcome, {st.session_state.user_name or 'Coder'}!</h1>", unsafe_allow_html=True)

# Daily Practice Log
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

# Log Display
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📘 View Log"):
        st.dataframe(df)

# Weekly Goal Tracker
st.subheader("🎯 Weekly Goal")
weekly_goal = st.slider("Set your goal", 0, 70, 35)
this_week = datetime.date.today().isocalendar()[1]
solved_this_week = sum(
    i["Solved"] for i in st.session_state.log
    if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week
)
st.progress(min(solved_this_week / weekly_goal, 1.0))
st.write(f"**{solved_this_week} / {weekly_goal} solved this week**")

# Pomodoro Timer
st.subheader("⏱️ Focus Mode (Pomodoro)")
timer_min = st.selectbox("Focus Time (minutes)", [15, 25, 45])
if st.button("▶️ Start Timer"):
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("⏰ Done! Take a break.")

# Random Challenge
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

# Starred Notes
if st.session_state.starred_notes:
    st.subheader("⭐ Starred Notes")
    for n in st.session_state.starred_notes[-5:]:
        st.markdown(f"- **{n['Date']}**: {n['Notes']} ({n['Solved']} problems)")

# Motivational Quote
quotes = [
    "“Consistency is what transforms average into excellence.”",
    "“The expert in anything was once a beginner.”",
    "“Code more. Fear less.”",
    "“Success is the sum of small efforts repeated daily.”"
]
st.success(f"💡 {random.choice(quotes)}")

# Footer
st.markdown("---")
st.markdown("""
<center style='color: gray;'>
Built with ❤️ using Streamlit | Stay consistent, coder!<br><br>
👨‍💻 Created by <b>Dwivedula Venkata Satya Samrudh</b>
</center>
""", unsafe_allow_html=True)

