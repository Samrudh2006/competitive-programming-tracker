# cp_tracker_app.py

import streamlit as st
import pandas as pd
import datetime
import time
import os

# --------- PAGE CONFIG --------- #
st.set_page_config(page_title="🚀 CP Tracker", layout="wide")

# --------- SESSION SETUP --------- #
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

if 'log' not in st.session_state:
    st.session_state.log = []

if 'solved_problems' not in st.session_state:
    st.session_state.solved_problems = set()

if 'goal' not in st.session_state:
    st.session_state.goal = 0

# --------- SIDEBAR --------- #
st.sidebar.header("👤 Profile")
user_name = st.sidebar.text_input("Enter your name", value=st.session_state.user_name)
st.session_state.user_name = user_name

profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])
if profile_pic:
    st.sidebar.image(profile_pic, width=120)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# Theme toggle
theme = st.sidebar.radio("Theme Mode", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown("""
        <style>
        body { background-color: #0f1117; color: white; }
        section[data-testid="stSidebar"] { background-color: #161a25; }
        </style>
    """, unsafe_allow_html=True)

# Useful Links
st.sidebar.markdown("---")
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")
st.sidebar.markdown("- [Neetcode](https://neetcode.io/)")

# Profile Greeting
if user_name:
    st.markdown(f"## 👋 Welcome back, **{user_name}**")
else:
    st.markdown("## 👋 Welcome, Coder!")

st.markdown("---")
# ---------- PROBLEM SETUP ---------- #
st.header("🧠 Problem Set Tracker")

# File Upload
# ------------------ Load Problems ------------------ #
st.header("🧠 Random 100 CP Problems")

# Load default problems file from GitHub
problems = pd.read_csv("https://raw.githubusercontent.com/Samrudh2006/cp-problems-dataset/main/problems.csv")

# Select 100 random problems
random_100 = problems.sample(n=100)

# Allow marking problems as solved
solved = st.multiselect("✅ Tick solved problems:", random_100['Problem Name'])
st.progress(len(solved)/100)
st.write(f"**{len(solved)} / 100 problems solved**")

# Expandable list
with st.expander("📄 View Problem List"):
    for index, row in random_100.iterrows():
        st.markdown(f"**🔹 {row['Problem Name']}**")
        st.markdown(f"[🔗 Go to Problem]({row['Link']})")
        st.markdown("---")


# ---------- FILTERING ---------- #
st.markdown("### 🔍 Filter Problems")
col1, col2 = st.columns(2)

with col1:
    selected_difficulty = st.multiselect("Select Difficulty", df_problems['Difficulty'].unique())

with col2:
    selected_tags = st.multiselect("Select Tags", df_problems['Tags'].unique())

filtered_df = df_problems.copy()

if selected_difficulty:
    filtered_df = filtered_df[filtered_df['Difficulty'].isin(selected_difficulty)]

if selected_tags:
    filtered_df = filtered_df[filtered_df['Tags'].isin(selected_tags)]

# ---------- SOLVED TRACKER ---------- #
st.markdown("### ✅ Mark Solved Problems")
selected = st.multiselect("Choose solved problems", filtered_df['Problem Name'])

# Store solved set in session
st.session_state.solved_problems.update(selected)
progress = len(st.session_state.solved_problems) / len(df_problems)

st.progress(progress)
st.success(f"{len(st.session_state.solved_problems)} / {len(df_problems)} problems solved")

# ---------- VIEW TABLE ---------- #
with st.expander("📄 View Problem List Table"):
    st.dataframe(filtered_df)

# ---------- EXPORT SOLVED ---------- #
if st.download_button("⬇️ Download Solved Problems", pd.DataFrame({'Solved': list(st.session_state.solved_problems)}).to_csv(index=False), "solved.csv"):
    st.success("Download started!")

st.markdown("---")
# ---------- DAILY PROBLEM TRACKER ---------- #
st.header("🔥 Daily Problem Tracker")

if 'daily_log' not in st.session_state:
    st.session_state.daily_log = []

with st.form("daily_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📅 Date", value=datetime.date.today())
    with col2:
        count = st.number_input("✅ Solved Today", min_value=0, step=1)

    notes = st.text_area("📝 Notes about today's practice (optional)")
    submit = st.form_submit_button("Add Entry")

    if submit:
        st.session_state.daily_log.append({'Date': date, 'Solved': count, 'Notes': notes})
        st.success("Entry added!")

if st.session_state.daily_log:
    df_log = pd.DataFrame(st.session_state.daily_log)
    st.line_chart(df_log.set_index("Date")["Solved"])

    with st.expander("📘 Daily Log Table"):
        st.dataframe(df_log)

# ---------- GOAL TRACKER ---------- #
st.header("🎯 Goal Setting")

goal = st.number_input("Set a total CP problem goal", min_value=1, step=10)
solved_now = len(st.session_state.solved_problems)
goal_progress = solved_now / goal if goal else 0

st.progress(goal_progress)
st.write(f"**{solved_now}/{goal}** problems solved towards your goal")

# ---------- CODING TIMER ---------- #
st.header("⏱️ Practice Timer")

if "start_time" not in st.session_state:
    st.session_state.start_time = None

timer_col1, timer_col2 = st.columns(2)

with timer_col1:
    if st.button("▶️ Start"):
        st.session_state.start_time = datetime.datetime.now()

with timer_col2:
    if st.button("⏹️ Stop"):
        if st.session_state.start_time:
            elapsed = datetime.datetime.now() - st.session_state.start_time
            st.success(f"You coded for **{elapsed.seconds // 60} minutes and {elapsed.seconds % 60} seconds**")
            st.session_state.start_time = None
        else:
            st.warning("Start the timer first!")

# ---------- SAVE/LOAD USER DATA ---------- #
st.header("💾 Save / Load My Progress")

if st.button("💾 Save Progress to CSV"):
    combined = {
        "Solved Problems": list(st.session_state.solved_problems),
        "Daily Log": st.session_state.daily_log
    }
    save_df = pd.DataFrame(combined["Solved Problems"], columns=["Solved Problems"])
    save_df.to_csv("user_progress.csv", index=False)
    st.success("Progress saved to user_progress.csv")

load_file = st.file_uploader("🔄 Load Previous Progress", type=["csv"])
if load_file:
    df_loaded = pd.read_csv(load_file)
    st.session_state.solved_problems.update(df_loaded["Solved Problems"].tolist())
    st.success("Progress loaded successfully!")

st.markdown("---")
# ---------- THEME & USER PREFS ---------- #
st.sidebar.subheader("⚙️ Preferences")

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

theme_choice = st.sidebar.radio("Choose Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1)

# Apply theme styling
if theme_choice == "Dark":
    dark_style = """
    <style>
    body { background-color: #0f1117; color: #f5f5f5; }
    section[data-testid="stSidebar"] { background-color: #161a25; }
    .stButton>button { background-color: #00adb5; color: white; }
    .stProgress>div>div>div>div { background-color: #00ffcc; }
    </style>
    """
    st.markdown(dark_style, unsafe_allow_html=True)

st.session_state.theme = theme_choice  # save preference

# ---------- PROFILE PICTURE WITH GALLERY ---------- #
st.sidebar.subheader("🧑 Select Profile Picture")

pic_source = st.sidebar.radio("Choose Source", ["Upload", "From Gallery"])

if pic_source == "Upload":
    uploaded_pic = st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_pic:
        st.sidebar.image(uploaded_pic, width=100)
    elif "user_image" in st.session_state:
        st.sidebar.image(st.session_state.user_image, width=100)
    else:
        st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)
else:
    gallery = {
        "Dev Icon": "https://cdn-icons-png.flaticon.com/512/1055/1055687.png",
        "Rocket Coder": "https://cdn-icons-png.flaticon.com/512/2721/2721296.png",
        "Girl Dev": "https://cdn-icons-png.flaticon.com/512/921/921347.png",
        "Boy Dev": "https://cdn-icons-png.flaticon.com/512/2922/2922506.png"
    }
    selected = st.sidebar.selectbox("Choose Avatar", list(gallery.keys()))
    st.session_state.user_image = gallery[selected]
    st.sidebar.image(st.session_state.user_image, width=100)

# ---------- FINAL TOUCHES ---------- #
st.markdown("---")
st.markdown(
    "<div style='text-align:center;'>"
    "✅ <b>Built for Competitive Coders</b> | 📈 Track your progress | 💪 Stay consistent"
    "</div>",
    unsafe_allow_html=True,
)
