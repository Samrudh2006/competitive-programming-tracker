import streamlit as st
import pandas as pd
import datetime

# ----------- Streamlit Config ----------- #
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

# ----------- Custom HTML/CSS Design ----------- #
custom_css = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #FF6B00;
}
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
.card {
    padding: 20px;
    border-radius: 10px;
    background-color: #ffffff;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
.problem-box {
    background-color: #e6f7ff;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}
hr {
    border: 1px solid #eee;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ----------- Persistent Username ----------- #
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

st.sidebar.header("👤 Your Profile")
name_input = st.sidebar.text_input("Enter your name", value=st.session_state.user_name or "Coder")
st.session_state.user_name = name_input or "Coder"

# Profile Picture Upload
profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])
if profile_pic:
    st.sidebar.image(profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# ----------- Sheet Links ----------- #
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("""
- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)
- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)
- [Neetcode](https://neetcode.io/)
- [Blind 75](https://blind75.io/)
""")

# ----------- Theme Toggle ----------- #
theme = st.sidebar.radio("Theme", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown("""
    <style>
    body { background-color: #1e1e1e; color: #f5f5f5; }
    .card { background-color: #2c2c2c; color: #f5f5f5; }
    .problem-box { background-color: #333333; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# ----------- Main Title ----------- #
st.markdown(f"<h1>🚀 Hello, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)

# ----------- CP Problems Section ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🧠 CP Problem Tracker")

# Add your static list of problems
problems = [
    {"Problem Name": "Two Sum", "Link": "https://leetcode.com/problems/two-sum/"},
    {"Problem Name": "Reverse Linked List", "Link": "https://leetcode.com/problems/reverse-linked-list/"},
    {"Problem Name": "Binary Search", "Link": "https://leetcode.com/problems/binary-search/"},
    {"Problem Name": "Maximum Subarray", "Link": "https://leetcode.com/problems/maximum-subarray/"},
    {"Problem Name": "Valid Parentheses", "Link": "https://leetcode.com/problems/valid-parentheses/"},
    # Add up to 150 manually
]

problem_names = [p["Problem Name"] for p in problems]
solved = st.multiselect("✅ Tick problems you've solved:", problem_names)

# Progress Bar
progress = len(solved) / len(problems)
st.progress(progress)
st.write(f"**{len(solved)} / {len(problems)} solved**")

# View Problem List
with st.expander("📄 View Problem List"):
    for p in problems:
        st.markdown(f"""
        <div class='problem-box'>
        <strong>🔹 {p['Problem Name']}</strong><br>
        <a href="{p['Link']}" target="_blank">🔗 Go to Problem</a>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ----------- Daily Log Section ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🔥 Daily Practice Log")

if "log" not in st.session_state:
    st.session_state.log = []

with st.form("log_form"):
    date = st.date_input("📅 Date", value=datetime.date.today())
    count = st.number_input("🔢 Problems Solved", min_value=0)
    notes = st.text_area("📝 Notes")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        st.session_state.log.append({"Date": date, "Solved": count, "Notes": notes})
        st.success("Added!")

# Show chart and table
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📘 View Full Log"):
        st.dataframe(df)
st.markdown("</div>", unsafe_allow_html=True)
# ---------- Focus Timer Section ---------- #
# ---------- Focus Timer Section ---------- #
import time

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏳ Focus Mode Timer (Pomodoro)")

# Initialize state variables
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None
if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "timer_duration" not in st.session_state:
    st.session_state.timer_duration = 25 * 60  # default 25 mins
if "remaining_time" not in st.session_state:
    st.session_state.remaining_time = 25 * 60

# UI to set focus time
focus_time = st.slider("🎯 Set Focus Time (in minutes)", min_value=5, max_value=60, value=25)

# Start / Stop buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Start Timer"):
        st.session_state.timer_duration = focus_time * 60
        st.session_state.remaining_time = focus_time * 60
        st.session_state.timer_start = time.time()
        st.session_state.timer_running = True
with col2:
    if st.button("⏹ Stop Timer"):
        st.session_state.timer_running = False

# Countdown logic
if st.session_state.timer_running:
    elapsed = int(time.time() - st.session_state.timer_start)
    st.session_state.remaining_time = max(0, st.session_state.timer_duration - elapsed)

    minutes = st.session_state.remaining_time // 60
    seconds = st.session_state.remaining_time % 60

    st.markdown(f"### ⏱ {minutes:02d}:{seconds:02d} remaining")

    if st.session_state.remaining_time == 0:
        st.success("✅ Time's up! Great job! 🎉")
        st.balloons()
        st.session_state.timer_running = False
    else:
        # Refresh every second
        st.experimental_rerun()
else:
    st.info("⏸ Timer is not running. Set time and press ▶️ Start.")

st.markdown("</div>", unsafe_allow_html=True)



# ----------- Footer ----------- #
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>✨ Built with ❤️ for passionate coders ✨</center>", unsafe_allow_html=True)
