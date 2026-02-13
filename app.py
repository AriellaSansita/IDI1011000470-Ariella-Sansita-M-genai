import streamlit as st
import google.generativeai as genai
import pandas as pd

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="CoachBot AI", layout="wide")
st.title("🏆 CoachBot AI - Smart Fitness Assistant")
st.write("AI-powered personalized coach for young athletes")

# ---------------- USER INPUT ----------------
sports_list = [
    "Football","Cricket","Basketball","Athletics","Badminton","Tennis",
    "Hockey","Volleyball","Kabaddi","Table Tennis","Swimming","Martial Arts","Other"
]

sport = st.selectbox("Sport", sports_list)

positions_by_sport = {
    "Football": ["Goalkeeper","Defender","Midfielder","Winger","Striker"],
    "Cricket": ["Batsman","Bowler","All-Rounder","Wicket Keeper"],
    "Basketball": ["Point Guard","Shooting Guard","Small Forward","Power Forward","Center"],
    "Athletics": ["Sprinter","Long Distance Runner","Jumper","Thrower"],
    "Badminton": ["Singles Player","Doubles Player"],
    "Tennis": ["Singles Player","Doubles Player"],
    "Hockey": ["Goalkeeper","Defender","Midfielder","Forward"],
    "Volleyball": ["Setter","Libero","Spiker","Blocker"],
    "Kabaddi": ["Raider","Defender","All-Rounder"],
    "Table Tennis": ["Singles Player","Doubles Player"],
    "Swimming": ["Freestyle Specialist","Backstroke Specialist","Butterfly Specialist"],
    "Martial Arts": ["Striker","Grappler","Mixed Fighter"]
}

if sport == "Other":
    sport = st.text_input("Enter Your Sport") or "General Sport"
    position = st.text_input("Enter Position") or "Athlete"
else:
    position = st.selectbox("Player Position", positions_by_sport.get(sport, ["Athlete"]))

injury = st.text_input("Injury History (None if no injury)")
goal = st.selectbox("Primary Goal", ["Stamina","Strength","Speed","Recovery","Skill Improvement"])
diet = st.selectbox("Diet Type", ["Vegetarian","Non-Vegetarian","Vegan"])
intensity = st.selectbox("Training Intensity", ["Low","Moderate","High"])
weakness = st.text_input("Biggest Weakness (optional)")
age = st.slider("Age", 10, 50, 15)
training_days = st.slider("Training Days / Week", 1, 7, 4)
session_duration = st.slider("Session Duration (minutes)", 20, 180, 60)

# ---------------- FEATURES ----------------
st.sidebar.header("Select Coaching Features")

all_features = [
    "Full Workout Plan",
    "Injury Recovery Plan",
    "Weekly Training Plan",
    "Stamina Builder",
    "Nutrition Plan",
    "Hydration Strategy",
    "Warm-up & Cooldown"
]

selected_features = [f for f in all_features if st.sidebar.checkbox(f, True)]

# ---------------- WORKOUT TABLE ----------------
def generate_workout_table():

    exercises = [
        {"name": "Push-ups", "type": "strength", "uses_arm": True},
        {"name": "Squats", "type": "strength", "uses_arm": False},
        {"name": "Plank", "type": "core", "uses_arm": True},
        {"name": "Lunges", "type": "strength", "uses_arm": False},
        {"name": "Jogging", "type": "cardio", "uses_arm": False},
    ]

    inj = injury.lower()
    if any(x in inj for x in ["arm","wrist","elbow","shoulder","fracture","broken"]):
        exercises = [e for e in exercises if not e["uses_arm"]]

    rows = []
    non_cardio = [e for e in exercises if e["type"] != "cardio"]
    cardio = [e for e in exercises if e["type"] == "cardio"]

    # reserve time for strength/core
    strength_time = len(non_cardio) * 1
    cardio_time = max(5, session_duration - strength_time)

    for ex in non_cardio:
        if intensity == "Low":
            sets, reps = 1, "10-12"
        elif intensity == "Moderate":
            sets, reps = 2, "12-15"
        else:
            sets, reps = 3, "15-20"

        rows.append({"Exercise": ex["name"], "Sets": sets, "Reps / Time": f"{reps} reps"})

    for ex in cardio:
        rows.append({"Exercise": ex["name"], "Sets": "-", "Reps / Time": f"{cardio_time} min steady pace"})

    return pd.DataFrame(rows)

# ---------------- PROMPT ----------------
def build_prompt():

    feature_text = ", ".join(selected_features)

    return f"""
You are a youth sports coach AI. Be SHORT, structured, practical.

Athlete:
Sport: {sport}
Position: {position}
Age: {age}
Goal: {goal}
Injury: {injury}
Intensity: {intensity}
Diet: {diet}
Training Days: {training_days}
Session Duration: {session_duration}

Focus ONLY on these features: {feature_text}

Rules:
- Max 200 words
- Bullet points
- No lecture
- Practical actions only

Sections:
1. Recovery (only if injury)
2. Workout Focus
3. Weekly Advice
4. Diet / Hydration
"""

# ---------------- SAFE GEMINI ----------------
def get_ai_text(prompt):

    try:
        response = model.generate_content(prompt)

        if not response or not response.candidates:
            return "⚠️ AI returned no candidates."

        candidate = response.candidates[0]

        if candidate.finish_reason != 1 and not candidate.content:
            return "⚠️ AI blocked or empty response."

        text = ""
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if hasattr(part, "text") and part.text:
                    text += part.text

        return text.strip() if text else "⚠️ Empty AI output."

    except Exception as e:
        return f"Error: {e}"

# ---------------- GENERATE ----------------
if st.button("Generate Coaching Advice"):

    if not selected_features:
        st.warning("Select at least one feature.")
    else:
        with st.spinner("Generating..."):
            output = get_ai_text(build_prompt())

        st.subheader("📋 AI Coaching Output")
        st.write(output)

        if any(f in selected_features for f in ["Full Workout Plan","Stamina Builder"]):
            st.subheader("🏋️ Workout Plan")
            st.dataframe(generate_workout_table())

        if "Weekly Training Plan" in selected_features:
            st.subheader("📅 Weekly Training Schedule")

            days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            workout_types = [
                "Stamina + Core",
                "Strength",
                "Cardio",
                "Mobility",
                "Speed",
                "Technique",
                "Recovery"
            ]

            schedule = [workout_types[i] if i < training_days else "Rest" for i in range(7)]
            st.table(pd.DataFrame({"Day": days, "Focus": schedule}))

        if "Nutrition Plan" in selected_features:
            st.subheader("🥗 Nutrition Guide")
            st.dataframe(pd.DataFrame({
                "Meal":["Breakfast","Lunch","Dinner","Snacks"],
                "Focus":["Carbs + Protein","Balanced","Protein Rich","Fruits + Nuts"]
            }))
