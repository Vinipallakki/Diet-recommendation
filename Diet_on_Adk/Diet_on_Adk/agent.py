# import os
# from dotenv import load_dotenv
# from google.adk import Agent
# from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
# from google.adk.tools.tool_context import ToolContext

# from a2a.types import AgentCapabilities, AgentCard, AgentSkill

# from google import genai
# from google.genai import types

# load_dotenv()

# project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
# client = genai.Client(vertexai=True,
#     project=project_id,
#     location=os.getenv("GOOGLE_CLOUD_LOCATION")
# )
# # Tools

# def generate_diet_prompt(cleaned_data):
#     return f"""
#     Based on the following weekly diet data:
#     {json.dumps(cleaned_data, indent=2)}

#     You are a professional health and nutrition AI assistant.

#     Using the provided weekly user data from a health tracker, perform the following tasks with sensitivity to missing or inconsistent data:
#     👋 **Hi [User’s Name],**

#     Hope you're doing well! 😊

#     Before we dive into the breakdown of your weekly health and nutrition summary, tell me —  
#     **how are you feeling about your progress last week?**  
#     Was it easier to stick to your meals and workouts, or did anything feel off?

#     Take a moment to reflect. We'll walk through your data together and make sure you're set for a healthier, balanced next week.

#     ---

#     ### 1. Weekly Nutrient Intake Estimation:

#     - Use total weekly `food_intake_grams` (sum of all 7 days).
#     - Calculate weekly totals as follows:

#     #### Macronutrient Breakdown:
#     - **Total Calories** = total food intake (add calories of that week)
#     - **Protein**:
#     - Formula: `Recommended Daily Protein_Intake_per_day = 1.6 × body_weight (in kg)`
#     - Weekly_Protein = Protein_Intake_per_day × 7
#     - **Fats**:
#     - Formula: `Recommended Daily Fat_Intake_per_day = 1.0 × body_weight (in kg)`
#     - Weekly_Fat = Fat_Intake_per_day × 7
#     - **Carbohydrates** = Remaining grams after subtracting protein and fats from total food intake


#     ---

#     ### 2. Weekly Macro Summary Table:

#     Summarize the **weekly estimated intake** and compare it against **recommended values**:
#     **calculate the carbs and calories based on the food item they took last week(IMP for the below calculation )

#     | Macro         | Intake (Total) | Recommended Range | % Met |
#     |---------------|----------------|-------------------|--------|
#     | Protein       |Weekly_Protein g| perday x 7 g     | yes/no    |
#     | Carbohydrates | XXX g          |(Auto-calculated) |yes/no  |
#     | Fats          | Weekly_Fat g   | perday x 7 g     | yes/no   |
#     | Calories      | XXXX kcal      | perday x7        | yes/no  |

#     > If any macro data is skipped due to missing input, mention that clearly.

#     ---

#     ### 3. Daily Meal Plan (Per Day - Monday to Sunday):

#     - Suggest 1 **Breakfast**, 1 **Lunch**, and 1 **Dinner** per day
#     - Meals must:
#     - Reflect **South Indian (Karnataka-style)** cuisine
#     - Be balanced in **protein, fats, carbs**
#     - Use `recommended_items`, `bmi`, `goal_weight`, `lifestyle`
#     - If user name is **Shilpa**, suggest **vegetarian and egg-based only** (no meat/fish)

#     ---

#     ### 4. Evening Add-ons:

#     Suggest **1 evening snack/beverage per day** under 150 kcal:
#     - Pick from: green tea, almonds, walnuts, cucumber slices, sprouts, buttermilk
#     - Rotate items across the week for variety

#     ---

#     ### 5. Weekly Exercise Plan:

#     - Use:
#     - `exercise_type`, `lifestyle`, `sleep_duration` (default: 7 hrs), and `exercise_calories` (default: 200/day)
#     - Recommend 1 activity per day:
#     - Mix of yoga, cardio, strength, walking/stretching
#     - Include **rest/recovery day(s)** if needed
#     - Ensure total calories burned in the week ≥ target

#     ---

#     ### 6. Red Flag Warnings:

#     Flag gently if:
#     - **BMI** <15 or >40
#     - **Goal weight** change >20% of current weight
#     - **Age** <14 or >80    

#     > Kindly advise: “Please consult a healthcare provider for a safe and effective plan.”

#     ---

#     ### 7. Motivational Quote:

#     End with a warm, culturally uplifting quote like:

#     > _“Your body deserves the best. Small steps today, big results tomorrow.”_

#     ---

#     💡 **Notes**:
#     - Ignore daily breakdown tables — use weekly totals only
#     - Mention “data not available” for any missing required field
#     - Format all output cleanly using **Markdown tables and headings**
#     - Be professional and supportive — **do not write like an email**
#     """


# # Agents

# root_agent = Agent(
#     name="Diet_on_Adk",
#     model=os.getenv("MODEL"),
#     description="Suggest the food pattern for next week.",
#     instruction="""
#     You are a professional health and nutrition AI assistant.
#     """,
#     tools=[generate_diet_prompt]
# )

import os
import json
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext

from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from google import genai
from google.genai import types
from google.cloud import bigquery

# -------------------
# Load Environment
# -------------------
load_dotenv()

project_id = "gen-lang-client-0224588610"
dataset = "first"
table = "shilpa"
location = os.getenv("GOOGLE_CLOUD_LOCATION")  # e.g. "us-central1"

client = genai.Client(
    vertexai=True,
    project=project_id,
    location=location
)


# -------------------
# Instruction Prompt
# -------------------
def prompt_diet():
    return """You are a professional health and nutrition AI assistant.

Using the provided weekly user data from a health tracker, perform the following tasks with sensitivity to missing or inconsistent data:
👋 **Hi [User’s Name],**
Ask the user name first and then say wish them good day
like
Hope you're doing well! 😊

Before we dive into the breakdown of your weekly health and nutrition summary, tell me —  
**how are you feeling about your progress last week?**  
Was it easier to stick to your meals and workouts, or did anything feel off?

Take a moment to reflect. We'll walk through your data together and make sure you're set for a healthier, balanced next week.

---
Please refer these data from the Bigquery table refer this function "get_user_weekly_food_data":

### 1. Weekly Nutrient Intake Estimation:

- Use total weekly `food_intake_grams` (sum of all 7 days).
- Calculate weekly totals as follows:

#### Macronutrient Breakdown:
- **Total Calories** = total food intake (add calories of that week)
- **Protein**:
  Formula: `Recommended Daily Protein_Intake_per_day = 1.6 × body_weight (in kg)`
  Weekly_Protein = Protein_Intake_per_day × 7
- **Fats**:
  Formula: `Recommended Daily Fat_Intake_per_day = 1.0 × body_weight (in kg)`
  Weekly_Fat = Fat_Intake_per_day × 7
- **Carbohydrates** = Remaining grams after subtracting protein and fats from total food intake

---

### 2. Weekly Macro Summary Table:

Summarize the **weekly estimated intake** and compare it against **recommended values**.  
**calculate the carbs and calories based on the food item they took last week (IMP for the below calculation)**

| Macro         | Intake (Total) | Recommended Range | % Met |
|---------------|----------------|-------------------|-------|
| Protein       | Weekly_Protein g | perday x 7 g     | yes/no |
| Carbohydrates | XXX g            | (Auto-calculated) | yes/no |
| Fats          | Weekly_Fat g     | perday x 7 g     | yes/no |
| Calories      | XXXX kcal        | perday x 7       | yes/no |

> If any macro data is skipped due to missing input, mention that clearly.

---

### 3. Daily Meal Plan (Per Day - Monday to Sunday):

- Suggest 1 **Breakfast**, 1 **Lunch**, and 1 **Dinner** per day
- Meals must:
    - Reflect **South Indian (Karnataka-style)** cuisine
    - Be balanced in **protein, fats, carbs**
    - Use `recommended_items`, `bmi`, `goal_weight`, `lifestyle`
    - If user name is **Shilpa**, suggest **vegetarian and egg-based only** (no meat/fish)

---

### 4. Evening Add-ons:

Suggest **1 evening snack/beverage per day** under 150 kcal:
- Pick from: green tea, almonds, walnuts, cucumber slices, sprouts, buttermilk
- Rotate items across the week for variety

---

### 5. Weekly Exercise Plan:

- Use:
    - `exercise_type`, `lifestyle`, `sleep_duration` (default: 7 hrs), and `exercise_calories` (default: 200/day)
- Recommend 1 activity per day:
    - Mix of yoga, cardio, strength, walking/stretching
    - Include **rest/recovery day(s)** if needed
    - Ensure total calories burned in the week ≥ target

---

### 6. Red Flag Warnings:

Flag gently if:
- **BMI** <15 or >40
- **Goal weight** change >20% of current weight
- **Age** <14 or >80    

> Kindly advise: “Please consult a healthcare provider for a safe and effective plan.”

---

### 7. Motivational Quote:

End with a warm, culturally uplifting quote like:

> _“Your body deserves the best. Small steps today, big results tomorrow.”_

---

💡 **Notes**:
- Ignore daily breakdown tables — use weekly totals only
- Mention “data not available” for any missing required field
- Format all output cleanly using **Markdown tables and headings**
- Be professional and supportive — **do not write like an email**
"""


# -------------------
# BigQuery Fetcher
# -------------------
def get_user_weekly_food_data(project_id, dataset, table):
    client_bq = bigquery.Client(project=project_id)
    query = f"""
        SELECT *
        FROM `{project_id}.{dataset}.{table}`
        ORDER BY recorded_date DESC
        LIMIT 7
    """
    query_job = client_bq.query(query)
    results = [dict(row) for row in query_job.result()]
    return results


# -------------------
# Prompt Builder
# -------------------
def build_diet_prompt(cleaned_data: list[dict]) -> str:
    return f"""
    Based on the following weekly diet data:
    {json.dumps(cleaned_data, indent=2)}

    You are a professional health and nutrition AI assistant.

    (Same detailed instructions as in prompt_diet...)
    """


# -------------------
# Agent
# -------------------
root_agent = Agent(
    name="Diet_on_Adk",
    model=os.getenv("MODEL"),
    description="Suggest the food pattern for next week.",
    instruction=prompt_diet(),
)


# -------------------
# Main Execution
# -------------------
if __name__ == "__main__":
    # Step 1: Fetch weekly data
    weekly_data = get_user_weekly_food_data(project_id, dataset, table)

    if not weekly_data:
        print("⚠️ No data found in BigQuery for this user.")
    else:
        # Step 2: Build the diet prompt
        diet_prompt = build_diet_prompt(weekly_data)

        # Step 3: Run the agent with generated prompt
        response = root_agent.run(diet_prompt)
        print(response)
