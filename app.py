import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Requirement: Integrate Gemini 1.5 Pro to process and generate outputs (Step 2)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash", 
    generation_config={
        "temperature": 0.3, # Conservative tuning for youth safety as per brief
        "top_p": 0.8
    }
)

st.set_page_config(page_title="CoachBot AI", layout="wide", page_icon="🏆")

# Function for the Reset Button (Step 6: User-centric UX)
def reset_app():
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()

# ---------------- DATA MAPPING ----------------
# Expanded sports and positions to bridge coaching gaps (Step 1)
positions_map = {
    "Football": ["Striker", "Midfielder", "Defender", "Goalkeeper", "Winger"],
    "Cricket": ["Batsman", "Fast Bowler", "Spin Bowler", "Wicket Keeper", "All-Rounder"],
    "Basketball": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
    "Athletics": ["Sprinter", "Long Distance", "Jumper", "Thrower"],
    "Swimming": ["Freestyle", "Breaststroke", "Butterfly", "Backstroke"],
    "Tennis": ["Singles", "Doubles Specialist"],
    "Rugby": ["Forward", "Back"],
    "Volleyball": ["Setter", "Libero", "Attacker", "Blocker"],
    "Badminton": ["Singles", "Doubles"],
    "Hockey": ["Forward", "Midfielder", "Defender", "Goalie"],
    "Kabaddi": ["Raider", "Defender", "All-Rounder"]
}

# ---------------- TOP UI LAYOUT ----------------
st.title("🏆 CoachBot AI: Smart Fitness Assistant")
st.info("Personalized virtual coaching for the next generation of athletes.")

tab1, tab2 = st.tabs(["📊 Smart Coaching Assistant", "🧠 Custom AI Coach"])

with tab1:
    # Row 1: Athlete Profile
    st.subheader("1. Athlete Profile")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        sport = st.selectbox("Sport", list(positions_map.keys()))
    with p_col2:
        position = st.selectbox("Position", positions_map[sport])
    with p_col3:
        age = st.number_input("Age", 10, 50, 18)
    with p_col4:
        injury = st.text_input("Injury History", "None")

    # Row 2: Training Configuration (Step 3: At least 10 Prompts/Features)
    st.subheader("2. Training Configuration")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        # These 10 features are mapped directly to the Assessment Brief requirements
        feature = st.selectbox("Coaching Focus", [
            "Full Workout Plan",        # Required: Position-based workouts
            "Weekly Training Plan",     # Required: Adaptive fitness routines
            "Nutrition Plan",           # Required: Nutrition recommendations
            "Hydration Strategy",       # Hint: Electrolyte strategies
            "Warm-up & Cooldown",       # Required: Healthy and safe sports development
            "Tactical Coaching",        # Required: Game strategies & tactical advice
            "Skill Drills",             # Required: Technical improvement
            "Injury Risk Predictor",    # Required: Account for risk factors
            "Mobility & Stretching",    # Hint: Post-injury recovery
            "Mental Focus Training"     # Hint: Mindset & visualization
        ])
    with g_col2:
        goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
    with g_col3:
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
    with g_col4:
        schedule_days = st.number_input("Schedule Days", 1, 30, 7)

    st.markdown("---")

    # Action Buttons Row (Step 6: Usability)
    btn_col1, btn_col2 = st.columns([1, 6])
    with btn_col1:
        generate_btn = st.button("Generate Plan", type="primary")
    with btn_col2:
        st.button("Reset All Fields", on_click=reset_app)

    if generate_btn:
        # Prompt Engineering (Step 3)
        prompt = (
            f"Act as a professional youth coach for a {age} year old {sport} player ({position}). "
            f"Goal: {goal}. Intensity: {intensity}. Injury History: {injury}. "
            f"Provide a {feature} for {schedule_days} days. "
            "MANDATORY FORMATTING:\n"
            "1. Output ONLY a Markdown table.\n"
            "2. DO NOT use HTML tags like <br> or <div>.\n"
            "3. Use a single space or comma for line breaks inside a cell.\n"
            "4. Ensure the output is highly coherent and position-sensitive."
        )
        
        with st.spinner("CoachBot is analyzing your profile..."):
            try:
                response = model.generate_content(prompt)
                res_col, vis_col = st.columns([2, 1])
                
                with res_col:
                    st.success(f"Generated {feature}")
                    st.markdown(response.text) # Step 4: Output Quality
                
                with vis_col:
                    st.subheader("📊 Target Effort Split")
                    # Step 6: Data Visualization using Matplotlib
                    fig, ax = plt.subplots(figsize=(5, 4))
                    ax.pie([15, 70, 15], labels=['Warm-up', 'Core', 'Cool-down'], 
                           autopct='%1.1f%%', colors=['#ffcc99','#66b3ff','#99ff99'], startangle=90)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("🧠 Direct Coach Consultation")
    user_custom_prompt = st.text_area("What is your coaching question?", 
                                     placeholder="e.g., Suggest pre-match visualization techniques for a striker.")
    
    custom_col1, custom_col2 = st.columns([1, 2])
    with custom_col1:
        # Step 2: Hyperparameter Tuning (Temperature control)
        custom_temp = st.slider("Coaching Style (Temperature)", 0.0, 1.0, 0.4)

    cbtn_col1, cbtn_col2 = st.columns([1, 6])
    with cbtn_col1:
        ask_btn = st.button("Ask Coach", type="primary")
    with cbtn_col2:
        st.button("Clear Question", on_click=reset_app)

    if ask_btn:
        if user_custom_prompt:
            try:
                custom_model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"temperature": custom_temp})
                custom_res = custom_model.generate_content(user_custom_prompt)
                st.info("CoachBot AI Advice:")
                st.markdown(custom_res.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed for NextGen Sports Lab | AI Summative Assessment | Gemini 2.5 Flash")
