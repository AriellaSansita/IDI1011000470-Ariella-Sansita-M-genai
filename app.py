import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np

# ---------------- CONFIG ----------------
st.set_page_config(page_title="CoachBot AI", page_icon="🏋️", layout="centered")

# Get API key from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("GOOGLE_API_KEY not found. Add it in Streamlit → App Settings → Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- UI ----------------
st.title("🏋️ CoachBot AI")
st.caption("AI-powered personalized fitness & sports coaching")

st.divider()

sport = st.text_input("Sport", placeholder="e.g., Football, Cricket, Basketball")
position = st.text_input("Player Position", placeholder="e.g., Striker, Bowler, Guard")
goal = st.text_input("Primary Goal", placeholder="e.g., Build stamina, Strength, Recovery")
injury = st.text_input("Injury / Risk Area", placeholder="e.g., Knee strain, None")
diet = st.selectbox("Diet Preference", ["No Preference", "Vegetarian", "Non-Vegetarian", "Vegan"])

st.divider()

feature = st.selectbox(
    "What would you like to generate?",
    [
        "Full Workout Plan",
        "Recovery & Injury-Safe Training",
        "Weekly Nutrition Plan",
        "Warm-up & Cooldown Routine",
        "Tactical Improvement Tips"
    ]
)

# ---------------- PROMPT LOGIC ----------------
def build_prompt(feature):
    base = f"""
You are a certified professional sports coach and fitness trainer.

Athlete Profile:
Sport: {sport}
Position: {position}
Goal: {goal}
Injury/Risk Area: {injury}
Diet Preference: {diet}

Follow safe training practices. Avoid medical diagnosis.
Write COMPLETE structured output in clear sections. Do NOT stop early.
"""

    prompts = {
        "Full Workout Plan": base + "Generate a full detailed weekly workout plan (Day-wise).",
        "Recovery & Injury-Safe Training": base + "Generate a recovery-focused and injury-safe weekly training routine.",
        "Weekly Nutrition Plan": base + "Generate a simple weekly nutrition plan aligned with the athlete’s goal.",
        "Warm-up & Cooldown Routine": base + "Generate a structured warm-up and cooldown routine.",
        "Tactical Improvement Tips": base + "Provide clear tactical and performance improvement tips for the position."
    }

    return prompts[feature]

# ---------------- GENERATION ----------------
if st.button("Generate Plan"):
    if not sport or not goal:
        st.warning("Please enter at least the Sport and Goal.")
    else:
        with st.spinner("CoachBot AI is generating..."):
            try:
                response = model.generate_content(
                    build_prompt(feature),
                    generation_config={
                        "temperature": 0.4,
                        "max_output_tokens": 1500
                    }
                )

                st.subheader("📋 AI Generated Output")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error generating plan: {str(e)}")

# ---------------- GRAPH ----------------
st.divider()
st.subheader("📈 Weekly Training Load")

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
load = np.random.randint(50, 100, size=7)

fig, ax = plt.subplots()
ax.plot(days, load, marker="o")
ax.set_xlabel("Day")
ax.set_ylabel("Training Intensity")
ax.set_title("Weekly Training Load")

st.pyplot(fig)

st.divider()
st.caption("⚠️ AI-generated advice is for educational purposes only.")
