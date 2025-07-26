import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Competitive Programming Tracker", layout="centered")
st.title("🏁 Competitive Programming Tracker")

DATA_FILE = "problems.csv"

def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["Problem Name", "Platform", "Difficulty", "Status"])
        df.to_csv(DATA_FILE, index=False)
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

st.sidebar.header("➕ Add New Problem")
with st.sidebar.form(key="add_form"):
    name = st.text_input("Problem Name")
    platform = st.selectbox("Platform", ["LeetCode", "Codeforces", "GFG", "HackerRank", "Other"])
    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
    status = st.selectbox("Status", ["Pending", "Solved"])
    submit = st.form_submit_button("Add Problem")

    if submit and name:
        df.loc[len(df.index)] = [name, platform, difficulty, status]
        save_data(df)
        st.success("✅ Problem added!")

st.header("📋 Your Problems List")

filter_status = st.multiselect("Filter by Status", options=["Pending", "Solved"], default=["Pending", "Solved"])
filter_difficulty = st.multiselect("Filter by Difficulty", options=["Easy", "Medium", "Hard"], default=["Easy", "Medium", "Hard"])

filtered_df = df[(df["Status"].isin(filter_status)) & (df["Difficulty"].isin(filter_difficulty))]

st.dataframe(filtered_df, use_container_width=True)

if st.button("Clear All Data ❌"):
    df = df.iloc[0:0]
    save_data(df)
    st.warning("All data cleared!")
