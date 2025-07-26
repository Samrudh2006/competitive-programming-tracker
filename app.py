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

# ---------------- Load & Display Problems ----------------
st.header("🧠 100 Random CP Problems")

try:
    df_all = pd.read_csv("problems.csv")
    if len(df_all) < 100:
        st.error("❌ problems.csv must have at least 100 entries!")
    else:
        df_100 = df_all.sample(n=100, random_state=42).reset_index(drop=True)
        solved = st.multiselect("✅ Select problems you've solved:", df_100['Problem Name'])
        st.progress(len(solved) / 100)
        st.write(f"**{len(solved)} / 100 problems solved**")

        with st.expander("📄 View All 100 Problems"):
            for i, row in df_100.iterrows():
                st.markdown(f"**{i+1}. [{row['Problem Name']}]({row['Link']})**")
                st.markdown("---")

except Exception as e:
    st.error(f"⚠️ Error loading problems.csv: {e}")

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

