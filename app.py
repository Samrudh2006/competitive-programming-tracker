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
if "timer_sessions" not in st.session_state:
    st.session_state.timer_sessions = []
if "topics" not in st.session_state:
    st.session_state.topics = {}

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
    topic_tags = st.text_input("🏷️ Tags (comma separated)", placeholder="e.g., arrays, dp, trees")
    starred = st.checkbox("⭐ Mark as Important")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        entry = {"Date": date, "Solved": count, "Notes": notes}
        st.session_state.log.append(entry)
        if starred:
            st.session_state.starred_notes.append(entry)
        if topic_tags:
            for tag in [t.strip() for t in topic_tags.split(",")]:
                st.session_state.topics[tag] = st.session_state.topics.get(tag, 0) + count
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

# --- Progress Badge ---
st.markdown("### 🏅 Achievement Badge")
if solved_this_week >= weekly_goal:
    st.success("🎉 Excellent! You've met your weekly goal!")
elif solved_this_week >= weekly_goal * 0.75:
    st.info("💪 Almost there! Keep going!")
else:
    st.warning("🚀 Push a little more to hit your weekly target!")

# --- Pomodoro Timer + Logging ---
st.subheader("⏱️ Focus Mode (Pomodoro)")
timer_min = st.selectbox("Focus Time (minutes)", [15, 25, 45])
if st.button("▶️ Start Timer"):
    start_time = datetime.datetime.now()
    with st.empty():
        for i in range(timer_min * 60, 0, -1):
            m, s = divmod(i, 60)
            st.metric("Time Left", f"{m:02d}:{s:02d}")
            time.sleep(1)
    end_time = datetime.datetime.now()
    st.session_state.timer_sessions.append((start_time, end_time))
    st.success("⏰ Done! Take a break.")

if st.session_state.timer_sessions:
    st.markdown("### ⌛ Past Focus Sessions")
    for idx, (start, end) in enumerate(st.session_state.timer_sessions[-5:], 1):
        duration = end - start
        st.write(f"{idx}. {start.strftime('%H:%M:%S')} - {end.strftime('%H:%M:%S')} ({duration})")

# --- Topic Distribution Pie Chart ---
if st.session_state.topics:
    st.subheader("📊 Most Solved Topics")
    fig, ax = plt.subplots()
    ax.pie(st.session_state.topics.values(), labels=st.session_state.topics.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

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

# --- Export Log to CSV ---
if st.session_state.log:
    st.subheader("📤 Export Your Log")
    df = pd.DataFrame(st.session_state.log)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Log as CSV", data=csv, file_name="cp_log.csv", mime="text/csv")

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
