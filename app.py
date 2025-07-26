import streamlit as st
import pandas as pd
import datetime
import random
import time
import matplotlib.pyplot as plt

# --- Page Setup ---
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

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
st.sidebar.header("👤 Profile")
name_input = st.sidebar.text_input("Enter your name", value=st.session_state.user_name or "Coder")
st.session_state.user_name = name_input or "Coder"

profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])
if profile_pic:
    st.sidebar.image(profile_pic, width=100)
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
    topic = st.selectbox("📚 Topic", ["Arrays", "Strings", "Linked List", "Trees", "Graphs", "DP", "Recursion", "Sorting", "Maths", "Other"])
    starred = st.checkbox("⭐ Mark as Important")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        entry = {"Date": date, "Solved": count, "Notes": notes, "Topic": topic}
        st.session_state.log.append(entry)
        if starred:
            st.session_state.starred_notes.append(entry)
        st.success("✅ Log Added!")

# --- Log Display ---
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)

    st.line_chart(df.set_index("Date")["Solved"])

    with st.expander("📘 View Log Data"):
        st.dataframe(df)

# --- Weekly Goal Tracker ---
st.subheader("🎯 Weekly Goal")
weekly_goal = st.slider("Set your goal", 0, 70, 35)
this_week = datetime.date.today().isocalendar()[1]
solved_this_week = sum(i["Solved"] for i in st.session_state.log if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week)
st.progress(min(solved_this_week / weekly_goal, 1.0))
st.write(f"**✅ {solved_this_week} / {weekly_goal} solved this week**")

# --- Streak Tracker ---
st.subheader("🔥 Current Streak")
dates = sorted([pd.to_datetime(i["Date"]).date() for i in st.session_state.log])
streak = 0
today = datetime.date.today()
for i in range(len(dates)-1, -1, -1):
    if (today - dates[i]).days == streak:
        streak += 1
    else:
        break
st.write(f"🔥 **You’ve been consistent for {streak} day(s) in a row!**")

# --- Pie Chart for Topic Distribution ---
if st.session_state.log:
    st.subheader("📊 Topic Distribution")
    topic_counts = pd.DataFrame(st.session_state.log)["Topic"].value_counts()
    if not topic_counts.empty:
        fig, ax = plt.subplots()
        ax.pie(topic_counts, labels=topic_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

# --- Pomodoro Timer ---
st.subheader("⏱️ Focus Mode (Pomodoro)")
timer_min = st.selectbox("Focus Time (minutes)", [15, 25, 45])
if st.button("▶️ Start Timer"):
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
        st.success("⏰ Done! Take a break!")

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

# --- Flashcard Picker ---
st.subheader("🧠 DSA Concept Flashcard")
flashcards = {
    "Two Pointer": "Efficient for searching pairs/triples in sorted arrays.",
    "Sliding Window": "For subarrays/substrings of size k or with some constraint.",
    "Backtracking": "Try all combinations, but prune invalid ones early.",
    "Dynamic Programming": "Optimal substructure + overlapping subproblems.",
    "Binary Search": "Used in sorted arrays or to minimize/maximize answers."
}
selected = st.selectbox("Choose a concept", list(flashcards.keys()))
st.info(flashcards[selected])

# --- Bonus Tip Section ---
st.subheader("💡 Bonus Coding Tip")
tips = [
    "Use Leetcode Discuss for hints before seeing full solutions.",
    "Practice one topic a week to build deep understanding.",
    "Build your own GitHub repo to track CP progress.",
    "Explain problems aloud after solving — it deepens retention!",
    "Start timing your problems to simulate real contests."
]
st.success(random.choice(tips))

# --- Export Logs to CSV ---
if st.session_state.log:
    st.subheader("📂 Export Your Log")
    df = pd.DataFrame(st.session_state.log)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Log as CSV", csv, "cp_log.csv", "text/csv")

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
