import google.generativeai as genai
import matplotlib.pyplot as plt
import pandas as pd
import json

# ---------------- CONFIG ----------------
API_KEY = "YOUR_ACTUAL_GOOGLE_API_KEY"  # Replace with your real key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- USER INPUT ----------------
sport = "Basketball"
position = "Guard"
goal = "Build stamina"
injury = "None"
diet = "No Preference"

feature = "Full Workout Plan"  # Options: Full Workout Plan, Recovery & Injury-Safe Training, Weekly Nutrition Plan, Warm-up & Cooldown Routine, Tactical Improvement Tips

# ---------------- PROMPT LOGIC ----------------
def build_prompt(feature):
    base = f"""
You are a professional sports coach.

Athlete Profile:
Sport: {sport}
Position: {position}
Goal: {goal}
Injury/Risk Area: {injury}
Diet Preference: {diet}

Follow safe training practices. Avoid medical diagnosis.

Output 7 entries for the week (Monday to Sunday) as JSON.
Format each entry as:
{{"Day": "Monday", "Workout": "Squats, Push-ups", "Intensity": 70}}

Do NOT include any text outside JSON.
"""
    prompts = {
        "Full Workout Plan": base,
        "Recovery & Injury-Safe Training": base.replace("Workout", "Recovery Routine"),
        "Weekly Nutrition Plan": base.replace("Workout", "Meals"),
        "Warm-up & Cooldown Routine": base.replace("Workout", "Warm-up & Cooldown"),
        "Tactical Improvement Tips": base.replace("Workout", "Tactical Tips")
    }
    return prompts[feature]

# ---------------- GENERATION ----------------
try:
    print("Generating plan...")
    response = model.generate_content(
        build_prompt(feature),
        generation_config={"temperature":0.3, "max_output_tokens":800}
    )

    # Parse JSON
    plan_data = json.loads(response.text)
    df = pd.DataFrame(plan_data)

    # Show table
    print("\n📋 Weekly Plan Table:")
    print(df.to_string(index=False))

    # Show / save graph if Intensity exists
    if "Intensity" in df.columns:
        plt.figure(figsize=(10,5))
        plt.plot(df["Day"], df["Intensity"], marker="o", linestyle="-", color="orange")
        plt.xlabel("Day")
        plt.ylabel("Intensity")
        plt.title("📈 Weekly Training Load")
        plt.ylim(0, 100)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("weekly_intensity.png")  # Saves the graph as a file
        print("\nGraph saved as 'weekly_intensity.png' in your folder.")

except Exception as e:
    print(f"Error: {str(e)}")

