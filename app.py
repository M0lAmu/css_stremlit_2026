# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1 22:09:12 2026

@author: thato
"""

import streamlit as st
import pandas as pd
import random
from datetime import date, timedelta

# --- Page Configuration ---
st.set_page_config(page_title="Gym Bro App", page_icon="🏋️")

st.title("🏋️ The Ultimate Fitness Companion")
st.write("Your all-in-one dashboard for nutrition, training, and memes.")

# --- Sidebar: User Inputs ---
with st.sidebar:
    st.header("1. Your Stats")
    gender = st.radio("Gender", ["Male", "Female"])
    age = st.slider("Age", 15, 80, 24)
    height = st.number_input("Height (cm)", value=175, step=1)
    weight = st.number_input("Current Weight (kg)", value=75, step=1)
    
    st.header("2. Your Goals")
    goal = st.selectbox("Goal", ["Maintain Weight", "Lose Weight", "Gain Muscle"])
    activity = st.select_slider("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active"], value="Moderately Active")
    
    st.header("3. Preferences")
    diet_type = st.selectbox("Diet Type", ["Standard", "Vegetarian", "Vegan", "Keto"])
    allergies = st.multiselect("Allergies", ["Nuts", "Dairy", "Gluten", "Shellfish"])

# --- Logic: Calculator ---
# 1. BMI
height_m = height / 100
bmi = round(weight / (height_m ** 2), 1)

if bmi < 18.5: bmi_status = "Underweight"
elif 18.5 <= bmi < 25: bmi_status = "Normal"
elif 25 <= bmi < 30: bmi_status = "Overweight"
else: bmi_status = "Obese"

# 2. Calories
if gender == "Male": bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
else: bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

activity_multipliers = {"Sedentary": 1.2, "Lightly Active": 1.375, "Moderately Active": 1.55, "Very Active": 1.725}
tdee = bmr * activity_multipliers[activity]

if goal == "Lose Weight": target_calories = tdee - 500
elif goal == "Gain Muscle": target_calories = tdee + 400
else: target_calories = tdee

# --- Logic: Data Libraries (The "Brain" of the app) ---

# Simple Meal Database
meal_options = {
    "Standard": {
        "Breakfast": ["Oatmeal with Whey Protein & Berries", "3 Eggs & Toast", "Greek Yogurt Parfait"],
        "Lunch": ["Chicken Breast, Rice & Broccoli", "Turkey Sandwich", "Tuna Pasta Salad"],
        "Dinner": ["Lean Steak with Potatoes", "Salmon & Asparagus", "Beef Stir Fry"],
        "Snack": ["Protein Shake", "Apple & Peanut Butter", "Jerky"]
    },
    "Vegetarian": {
        "Breakfast": ["Oatmeal with Chia Seeds", "Greek Yogurt with Honey", "Avocado Toast with Egg"],
        "Lunch": ["Lentil Soup with Bread", "Caprese Salad", "Quinoa & Black Bean Bowl"],
        "Dinner": ["Vegetable Stir Fry with Tofu", "Spinach & Ricotta Pasta", "Veggie Burger"],
        "Snack": ["Hard Boiled Eggs", "Almonds", "Cheese Stick"]
    },
    "Vegan": {
        "Breakfast": ["Tofu Scramble", "Overnight Oats with Soy Milk", "Smoothie Bowl"],
        "Lunch": ["Chickpea Salad Sandwich", "Lentil Curry", "Falafel Wrap"],
        "Dinner": ["Tofu Stir Fry", "Vegan Chili", "Sweet Potato & Black Bean Tacos"],
        "Snack": ["Hummus & Carrots", "Mixed Nuts", "Fruit"]
    },
    "Keto": {
        "Breakfast": ["Bacon & Eggs", "Keto Coffee (Butter/MCT)", "Omelette with Cheese"],
        "Lunch": ["Chicken Caesar Salad (No Croutons)", "Tuna Salad Lettuce Wraps", "Burger Patty (No Bun)"],
        "Dinner": ["Steak & Buttered Broccoli", "Baked Salmon with Asparagus", "Zucchini Noodles with Alfredo"],
        "Snack": ["Cheese Cubes", "Pork Rinds", "Macadamia Nuts"]
    }
}

# Workout Database
workout_plans = {
    "Gain Muscle": {
        "Push (Chest/Triceps)": ["Bench Press: 3x8-12", "Overhead Press: 3x8-12", "Incline Dumbbell Press: 3x10", "Tricep Dips: 3xFailure"],
        "Pull (Back/Biceps)": ["Deadlifts: 3x5", "Lat Pulldowns: 3x10-12", "Barbell Rows: 3x8-10", "Bicep Curls: 3x12"],
        "Legs": ["Squats: 3x5-8", "Romanian Deadlifts: 3x10", "Leg Press: 3x12", "Calf Raises: 4x15"]
    },
    "Lose Weight": {
        "Full Body A": ["Goblet Squats: 3x15", "Pushups: 3xFailure", "Kettlebell Swings: 3x20", "Plank: 60s"],
        "Full Body B": ["Lunges: 3x12 per leg", "Dumbbell Rows: 3x12", "Burpees: 3x10", "Mountain Climbers: 3x30s"],
        "Cardio": ["30 min Jog", "15 min HIIT Sprints", "45 min Brisk Walk"]
    },
    "Maintain Weight": {
        "Upper": ["Bench Press: 3x10", "Pullups: 3xFailure", "Shoulder Press: 3x12"],
        "Lower": ["Squats: 3x10", "Lunges: 3x12", "Plank: 60s"],
        "Active": ["Yoga", "Hiking", "Swimming"]
    }
}

# Meme List (URLs)
meme_urls = [
    "https://i.imgflip.com/2/1e7ql7.jpg", # Doge wow
    "https://media.makeameme.org/created/gym-time-baby-5c0c9d.jpg",
    "https://i.pinimg.com/736x/21/5d/3c/215d3c5df52026ae8955294e0e470814.jpg",
    "https://sayingimages.com/wp-content/uploads/when-you-get-to-the-gym-funny-gym-meme.jpg"
]

# --- MAIN PAGE LAYOUT ---

# Create Tabs for cleaner UI
tab1, tab2, tab3, tab4 = st.tabs(["📊 Stats & Macros", "🥗 Meal Plan", "🏋️ Workout", "😂 Motivation"])

# TAB 1: STATS & MACROS
with tab1:
    col1, col2 = st.columns(2)
    col1.metric("Your BMI", f"{bmi}", delta=bmi_status)
    col2.metric("Target Calories", f"{int(target_calories)}", delta=f"{goal}")
    
    st.divider()
    st.subheader("Adjust Your Macros")
    st.info("Drag the slider to customize your protein intake!")
    
    # Macro Slider
    protein_pct = st.slider("Protein Percentage", 10, 60, 30)
    fat_pct = st.slider("Fat Percentage", 10, 60, 30)
    carb_pct = 100 - (protein_pct + fat_pct)
    
    # Error checking for slider
    if carb_pct < 0:
        st.error("⚠️ Your percentages exceed 100%! Please lower Protein or Fat.")
    else:
        # Data for chart
        macro_data = pd.DataFrame({
            "Macro": ["Protein", "Fats", "Carbs"],
            "Percentage": [protein_pct, fat_pct, carb_pct]
        })
        st.bar_chart(macro_data, x="Macro", y="Percentage", color=["#FF4B4B", "#FFA500", "#00FF00"])
        
        # Calculate Grams
        p_grams = (target_calories * (protein_pct/100)) / 4
        f_grams = (target_calories * (fat_pct/100)) / 9
        c_grams = (target_calories * (carb_pct/100)) / 4
        
        st.write(f"**Your Daily Grams:** 🥩 {int(p_grams)}g Protein | 🥑 {int(f_grams)}g Fat | 🍞 {int(c_grams)}g Carbs")

# TAB 2: MEAL PLAN
with tab2:
    st.subheader(f"Recommended {diet_type} Day of Eating")
    
    # Simple Allergy Filter Logic
    plan = meal_options[diet_type]
    
    for meal_name, foods in plan.items():
        # Pick a random meal from the list
        selection = random.choice(foods)
        
        # VERY basic allergy check (just string matching)
        warning = ""
        if "Nuts" in allergies and ("Nut" in selection or "Almond" in selection or "Peanut" in selection):
            warning = " ⚠️ (Contains Nuts! Swap this!)"
        if "Dairy" in allergies and ("Cheese" in selection or "Yogurt" in selection or "Whey" in selection):
            warning = " ⚠️ (Contains Dairy! Swap this!)"
        if "Gluten" in allergies and ("Bread" in selection or "Toast" in selection or "Pasta" in selection):
            warning = " ⚠️ (Contains Gluten! Swap this!)"

        st.write(f"**{meal_name}:** {selection} {warning}")
    
    st.caption("*Note: This is a generated sample plan. Consult a nutritionist.*")

# TAB 3: WORKOUT
with tab3:
    st.subheader(f"Plan for: {goal}")
    
    current_plan = workout_plans[goal]
    
    for day, exercises in current_plan.items():
        with st.expander(day, expanded=True): # Expanders look like cards
            for ex in exercises:
                st.write(f"- {ex}")

# TAB 4: MOTIVATION (MEMES)
with tab4:
    st.subheader("Lightweight Baby! 🟢")
    
    if st.button("Generate New Motivation"):
        meme = random.choice(meme_urls)
        st.image(meme, caption="You got this!", use_container_width=True)
    else:
        st.write("Click the button for a boost!")
    
    st.write("### Gym Bro Wisdom:")
    quotes = [
        "The only bad workout is the one that didn't happen.",
        "Sore today, strong tomorrow.",
        "Sweat is just fat crying.",
        "Excuse me, do you have a permit for those guns? 💪"
    ]
    st.info(random.choice(quotes))
