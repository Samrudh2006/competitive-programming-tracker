import streamlit as st
import pandas as pd
import datetime
import random
import time
from PIL import Image

# Page setup
st.set_page_config(page_title="💻 CP Tracker", layout="wide")

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "profile_pic" not in st.session_state:
    st.session_state.profile_pic = None
if "page" not in st.session_state:
    st.session_state.page = "DSA Tracker"

# ---------------- Sidebar ----------------
with st.sidebar.form("profile_form"):
    st.markdown("### 👤 Enter Profile Details")
    name_input = st.text_input("Your Name", value=st.session_state.user_name)
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.session_state.user_name = name_input.strip() or "Coder"
        st.session_state.profile_pic = profile_pic
        st.success("✅ Profile Updated!")

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

st.markdown("### 📂 Menu")
pages = [
    "DSA Tracker",
    "Submissions",
    "Progress",
    "Problems",
    "Discuss",
    "Contests",
    "Daily Goals",
    "Notebook",
    "Try New Features",
    "Settings",
    "Sign Out"
]
choice = st.radio("", pages, index=pages.index(st.session_state.page))
st.session_state.page = choice
st.markdown("---")

theme = st.radio("🖌️ Theme", ["🌞 Light", "🌙 Dark"])
if theme == "🌙 Dark":
    st.markdown("<style>body { background-color: #1e1e1e; color: #f0f0f0; }</style>", unsafe_allow_html=True)

st.header("📚 DSA Sheets")
st.markdown("""
- [Striver SDE Sheet](https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/)
- [Love Babbar Sheet](https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view)
- [GFG DSA Sheet](https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/)
- [Neetcode](https://neetcode.io/)
- [Blind 75](https://blind75.io/)
""")

# ---------------- Main Content ----------------
st.title(f"📊 {st.session_state.page}")

if st.session_state.page == "DSA Tracker":
    st.markdown("Welcome to your personalized coding progress dashboard.")
    # ... insert tracker widgets here ...

elif st.session_state.page == "Submissions":
    st.write("📝 Your Submissions")
    # ... insert submissions view here ...

elif st.session_state.page == "Progress":
    st.write("📈 Your Progress Charts")
    # ... insert progress analysis widgets here ...

elif st.session_state.page == "Problems":
    st.write("📚 Problem Bank")
    # ... link to problem lists or filters ...

elif st.session_state.page == "Discuss":
    st.write("💬 Discussion Forums (external links)")
    st.markdown("- [GeeksforGeeks Forum](https://discuss.geeksforgeeks.org/)\n- [Stack Overflow](https://stackoverflow.com/)")

elif st.session_state.page == "Contests":
    st.write("🏆 Upcoming Contests")
    # ... display contest info (static or API-based) ...

elif st.session_state.page == "Daily Goals":
    st.write("🎯 Set and track your daily/weekly goals")
    # ... include goal tracker UI ...

elif st.session_state.page == "Notebook":
    st.write("📝 Your Notes & Flashcards")
    # ... integrate notebook space ...

elif st.session_state.page == "Try New Features":
    st.write("🧪 Explore upcoming or beta features:")
    # ... list new features toggle or roadmap ...

elif st.session_state.page == "Settings":
    st.write("⚙️ Settings")
    # ... include theme choice, profile reset, export preferences ...

elif st.session_state.page == "Sign Out":
    st.write("🚪 Signing out...")
    st.session_state.user_name = ""
    st.session_state.profile_pic = None
    st.session_state.page = "DSA Tracker"
    st.experimental_rerun()

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("<center>✨ Built with ❤️ using Streamlit | Keep Coding ✨</center>", unsafe_allow_html=True)
