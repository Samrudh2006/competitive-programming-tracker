import streamlit as st
import base64
from PIL import Image

st.set_page_config(page_title="Competitive Programming Tracker", layout="wide", page_icon="✨")

# Sidebar menu
menu_options = ["🏠 Home", "📈 DSA Tracker", "📝 Submissions", "📅 Progress", "💬 Discuss", "🏁 Contests", "📓 Notebook"]
choice = st.sidebar.radio("Explore Sections", menu_options)

# User Info Submission (only shown once)
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    st.title("🚀 Welcome to Competitive Programming Tracker")
    st.subheader("Please enter your details")

    name = st.text_input("👤 Name")
    uploaded_img = st.file_uploader("Upload your profile picture", type=["jpg", "png"])
    if st.button("Submit"):
        if name:
            st.session_state.name = name
            st.session_state.submitted = True
            if uploaded_img:
                st.session_state.pic = uploaded_img
            else:
                st.session_state.pic = None
            st.success("Submitted successfully! Now explore the tracker.")
        else:
            st.warning("Please enter your name before submitting.")
else:
    # Display name and image once submitted
    if "name" in st.session_state:
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.session_state.pic:
                img = Image.open(st.session_state.pic)
                st.image(img, width=80)
        with col2:
            st.markdown(f"### 👋 Hello, **{st.session_state.name}**")
        st.markdown("---")

# Main content based on selected menu
if choice == "🏠 Home":
    st.markdown("## 🌟 Welcome to your Competitive Programming Tracker")
    st.markdown("Use the sidebar to navigate through different sections like your daily tracker, submission progress, contests, and more.")

elif choice == "📈 DSA Tracker":
    st.markdown("## 📈 DSA 30 Days Course")
    st.markdown("[🚀 Start DSA 30 Days Challenge on Unstop](https://unstop.com/dsa-30) ✨")

elif choice == "📝 Submissions":
    st.markdown("## 📊 Your LeetCode Submissions Dashboard")
    st.markdown("[🔗 Open LeetCode Profile](https://leetcode.com/dashboard) 🧠")

elif choice == "📅 Progress":
    st.markdown("## 📅 Track Your Progress")
    st.markdown("Use a notebook or dashboard to log your daily and weekly progress.")
    st.info("Coming soon: Auto progress sync!")

elif choice == "💬 Discuss":
    st.markdown("## 💬 Ask Your DSA Doubts")
    st.markdown("[📌 Ask on GFG Discuss](https://discuss.geeksforgeeks.org/) 💡")

elif choice == "🏁 Contests":
    st.markdown("## 🏁 Upcoming Contests")
    st.markdown("[🔥 Participate in LeetCode Contests](https://leetcode.com/contest/) 🏆")

elif choice == "📓 Notebook":
    st.markdown("## 📓 Your DSA Notes")
    note = st.text_area("📝 Write your notes here:")
    if st.button("💾 Save Note"):
        st.success("Note saved (not persistent in cloud).")

# Footer
st.markdown("""
    <hr style='border:1px solid #666;'>
    <center>✨ Built with ❤️ using Streamlit | Keep Coding ✨<br>By: <strong>{}</strong></center>
""".format(st.session_state.get("name", "Your Name")), unsafe_allow_html=True)
