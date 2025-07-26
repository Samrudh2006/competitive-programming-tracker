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
# ------------------ Load Problems ------------------ #
st.header("🧠 Random 100 CP Problems")
problems_list = [
    {"name": "Two Sum", "link": "https://leetcode.com/problems/two-sum/"},
    {"name": "Reverse Linked List", "link": "https://leetcode.com/problems/reverse-linked-list/"},
    {"name": "Merge Intervals", "link": "https://leetcode.com/problems/merge-intervals/"},
    {"name": "Maximum Subarray", "link": "https://leetcode.com/problems/maximum-subarray/"},
    {"name": "Longest Substring Without Repeating Characters", "link": "https://leetcode.com/problems/longest-substring-without-repeating-characters/"},
    {"name": "Valid Parentheses", "link": "https://leetcode.com/problems/valid-parentheses/"},
    {"name": "Valid Anagram", "link": "https://leetcode.com/problems/valid-anagram/"},
    {"name": "Group Anagrams", "link": "https://leetcode.com/problems/group-anagrams/"},
    {"name": "Top K Frequent Elements", "link": "https://leetcode.com/problems/top-k-frequent-elements/"},
    {"name": "Product of Array Except Self", "link": "https://leetcode.com/problems/product-of-array-except-self/"},
    {"name": "Best Time to Buy and Sell Stock", "link": "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"},
    {"name": "Contains Duplicate", "link": "https://leetcode.com/problems/contains-duplicate/"},
    {"name": "Maximum Product Subarray", "link": "https://leetcode.com/problems/maximum-product-subarray/"},
    {"name": "Find Minimum in Rotated Sorted Array", "link": "https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/"},
    {"name": "Search in Rotated Sorted Array", "link": "https://leetcode.com/problems/search-in-rotated-sorted-array/"},
    {"name": "3Sum", "link": "https://leetcode.com/problems/3sum/"},
    {"name": "Container With Most Water", "link": "https://leetcode.com/problems/container-with-most-water/"},
    {"name": "Climbing Stairs", "link": "https://leetcode.com/problems/climbing-stairs/"},
    {"name": "Coin Change", "link": "https://leetcode.com/problems/coin-change/"},
    {"name": "Longest Increasing Subsequence", "link": "https://leetcode.com/problems/longest-increasing-subsequence/"},
    {"name": "House Robber", "link": "https://leetcode.com/problems/house-robber/"},
    {"name": "Decode Ways", "link": "https://leetcode.com/problems/decode-ways/"},
    {"name": "Unique Paths", "link": "https://leetcode.com/problems/unique-paths/"},
    {"name": "Word Break", "link": "https://leetcode.com/problems/word-break/"},
    {"name": "Combination Sum", "link": "https://leetcode.com/problems/combination-sum/"},
    {"name": "Subsets", "link": "https://leetcode.com/problems/subsets/"},
    {"name": "Number of Islands", "link": "https://leetcode.com/problems/number-of-islands/"},
    {"name": "Clone Graph", "link": "https://leetcode.com/problems/clone-graph/"},
    {"name": "Pacific Atlantic Water Flow", "link": "https://leetcode.com/problems/pacific-atlantic-water-flow/"},
    {"name": "Course Schedule", "link": "https://leetcode.com/problems/course-schedule/"},
    {"name": "Maximum Depth of Binary Tree", "link": "https://leetcode.com/problems/maximum-depth-of-binary-tree/"},
    {"name": "Invert Binary Tree", "link": "https://leetcode.com/problems/invert-binary-tree/"},
    {"name": "Diameter of Binary Tree", "link": "https://leetcode.com/problems/diameter-of-binary-tree/"},
    {"name": "Balanced Binary Tree", "link": "https://leetcode.com/problems/balanced-binary-tree/"},
    {"name": "Same Tree", "link": "https://leetcode.com/problems/same-tree/"},
    {"name": "Lowest Common Ancestor of a Binary Search Tree", "link": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/"},
    {"name": "Validate Binary Search Tree", "link": "https://leetcode.com/problems/validate-binary-search-tree/"},
    {"name": "Binary Tree Level Order Traversal", "link": "https://leetcode.com/problems/binary-tree-level-order-traversal/"},
    {"name": "Serialize and Deserialize Binary Tree", "link": "https://leetcode.com/problems/serialize-and-deserialize-binary-tree/"},
    {"name": "Kth Smallest Element in a BST", "link": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/"},
    {"name": "Longest Palindromic Substring", "link": "https://leetcode.com/problems/longest-palindromic-substring/"},
    {"name": "Palindromic Substrings", "link": "https://leetcode.com/problems/palindromic-substrings/"},
    {"name": "Count and Say", "link": "https://leetcode.com/problems/count-and-say/"},
    {"name": "Longest Common Subsequence", "link": "https://leetcode.com/problems/longest-common-subsequence/"},
    {"name": "Minimum Window Substring", "link": "https://leetcode.com/problems/minimum-window-substring/"},
    {"name": "Edit Distance", "link": "https://leetcode.com/problems/edit-distance/"},
    {"name": "Interleaving String", "link": "https://leetcode.com/problems/interleaving-string/"},
    {"name": "Word Search", "link": "https://leetcode.com/problems/word-search/"},
    {"name": "Set Matrix Zeroes", "link": "https://leetcode.com/problems/set-matrix-zeroes/"},
    {"name": "Spiral Matrix", "link": "https://leetcode.com/problems/spiral-matrix/"},
    {"name": "Rotate Image", "link": "https://leetcode.com/problems/rotate-image/"},
    {"name": "Word Ladder", "link": "https://leetcode.com/problems/word-ladder/"},
    {"name": "Jump Game", "link": "https://leetcode.com/problems/jump-game/"},
    {"name": "Trapping Rain Water", "link": "https://leetcode.com/problems/trapping-rain-water/"},
    {"name": "Minimum Path Sum", "link": "https://leetcode.com/problems/minimum-path-sum/"},
    {"name": "Unique Binary Search Trees", "link": "https://leetcode.com/problems/unique-binary-search-trees/"},
    {"name": "Gas Station", "link": "https://leetcode.com/problems/gas-station/"},
    {"name": "Candy", "link": "https://leetcode.com/problems/candy/"},
    {"name": "Reconstruct Itinerary", "link": "https://leetcode.com/problems/reconstruct-itinerary/"},
    {"name": "Merge k Sorted Lists", "link": "https://leetcode.com/problems/merge-k-sorted-lists/"},
    {"name": "LRU Cache", "link": "https://leetcode.com/problems/lru-cache/"},
    {"name": "Sliding Window Maximum", "link": "https://leetcode.com/problems/sliding-window-maximum/"},
    {"name": "Maximum Frequency Stack", "link": "https://leetcode.com/problems/maximum-frequency-stack/"},
    {"name": "Meeting Rooms", "link": "https://leetcode.com/problems/meeting-rooms/"},
    {"name": "Meeting Rooms II", "link": "https://leetcode.com/problems/meeting-rooms-ii/"},
    {"name": "Alien Dictionary", "link": "https://leetcode.com/problems/alien-dictionary/"},
    {"name": "Accounts Merge", "link": "https://leetcode.com/problems/accounts-merge/"},
    {"name": "Word Break II", "link": "https://leetcode.com/problems/word-break-ii/"},
    {"name": "The Skyline Problem", "link": "https://leetcode.com/problems/the-skyline-problem/"},
    {"name": "Basic Calculator", "link": "https://leetcode.com/problems/basic-calculator/"},
    {"name": "Expression Add Operators", "link": "https://leetcode.com/problems/expression-add-operators/"},
    {"name": "Number of Connected Components in an Undirected Graph", "link": "https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/"},
    {"name": "Graph Valid Tree", "link": "https://leetcode.com/problems/graph-valid-tree/"},
    {"name": "Accounts Merge", "link": "https://leetcode.com/problems/accounts-merge/"},
    {"name": "Implement Trie", "link": "https://leetcode.com/problems/implement-trie-prefix-tree/"},
    {"name": "Design Add and Search Words Data Structure", "link": "https://leetcode.com/problems/design-add-and-search-words-data-structure/"},
    {"name": "Longest Word in Dictionary", "link": "https://leetcode.com/problems/longest-word-in-dictionary/"},
    {"name": "Add Binary", "link": "https://leetcode.com/problems/add-binary/"},
    {"name": "Excel Sheet Column Number", "link": "https://leetcode.com/problems/excel-sheet-column-number/"},
    {"name": "Factorial Trailing Zeroes", "link": "https://leetcode.com/problems/factorial-trailing-zeroes/"},
    {"name": "Power of Two", "link": "https://leetcode.com/problems/power-of-two/"},
    {"name": "Roman to Integer", "link": "https://leetcode.com/problems/roman-to-integer/"},
    {"name": "Integer to Roman", "link": "https://leetcode.com/problems/integer-to-roman/"},
    {"name": "Valid Sudoku", "link": "https://leetcode.com/problems/valid-sudoku/"},
    {"name": "Sudoku Solver", "link": "https://leetcode.com/problems/sudoku-solver/"},
    {"name": "Spiral Matrix II", "link": "https://leetcode.com/problems/spiral-matrix-ii/"},
    {"name": "Text Justification", "link": "https://leetcode.com/problems/text-justification/"},
    {"name": "Wildcard Matching", "link": "https://leetcode.com/problems/wildcard-matching/"},
    {"name": "Regular Expression Matching", "link": "https://leetcode.com/problems/regular-expression-matching/"},
    {"name": "Sudoku Solver", "link": "https://leetcode.com/problems/sudoku-solver/"},
    {"name": "Zigzag Conversion", "link": "https://leetcode.com/problems/zigzag-conversion/"}
]

import pandas as pd
import random

df = pd.DataFrame(problems)

# Random sample of 100 problems (or all if <100)
if len(df) > 100:
    df_sample = df.sample(n=100)
else:
    df_sample = df

solved = st.multiselect("✅ Tick the problems you solved", df_sample['Problem Name'])

# Show progress bar
st.progress(len(solved)/len(df_sample))
st.write(f"**{len(solved)} / {len(df_sample)} problems solved**")

# Show problem list
with st.expander("📄 View Problem List"):
    for index, row in df_sample.iterrows():
        st.markdown(f"🔹 [{row['Problem Name']}]({row['Link']})")


    


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

