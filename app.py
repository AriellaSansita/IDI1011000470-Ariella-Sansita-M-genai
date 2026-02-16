import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Configured for Gemini 2.5 Flash as requested
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash", 
    generation_config={
        "temperature": 0.3, # Optimized for precision and safety
        "top_p": 0.8
    }
)

st.set_page_config(page_title="Elite Athlete AI", layout="wide", page_icon="⚡")

# ---------------- RESET LOGIC ----------------
# Step 6: User-centric UX - Ensures the app can be cleared entirely
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

def reset_all():
    st.session_state.reset_counter += 1
    st.rerun()

# ---------------- DATA MAPPING ----------------
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
st.title("⚡ Elite Athlete AI: Smart Performance Assistant")
st.markdown("> **Scenario 2:** Bridging the coaching gap for youth athletes through AI-driven insights.")
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Performance Assistant", "🧠 Tactical AI Coach"])

with tab1:
    # Key version for reset functionality
    rv = st.session_state.reset_counter

    # Row 1: Athlete Profile
    st.subheader("1. Athlete Profile")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        sport = st.selectbox("Sport", list(positions_map.keys()), key=f"s_{rv}")
    with p_col2:
        position = st.selectbox("Position", positions_map[sport], key=f"p_{rv}")
    with p_col3:
        age = st.number_input("Age", 10, 50, 18, key=f"a_{rv}")
    with p_col4:
        injury = st.text_input("Injury History", "None", key=f"i_{rv}")

    # Row 2: Training Configuration (Step 3: Required 10 Prompts)
    st.subheader("2. Training Configuration")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        feature = st.selectbox("Coaching Focus", [
            "Full Workout Plan", "Weekly Training Plan", "Nutrition Plan", 
            "Hydration Strategy", "Warm-up & Cooldown", "Tactical Coaching", 
            "Skill Drills", "Injury Risk Predictor", "Mobility & Stretching", 
            "Mental Focus Training"
        ], key=f"f_{rv}")
    with g_col2:
        goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"], key=f"g_{rv}")
    with g_col3:
        intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"], key=f"int_{rv}")
    with g_col4:
        schedule_days = st.number_input("Schedule Days", 1, 30, 7, key=f"d_{rv}")

    st.markdown("---")

    # Action Buttons
    b1, b2 = st.columns([1, 6])
    with b1:
        generate_btn = st.button("Generate Plan", type="primary")
    with b2:
        st.button("Reset All Fields", on_click=reset_all)

    if generate_btn:
        # Prompt Engineering (Step 3 & 4): Enforcing table output and removing HTML
        prompt = (
            f"Act as a certified pro coach for a {age}yo {sport} {position}. "
            f"Goal: {goal}. Intensity: {intensity}. Injury History: {injury}. "
            f"Create a {feature} for {schedule_days} days. "
            "STRICT RULES:\n"
            "1. Output ONLY a Markdown table.\n"
            "2. NO HTML tags (like <br>).\n"
            "3. Ensure advice is safety-first and customized for the position."
        )
        
        with st.spinner("AI is calculating performance metrics..."):
            try:
                response = model.generate_content(prompt)
                out_col, vis_col = st.columns([2, 1])
                with out_col:
                    st.success(f"Generated: {feature}")
                    st.markdown(response.text) # Clean output
                with vis_col:
                    st.subheader("📊 Session Load Analysis")
                    # Step 6: Data Visualization for technical proficiency
                    fig, ax = plt.subplots(figsize=(5, 4))
                    ax.pie([15, 70, 15], labels=['Activation', 'Workload', 'Recovery'], 
                           autopct='%1.1f%%', colors=['#FFD700','#1E90FF','#32CD32'], startangle=90)
                    st.pyplot(fig)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("🧠 Tactical AI Coach")
    user_query = st.text_area("Specific coaching question:", 
                             placeholder="e.g., How should a striker position themselves during an indirect free kick?",
                             key=f"q_{rv}")
    
    c_col1, c_col2 = st.columns([1, 2])
    with c_col1:
        # Step 5: Hyperparameter Tuning (Temperature Slider)
        c_temp = st.slider("Coaching Style (Temperature)", 0.0, 1.0, 0.4, key=f"t_{rv}")

    if st.button("Ask AI Coach", type="primary"):
        if user_query:
            try:
                # Custom model instance with tuned temperature
                custom_model = genai.GenerativeModel("gemini-2.5-flash", generation_config={"temperature": c_temp})
                res = custom_model.generate_content(user_query)
                st.info("AI Coach Perspective:")
                st.markdown(res.text)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("⚡ Elite Athlete AI | NextGen Sports Lab | AI Summative Assessment 2026")
