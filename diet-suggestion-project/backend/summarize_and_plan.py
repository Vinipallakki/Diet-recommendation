from backend.analyze_with_gemini import setup_gemini, query_gemini
import json
from datetime import date

def create_prompt(food_data):
    def convert(obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return str(obj)

    cleaned_data = [{k: convert(v) for k, v in row.items()} for row in food_data]

    return f"""
    Based on the following weekly diet data:
    {json.dumps(cleaned_data, indent=2)}

    1. Summarize how much protein, vitamins, and nutrients the user took this week.
    2. Is this sufficient based on their BMI, current weight, and goal weight?
    3. Provide a suggested diet plan for next week with meals for each day.
    4. If user is Vinod consider Veg and he need only 2 meal a day and he need only on Monady,friday and saturday
    5. If user is Shilpa consider the Veg and Egg i need it in table format
    6. If user is Vini Consider non veg
    7. I need to these summary in  mail pattern to send client.
    """

def analyze_diet_and_plan(food_data):
    model_url = setup_gemini()
    prompt = create_prompt(food_data)
    return query_gemini(model_url, prompt)
