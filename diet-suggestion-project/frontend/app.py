import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
# from backend.summarize_and_plan import analyze_diet_and_plan
# from backend.fetch_bq_data import get_user_weekly_food_data
from backend.summarize_and_plan import analyze_diet_and_plan
from backend.fetch_bq_data import get_user_weekly_food_data



st.title("🍽️ Personalized Diet Suggestion")

# Directly fetch data without asking for user input
data = get_user_weekly_food_data(
    project_id="your project id",
    dataset="your dataset",
    table="your table name"
)

if data:
    st.subheader("📋 Weekly Summary & Next Plan")
    output = analyze_diet_and_plan(data)
    st.markdown(output)
else:
    st.warning("No data found in the table.")
