import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# --- CONFIGURATION ---
st.set_page_config(page_title="Personal Growth Dashboard", layout="wide")

# Initialize data in session state (Simulating a database)
if 'habits' not in st.session_state:
    st.session_state.habits = pd.DataFrame({
        'Habit': ['Drink Water', 'Exercise', 'Reading', 'Meditation'],
        'Target': [30, 30, 30, 30],
        'Done': [0, 0, 0, 0]
    })

if 'goals' not in st.session_state:
    st.session_state.goals = []

# --- SIDEBAR NAVIGATION ---
page = st.sidebar.radio("Navigate", ["Habit Tracker", "Goal Planner"])

# --- PAGE 1: HABIT TRACKER ---
if page == "Habit Tracker":
    st.title("📅 Monthly Habit Tracker")
    
    # Global Progress Logic
    total_possible = st.session_state.habits['Target'].sum()
    total_done = st.session_state.habits['Done'].sum()
    progress = total_done / total_possible if total_possible > 0 else 0
    
    st.metric("Overall Success Rate", f"{int(progress * 100)}%")
    st.progress(progress)

    # Habit Grid
    st.subheader("Your Habits")
    edited_df = st.data_editor(
        st.session_state.habits,
        column_config={
            "Done": st.column_config.ProgressColumn(
                "Progress", help="Days completed this month",
                min_value=0, max_value=30, format="%d days"
            ),
        },
        num_rows="dynamic"
    )
    st.session_state.habits = edited_df

# --- PAGE 2: GOAL PLANNER ---
elif page == "Goal Planner":
    st.title("🎯 Goal Planner & Areas of Life")
    
    # Area of Life Selector (from your Excel categories)
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Add New Goal")
        category = st.selectbox("Area of Life", [
            "Health & Fitness 🧘‍♀️", "Career Growth 💼", 
            "Finances & Wealth 💰", "Relationships 🤝", 
            "Adventure & Travel ✈️"
        ])
        goal_name = st.text_input("What is the goal?")
        why = st.text_area("Why is this important?")
        deadline = st.date_input("Deadline")
        
        if st.button("Add Goal"):
            st.session_state.goals.append({
                "Category": category,
                "Goal": goal_name,
                "Why": why,
                "Deadline": deadline,
                "Status": "▶️ In Progress"
            })

    with col2:
        st.subheader("Current Goals")
        if st.session_state.goals:
            for i, g in enumerate(st.session_state.goals):
                days_left = (g['Deadline'] - datetime.now().date()).days
                with st.expander(f"{g['Status']} - {g['Goal']} ({g['Category']})"):
                    st.write(f"**The Why:** {g['Why']}")
                    st.write(f"**Deadline:** {g['Deadline']} ({max(0, days_left)} days left)")
                    new_status = st.selectbox("Update Status", 
                                            ["❌ Not Started", "▶️ In Progress", "✔️ Achieved"], 
                                            key=f"status_{i}")
                    st.session_state.goals[i]['Status'] = new_status
        else:
            st.info("No goals added yet. Start planning!")
