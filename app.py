import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Competitive Programming Tracker", layout="wide")

# --- Header ---
st.title("💻 Competitive Programming Tracker")
st.markdown("Track your DSA journey and maintain your daily streaks like a pro!")

# --- Sidebar: User Profile ---
st.sidebar.title("👤 User Profile")
st.sidebar.text_input("Name", key="name")
st.sidebar.text_input("Email", key="email")
st.sidebar.date_input("Start Date", key="start_date")

# --- Load problems from DSA sheet (example simulated dataset) ---
if "dsa_problems" not in st.session_state:
    st.session_state.dsa_problems = pd.DataFrame({
        "Problem": ["Two Sum", "Reverse Linked List", "Merge Intervals", "LRU Cache", "Max Subarray"],
        "Source": ["Striver", "Babbar", "Striver", "GFG", "Babbar"],
        "Link": [
            "https://leetcode.com/problems/two-sum/",
            "https://leetcode.com/problems/reverse-linked-list/",
            "https://leetcode.com/problems/merge-intervals/",
            "https://practice.geeksforgeeks.org/problems/lru-cache/1",
            "https://leetcode.com/problems/maximum-subarray/"
        ],
        "Solved": [False]*5
    })

# --- Daily Log Form ---
st.subheader("📅 Daily Problem Log")

if "log" not in st.session_state:
    st.session_state.log = []

with st.form("log_form"):
    date = st.date_input("Date", value=datetime.date.today())
    problems_solved = st.number_input("Problems Solved", min_value=0, max_value=100)
    notes = st.text_input("Notes")
    submitted = st.form_submit_button("Add Entry")
    if submitted:
        st.session_state.log.append({"Date": date, "Solved": problems_solved, "Notes": notes})
        st.success("Entry added successfully!")

# --- Streak and Summary ---
st.subheader("🔥 Streak & Summary")
if st.session_state.log:
    df = pd.DataFrame(st.session_state.log)
    df_sorted = df.sort_values("Date")
    df_sorted["Date"] = pd.to_datetime(df_sorted["Date"])
    df_sorted = df_sorted.drop_duplicates("Date", keep="last")
    df_sorted = df_sorted.reset_index(drop=True)

    streak = 1
    for i in range(len(df_sorted)-1, 0, -1):
        delta = (df_sorted.loc[i, "Date"] - df_sorted.loc[i-1, "Date"]).days
        if delta == 1:
            streak += 1
        else:
            break
    st.metric(label="🔥 Current Streak (days)", value=streak)
    st.bar_chart(df_sorted.set_index("Date")["Solved"])
else:
    st.info("No logs yet. Start adding your daily progress!")

# --- Full Log Table ---
st.subheader("📖 Full Problem Solving Log")
if st.session_state.log:
    st.dataframe(pd.DataFrame(st.session_state.log))

# --- DSA Sheets Section ---
st.subheader("📚 DSA Sheets (Striver, Babbar, GFG)")

st.markdown("**🔗 [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)**")
st.markdown("**🔗 [Love Babbar 450 Sheet (PDF)](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)**")
st.markdown("**🔗 [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)**")
st.markdown("**📥 [Download Excel Sheet with Problem Links](sandbox:/mnt/data/DSA_Sheets_Links.xlsx)**")

# --- Problem Tracker ---
st.subheader("✅ DSA Problem Progress Tracker")
df_dsa = st.session_state.dsa_problems
for i, row in df_dsa.iterrows():
    df_dsa.at[i, "Solved"] = st.checkbox(f"{row['Problem']} ({row['Source']})", value=row["Solved"], key=f"solved_{i}")
    st.markdown(f"[🔗 Open Problem]({row['Link']})")

# --- Progress Bar ---
total = len(df_dsa)
solved = df_dsa["Solved"].sum()
progress = int((solved / total) * 100)

st.progress(progress / 100)
st.success(f"{solved}/{total} problems solved! ({progress}%)")

# --- Weekly/Daily Goal Setting ---
st.subheader("🎯 Set Your Solving Goals")
daily_goal = st.number_input("Daily Goal (problems)", value=2)
weekly_goal = st.number_input("Weekly Goal (problems)", value=14)

st.info(f"Try to solve {daily_goal} problems today and {weekly_goal} problems this week!")

# --- Footer ---
st.markdown("""
---
Made with ❤️ by Samrudh. Powered by Streamlit.
""")
