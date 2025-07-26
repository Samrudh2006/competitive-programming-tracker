import streamlit as st
from datetime import datetime

# ----------- Streamlit Config ----------- #
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

# ----------- Custom CSS ----------- #
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
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
        .dark-mode {
            background-color: #1e1e1e !important;
            color: #f5f5f5 !important;
        }
    </style>
""", unsafe_allow_html=True)

# ----------- Persistent Name ----------- #
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# ----------- Sidebar - Profile ----------- #
st.sidebar.header("👤 Your Profile")
name_input = st.sidebar.text_input("Enter your name", value=st.session_state.user_name or "Coder")
st.session_state.user_name = name_input or "Coder"

# Profile Picture Upload
profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])
if profile_pic:
    st.sidebar.image(profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# ----------- Sidebar - DSA Sheets ----------- #
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
        </style>
    """, unsafe_allow_html=True)

# ----------- Main Title ----------- #
st.markdown(f"<h1>🚀 Hello, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)
# ----------- Daily Practice Log ----------- #
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
        st.success("Log entry added!")

if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    st.line_chart(df.set_index("Date")["Solved"])
    with st.expander("📘 View Full Log"):
        st.dataframe(df)

st.markdown("</div>", unsafe_allow_html=True)

# ----------- Focus Mode Timer ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("⏱️ Focus Mode Timer")

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "end_time" not in st.session_state:
    st.session_state.end_time = None

col1, col2 = st.columns(2)
with col1:
    focus_minutes = st.number_input("🎯 Set Focus Duration (minutes):", min_value=1, max_value=120, value=25)
with col2:
    if st.button("▶ Start Focus Timer"):
        st.session_state.end_time = datetime.datetime.now() + datetime.timedelta(minutes=focus_minutes)
        st.session_state.timer_running = True

if st.session_state.timer_running and st.session_state.end_time:
    remaining = st.session_state.end_time - datetime.datetime.now()
    if remaining.total_seconds() > 0:
        st.success(f"⏳ Time Left: {str(remaining).split('.')[0]}")
    else:
        st.success("✅ Time's up! Great job focusing!")
        st.session_state.timer_running = False

st.markdown("</div>", unsafe_allow_html=True)
# ----------- Streak Tracker (Monthly Heatmap) ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📆 Streak Tracker")

if "streak" not in st.session_state:
    st.session_state.streak = set()

selected_date = st.date_input("✅ Mark Today's Streak", value=datetime.date.today())
if st.button("➕ Add to Streak"):
    st.session_state.streak.add(str(selected_date))
    st.success("Streak updated!")

# Generate simple calendar heatmap (textual)
calendar_df = pd.DataFrame(
    {"Date": list(st.session_state.streak), "Streak": [1] * len(st.session_state.streak)}
)
calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])
calendar_df = calendar_df.set_index("Date").resample("D").sum().fillna(0)

st.bar_chart(calendar_df)
st.markdown("</div>", unsafe_allow_html=True)
# ----------- Concept Revision Section ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📚 Concept Revision Notes")

if "concept_notes" not in st.session_state:
    st.session_state.concept_notes = []

with st.form("concept_form"):
    tag = st.selectbox("📌 Tag", ["Arrays", "DP", "Graphs", "OOP", "Recursion", "Sorting", "Greedy", "Other"])
    note = st.text_area("📝 Note")
    save_note = st.form_submit_button("Save Note")
    if save_note:
        st.session_state.concept_notes.append({"Tag": tag, "Note": note})
        st.success("Note saved!")

# Display notes grouped by tags
if st.session_state.concept_notes:
    df_notes = pd.DataFrame(st.session_state.concept_notes)
    for tag in df_notes["Tag"].unique():
        with st.expander(f"🔖 {tag}"):
            for i, row in df_notes[df_notes["Tag"] == tag].iterrows():
                st.markdown(f"✅ {row['Note']}")

st.markdown("</div>", unsafe_allow_html=True)
# ----------- Mini CP Game ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("🎮 CP Mini Game: Quick Quiz")

questions = [
    {
        "q": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
        "a": "O(log n)"
    },
    {
        "q": "Which data structure uses FIFO?",
        "options": ["Stack", "Queue", "Tree", "Graph"],
        "a": "Queue"
    },
    {
        "q": "Which sorting algorithm is NOT stable?",
        "options": ["Bubble Sort", "Merge Sort", "Quick Sort", "Insertion Sort"],
        "a": "Quick Sort"
    }
]

score = 0
for q in questions:
    ans = st.radio(q["q"], q["options"], key=q["q"])
    if ans == q["a"]:
        score += 1

if st.button("🧠 Submit Quiz"):
    st.success(f"🎉 You scored {score} / {len(questions)}")

st.markdown("</div>", unsafe_allow_html=True)
# ----------- Weekly Report Generator ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📊 Smart Weekly Report")

if st.session_state.get("log"):
    df_log = pd.DataFrame(st.session_state.log)
    df_log["Week"] = df_log["Date"].apply(lambda x: x.isocalendar()[1])
    week_summary = df_log.groupby("Week")["Solved"].sum().reset_index()
    st.bar_chart(week_summary.set_index("Week"))

    st.write("📌 **Weekly Summary Table**")
    st.dataframe(week_summary.rename(columns={"Solved": "Total Solved"}))

    most_active = df_log.sort_values(by="Solved", ascending=False).iloc[0]
    st.info(f"🔥 Best Day: `{most_active['Date']}` with `{most_active['Solved']} problems` solved.")
else:
    st.warning("⚠️ You need to add logs first in 'Daily Practice Log'.")
st.markdown("</div>", unsafe_allow_html=True)
# ----------- Export Progress Section ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📁 Export Your Progress")

if st.session_state.get("log"):
    df_export = pd.DataFrame(st.session_state.log)

    # Export as CSV
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="cp_progress.csv", mime="text/csv")

    # Export as simple PDF-like text file
    pdf_text = "Competitive Programming Progress Report\n\n"
    for row in df_export.itertuples():
        pdf_text += f"Date: {row.Date} | Solved: {row.Solved} | Notes: {row.Notes}\n"

    st.download_button("⬇️ Download Text Summary", data=pdf_text, file_name="cp_summary.txt", mime="text/plain")
else:
    st.info("No progress to export yet. Start solving and log it first!")
st.markdown("</div>", unsafe_allow_html=True)
# ----------- Upload Previous Progress ----------- #
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("📥 Upload Previous Logs")

upload_file = st.file_uploader("📂 Upload a previous CSV log", type=["csv"])
if upload_file:
    uploaded_df = pd.read_csv(upload_file)
    for _, row in uploaded_df.iterrows():
        entry = {
            "Date": pd.to_datetime(row["Date"]).date(),
            "Solved": int(row["Solved"]),
            "Notes": row["Notes"]
        }
        st.session_state.log.append(entry)
    st.success("Previous log data imported successfully!")
st.markdown("</div>", unsafe_allow_html=True)
custom_css = """
<style>
body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f4f6f9;
    color: #333333;
}
h1, h2, h3 {
    color: #FF6B00;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background-color: #ffffff;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}
.problem-box {
    background: linear-gradient(145deg, #e6f0ff, #ffffff);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #dce3ec;
    margin-bottom: 10px;
}
button, .stDownloadButton {
    border-radius: 8px !important;
    padding: 8px 16px !important;
    background-color: #FF6B00 !important;
    color: white !important;
    font-weight: bold !important;
}
hr {
    border: 1px solid #eee;
}
textarea, input {
    border-radius: 8px !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(f"<h1>🚀 Hello, {st.session_state.user_name}!</h1>", unsafe_allow_html=True)

st.subheader("📚 Daily Practice Log")
st.subheader("📊 Weekly Insights")
st.subheader("📝 Sticky Notes")
st.subheader("🎮 CP Mini Games")
st.subheader("📥 Upload Old Logs")
st.subheader("📤 Export Progress")
