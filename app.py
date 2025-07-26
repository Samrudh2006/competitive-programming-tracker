# NOTE: This version removes Streamlit dependency for environments where it isn't available.
# It prints logs and progress via standard output (console-based simulation).
# This version also avoids using `input()` to ensure compatibility with sandboxed environments.

import pandas as pd
import datetime
import random
import time
import matplotlib.pyplot as plt
import io

# --- Mocked Session State ---
class SessionState:
    def __init__(self):
        self.user_name = "Coder"
        self.log = []
        self.starred_notes = []
        self.timer_sessions = []
        self.topics = {}

st = SessionState()

# --- Input Substitution ---
def simulate_input(prompt, fallback):
    print(f"{prompt} [Auto: {fallback}]")
    return fallback

# --- Functions for Console Mode ---
def show_dashboard():
    print(f"\n=== DASHBOARD for {st.user_name} ===")
    if st.log:
        df = pd.DataFrame(st.log)
        print("\n📘 Log:")
        print(df)

        print("\n📊 Weekly Progress Chart")
        df.set_index("Date")["Solved"].plot(title="Problems Solved Per Day")
        plt.show()

        if st.topics:
            print("\n📊 Topics Pie Chart")
            fig, ax = plt.subplots()
            ax.pie(st.topics.values(), labels=st.topics.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            plt.title("Most Solved Topics")
            plt.show()

    weekly_goal = 35
    this_week = datetime.date.today().isocalendar()[1]
    solved_this_week = sum(i["Solved"] for i in st.log if pd.to_datetime(i["Date"]).isocalendar()[1] == this_week)
    print(f"\nWeekly Progress: {solved_this_week}/{weekly_goal}")

    if solved_this_week >= weekly_goal:
        print("🎉 Excellent! You've met your weekly goal!")
    elif solved_this_week >= weekly_goal * 0.75:
        print("💪 Almost there! Keep going!")
    else:
        print("🚀 Push a little more to hit your weekly target!")

def add_daily_log():
    print("\n=== Add Daily Log ===")
    date = simulate_input("Date (YYYY-MM-DD):", str(datetime.date.today()))
    count = int(simulate_input("Problems Solved:", "3"))
    notes = simulate_input("Notes:", "Solved 3 problems")
    tags = simulate_input("Tags (comma-separated):", "arrays")
    starred = simulate_input("Starred? (y/n):", "y").lower() == 'y'

    entry = {"Date": date, "Solved": count, "Notes": notes}
    st.log.append(entry)
    if starred:
        st.starred_notes.append(entry)
    for tag in [t.strip() for t in tags.split(",") if t.strip()]:
        st.topics[tag] = st.topics.get(tag, 0) + count
    print("Log Added!")

def focus_mode():
    print("\n=== Focus Mode ===")
    minutes = int(simulate_input("Focus time in minutes (e.g., 25):", "1"))
    print("Timer started...")
    start_time = datetime.datetime.now()
    try:
        for i in range(minutes * 60, 0, -1):
            if i % 60 == 0:
                print(f"Time left: {i//60} min")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Timer interrupted.")
    end_time = datetime.datetime.now()
    st.timer_sessions.append((start_time, end_time))
    print("⏰ Session complete!")

def export_log():
    print("\n=== Exporting Log to CSV ===")
    if st.log:
        df = pd.DataFrame(st.log)
        filename = "cp_log.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Log exported to {filename}")
    else:
        print("❌ No data to export.")

def settings():
    print("\n=== Daily Random Challenge ===")
    sheet_links = [
        ("Striver SDE", "https://takeuforward.org/interviews/strivers-sde-sheet-top-coding-interview-problems/"),
        ("Love Babbar", "https://drive.google.com/file/d/1W8hwhfvd7bJqF1DYFFJ5cu_yq1OQ_L1D/view"),
        ("GFG Sheet", "https://www.geeksforgeeks.org/dsa-sheet-by-love-babbar/"),
        ("Neetcode", "https://neetcode.io/"),
        ("Blind 75", "https://blind75.io/")
    ]
    rand = random.choice(sheet_links)
    print(f"Try something new from: {rand[0]} - {rand[1]}")

    quotes = [
        "“Consistency is what transforms average into excellence.”",
        "“The expert in anything was once a beginner.”",
        "“Code more. Fear less.”",
        "“Success is the sum of small efforts repeated daily.”"
    ]
    print("💡 Motivation: " + random.choice(quotes))

def menu():
    print("\n===== CP Tracker Console App =====")
    print("1. Dashboard")
    print("2. Daily Log")
    print("3. Focus Mode")
    print("4. Export Log")
    print("5. Settings")
    print("0. Exit")
    return simulate_input("Choose an option:", "1")  # Default to Dashboard for sandbox runs

# --- Main Loop ---
for _ in range(1):  # Loop only once in sandboxed mode
    choice = menu()
    if choice == '1':
        show_dashboard()
    elif choice == '2':
        add_daily_log()
    elif choice == '3':
        focus_mode()
    elif choice == '4':
        export_log()
    elif choice == '5':
        settings()
    elif choice == '0':
        print("Exiting app. Bye!")
        break
    else:
        print("Invalid choice. Try again.")
