# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 22:09:12 2026

@author: thato
"""

import streamlit as st
import pandas as pd

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
    weight = st.number_input("Weight (kg)", value=70, step=1)
    activity = st.select_slider(
        "Activity Level",
        options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active"],
        value="Moderately Active"
    )

    # Goal Selection
    goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])

# --- Calculations ---
# 1. BMI Calculation
height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

# BMI Category Logic
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

# 2. BMR (Basal Metabolic Rate) - Mifflin-St Jeor Equation
if gender == "Male":
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else:
    bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

# 3. TDEE (Total Daily Energy Expenditure)
activity_multipliers = {
    "Sedentary": 1.2,
    "Lightly Active": 1.375,
    "Moderately Active": 1.55,
    "Very Active": 1.725
}
tdee = bmr * activity_multipliers[activity]

# Adjust for Goal
if goal == "Lose Weight":
    target_calories = tdee - 500
elif goal == "Gain Muscle":
    target_calories = tdee + 400
else:
    target_calories = tdee

# --- Display Section ---

# Row 1: The Big Numbers
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your BMI")
    st.metric(label="Body Mass Index", value=bmi, delta=bmi_category)
    st.caption(f"A healthy BMI is generally between 18.5 and 24.9.")

with col2:
    st.subheader("Daily Calories")
    st.metric(label="Target Intake", value=f"{int(target_calories)} kcal")
    st.write(f"To **{goal.lower()}** based on your activity.")

# Row 2: Fun Visuals (The "Pizza" conversion)
st.divider()
st.subheader("🍕 What does that look like in food?")

# Pizza slice approx 285 calories
pizza_slices = target_calories / 285
# Burger approx 550 calories
burgers = target_calories / 550

tab1, tab2 = st.tabs(["🍕 In Pizza", "🍔 In Burgers"])

with tab1:
    st.write(f"Your daily limit is roughly **{pizza_slices:.1f} slices** of pepperoni pizza.")
    # Simple visual bar chart using a dataframe
    chart_data = pd.DataFrame({
        "Food": ["Your Limit", "Average Person"],
        "Slices": [pizza_slices, 8] # Assuming avg person eats 8 slices? Just for comparison
    })
    st.bar_chart(chart_data, x="Food", y="Slices", color="#FF9900")

with tab2:
    st.write(f"Your daily limit is roughly **{burgers:.1f} Big Burgers**.")
    # Display emojis based on count
    st.write("🍔 " * int(burgers))

# Row 3: Macro Split (Interactive)
st.divider()
st.subheader("🥗 Recommended Macros")
st.info("You can adjust the slider to change your protein preference.")

protein_ratio = st.slider("Protein %", 10, 50, 30)
carb_ratio = (100 - protein_ratio) / 2
fat_ratio = (100 - protein_ratio) / 2

# Create a donut chart using Vega-Lite (built-in to Streamlit)
macro_data = pd.DataFrame({
    "Macro": ["Protein", "Carbs", "Fats"],
    "Percentage": [protein_ratio, carb_ratio, fat_ratio]
})

st.bar_chart(macro_data, x="Macro", y="Percentage")