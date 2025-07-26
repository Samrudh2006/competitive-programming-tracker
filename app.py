import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="CP Tracker", layout="wide")

# ---------------- Sidebar: User Info ----------------
st.sidebar.header("👤 My Profile")
name = st.sidebar.text_input("Enter your name")
profile_pic = st.sidebar.file_uploader("Upload Profile Picture", type=["jpg", "png"])

if profile_pic:
    st.sidebar.image(profile_pic, width=100)
else:
    st.sidebar.image("https://avatars.githubusercontent.com/u/9919?s=200&v=4", width=100)

# ---------------- Sidebar: Theme Toggle ----------------
theme_mode = st.sidebar.radio("🌗 Theme", ["Light", "Dark"])
if theme_mode == "Dark":
    st.markdown("""
        <style>
        body {
            background-color: #0f1117;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #161a25;
        }
        .stButton>button {
            background-color: teal;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------------- Sidebar: DSA Sheets ----------------
st.sidebar.header("📚 DSA Sheets")
st.sidebar.markdown("- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)")
st.sidebar.markdown("- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)")
st.sidebar.markdown("- [GFG Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)")
st.sidebar.markdown("- [Blind 75](https://blind75.io/)")
st.sidebar.markdown("- [Neetcode](https://neetcode.io/)")

# ---------------- Main Title ----------------
st.title("🚀 Competitive Programming Tracker")
if name:
    st.subheader(f"Welcome, {name}!")

# ------------------ 🔥 Top Daily Coding Challenges ------------------ #
st.header("🔥 Top Daily Coding Challenges")

daily_problems = [
    {"Problem Name": "Two Sum", "Link": "https://leetcode.com/problems/two-sum/"},
    {"Problem Name": "Valid Parentheses", "Link": "https://leetcode.com/problems/valid-parentheses/"},
    {"Problem Name": "Merge Two Sorted Lists", "Link": "https://leetcode.com/problems/merge-two-sorted-lists/"},
    {"Problem Name": "Best Time to Buy and Sell Stock", "Link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
    {"Problem Name": "Linked List Cycle", "Link": "https://leetcode.com/problems/linked-list-cycle/"},
    {"Problem Name": "Binary Tree Level Order Traversal", "Link": "https://leetcode.com/problems/binary-tree-level-order-traversal/"},
    {"Problem Name": "Maximum Depth of Binary Tree", "Link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
    {"Problem Name": "Symmetric Tree", "Link": "https://leetcode.com/problems/symmetric-tree/"},
    {"Problem Name": "Climbing Stairs", "Link": "https://leetcode.com/problems/climbing-stairs/"},
    {"Problem Name": "Invert Binary Tree", "Link": "https://leetcode.com/problems/invert-binary-tree/"}
]

# Pick 5 random daily problems
import random
daily_selection = random.sample(daily_problems, 5)

daily_df = pd.DataFrame(daily_selection)
solved_today = st.multiselect("✅ Tick the ones you solved today:", daily_df['Problem Name'])

st.progress(len(solved_today)/5)
st.write(f"**{len(solved_today)} / 5 solved today**")

with st.expander("📄 View Today's Problems"):
    for problem in daily_selection:
        st.markdown(f"🔹 [{problem['Problem Name']}]({problem['Link']})")


    


# ---------------- Daily Tracker ----------------
st.header("🔥 Daily Problem Tracker")

if 'log' not in st.session_state:
    st.session_state.log = []

with st.form("log_form"):
    date = st.date_input("📅 Date", datetime.date.today())
    solved_today = st.number_input("Number of problems solved today", min_value=0)
    notes = st.text_area("📝 Notes (optional)")
    submit = st.form_submit_button("Add Entry")
    if submit:
        st.session_state.log.append({'Date': date, 'Solved': solved_today, 'Notes': notes})
        st.success("✅ Entry saved!")

if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    st.line_chart(df_log.set_index("Date")["Solved"])
    with st.expander("📘 View Daily Log"):
        st.dataframe(df_log)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("🛠️ Built with ❤️ by the CP Community | [GitHub](https://github.com/)")

