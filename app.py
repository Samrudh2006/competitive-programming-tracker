import streamlit as st
import pandas as pd
import datetime
import random
import time
from PIL import Image

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

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
    st.markdown("### 📂 Menu")
    menu_items = [
        ("📊 DSA Tracker", "#dsa-tracker"),
        ("📘 Submissions", "#submissions"),
        ("📈 Progress", "#progress"),
        ("📚 Problems", "#problems"),
        ("💬 Discuss", "#discuss"),
        ("🏆 Contests", "#contests"),
        ("🎯 Daily Goals", "#daily-goals"),
        ("📝 Notebook", "#notebook"),
        ("🧪 Try New Features", "#try-new-features"),
        ("⚙️ Settings", "#settings"),
        ("🚪 Sign Out", "#sign-out")
    ]
    for name, link in menu_items:
        st.markdown(f"[{name}]({link})")

    # Theme Toggle
    theme = st.radio("🖌️ Theme", ["🌞 Light", "🌙 Dark"])
    if theme == "🌙 Dark":
        st.markdown("<style>body { background-color: #1e1e1e; color: #f0f0f0; }</style>", unsafe_allow_html=True)

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
# --- LeetCode‑style Profile Section ---
st.markdown("""
    <style>
    .profile-card {
        background-color: #f9f9f9;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .profile-name {
        font-size: 24px;
        font-weight: bold;
        color: #333;
        margin-bottom: 0.5rem;
    }
    .profile-image {
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid #FFD700;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 👤 Your Profile")

if not st.session_state.profile_submitted:
    with st.form("profile_form"):
        col1, col2 = st.columns([1, 3])
        with col1:
            uploaded_file = st.file_uploader("Upload Profile Pic", type=["jpg", "jpeg", "png"])
        with col2:
            name = st.text_input("Enter Your Name")
        submitted = st.form_submit_button("🚀 Submit")
        if submitted:
            if uploaded_file and name:
                st.session_state.uploaded_file = uploaded_file
                st.session_state.profile_name = name
                st.session_state.profile_submitted = True
            else:
                st.error("Please upload a picture and enter your name.")
else:
    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(st.session_state.uploaded_file, width=100, use_column_width=False, output_format="auto")
    with col2:
        st.markdown(f'<div class="profile-name">👋 Hello, {st.session_state.profile_name}</div>', unsafe_allow_html=True)
        st.success("Profile submitted successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<center style='color: gray;'>
Built with ❤️ using Streamlit | Stay consistent, coder!<br><br>
👨‍💻 Created by <b>Dwivedula Venkata Satya Samrudh</b>
</center>
""", unsafe_allow_html=True)

