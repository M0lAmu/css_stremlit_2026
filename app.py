# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 22:09:12 2026

@author: thato
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta # New library for date math

# --- Page Configuration ---
st.set_page_config(page_title="Fitness Visualizer", page_icon="💪")

st.title("💪 Personal Fitness & BMI Visualizer")
st.write("Enter your details to get a personalized health snapshot.")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Your Stats")
    gender = st.radio("Gender", ["Male", "Female"])
    age = st.slider("Age", 15, 80, 25)
    height = st.number_input("Height (cm)", value=170, step=1)
    weight = st.number_input("Current Weight (kg)", value=70, step=1)
    
    # NEW: Goal Weight Input
    target_weight = st.number_input("Goal Weight (kg)", value=75, step=1)
    
    activity = st.select_slider(
        "Activity Level",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
        value="Moderately Active"
    )

    goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])

# --- Calculations ---
# 1. BMI Logic
height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

if bmi < 18.5:
    bmi_category = "Underweight"
    bmi_color = "blue"
elif 18.5 <= bmi < 25:
    bmi_category = "Normal Weight"
    bmi_color = "green"
elif 25 <= bmi < 30:
    bmi_category = "Overweight"
    bmi_color = "orange"
else:
    bmi_category = "Obese"
    bmi_color = "red"

# 2. BMR & TDEE Logic
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
tdee = bmr * activity_multipliers[activity]

if goal == "Lose Weight":
    target_calories = tdee - 500
    weekly_change = -0.5 # kg per week
elif goal == "Gain Muscle":
    target_calories = tdee + 400
    weekly_change = 0.25 # kg per week (muscle gain is slower)
else:
    target_calories = tdee
    weekly_change = 0

# --- Display Section ---

# Row 1: BMI & Calories
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your BMI")
    st.metric(label="Body Mass Index", value=bmi, delta=bmi_category)

with col2:
    st.subheader("Daily Calories")
    st.metric(label="Target Intake", value=f"{int(target_calories)} kcal")
    st.write(f"To **{goal.lower()}**.")

# --- NEW FEATURE 1: Time to Goal Predictor ---
st.divider()
st.subheader("📅 Time to Goal Prediction")

weight_diff = target_weight - weight

if weight_diff == 0:
    st.success("You are already at your target weight!")
elif (weight_diff > 0 and goal == "Lose Weight") or (weight_diff < 0 and goal == "Gain Muscle"):
    st.warning("Your target weight conflicts with your selected goal (Lose/Gain). Check your settings!")
else:
    # Calculate weeks needed
    if weekly_change != 0:
        weeks_needed = abs(weight_diff / weekly_change)
        # Calculate future date
        goal_date = date.today() + timedelta(weeks=weeks_needed)
        
        st.write(f"Based on a safe rate of **{abs(weekly_change)} kg/week**:")
        
        # Display as a timeline metric
        c1, c2 = st.columns(2)
        c1.metric("Weeks to Goal", f"{int(weeks_needed)} weeks")
        c2.metric("Estimated Date", goal_date.strftime("%d %b %Y"))
        
        # Simple progress bar visualization
        progress = 0
        st.progress(progress) # In a real app, you'd calculate % complete
    else:
        st.info("Select 'Lose Weight' or 'Gain Muscle' to see a timeline.")

# --- Original Feature: Food Visualization ---
st.divider()
st.subheader("🍕 What does that look like in food?")
pizza_slices = target_calories / 285
burgers = target_calories / 550

tab1, tab2 = st.tabs(["🍕 In Pizza", "🍔 In Burgers"])
with tab1:
    st.write(f"Your daily limit is roughly **{pizza_slices:.1f} slices** of pepperoni pizza.")
    chart_data = pd.DataFrame({"Food": ["Your Limit", "Average Person"], "Slices": [pizza_slices, 8]})
    st.bar_chart(chart_data, x="Food", y="Slices", color="#FF9900")
with tab2:
    st.write(f"Your daily limit is roughly **{burgers:.1f} Big Burgers**.")
    st.write("🍔 " * int(burgers))

# --- NEW FEATURE 2: Data Download ---
st.divider()

# Create a string for the report
report_text = f"""
FITNESS REPORT
--------------
Date: {date.today()}
Profile: {gender}, {age} years old
Height: {height} cm | Weight: {weight} kg
BMI: {bmi} ({bmi_category})
Goal: {goal} -> Target: {target_weight} kg
Daily Calories: {int(target_calories)} kcal
"""

st.download_button(
    label="📥 Download My Report",
    data=report_text,
    file_name="my_fitness_stats.txt",
    mime="text/plain"
)
