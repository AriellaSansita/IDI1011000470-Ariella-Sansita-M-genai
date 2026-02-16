import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION ----------------
# Use the specific Gemini 2.5 Flash model string as requested
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_ai_response(target_model, prompt):
    """Safely extracts text and programmatically removes HTML tags like <br>."""
    try:
        response = target_model.generate_content(prompt)
        # Verify the response contains valid parts to avoid 'Part' accessor errors
        if response.candidates and response.candidates[0].content.parts:
            raw_text = response.candidates[0].content.parts[0].text
            # Manual cleanup to ensure strict Markdown formatting
            clean_text = raw_text.replace("<br>", " ").replace("</br>", " ").replace("<div>", "").replace("</div>", "")
            return clean_text
        return "The AI Coach is currently unavailable. Please check your connection."
    except Exception as e:
        return f"Model Error: {str(e)}"

# Set app branding and layout
st.set_page_config(page_title="CoachBot AI", layout="wide", page_icon="🏆")

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

# ---------------- UI DESIGN ----------------
st.title("🏆 CoachBot AI")
st.write("Professional-grade coaching and fitness assistant for youth athletes.")

tab1, tab2 = st.tabs(["📊 Smart Assistant", "🧠 Custom Coach"])

with tab1:
    st.subheader("1. Athlete Profile")
    c1, c2, c3, c4 = st.columns(4)
    with c1: sport = st.selectbox("Sport", list(positions_map.keys()))
    with c2: position = st.selectbox("Position", positions_map[sport])
    with c3: age = st.number_input("Age", 10, 50, 18)
    with c4: injury = st.text_input("Injury History", "None")

    st.subheader("2. Training Details")
    g1, g2, g3, g4 = st.columns(4)
    with g1: 
        # Requirement: 10 creative, diverse prompts/features
        feature = st.selectbox("Coaching Focus", [
            "Full Workout Plan", "Weekly Training Plan", "Nutrition Plan", 
            "Hydration Strategy", "Warm-up & Cooldown", "Tactical Coaching", 
            "Skill Drills", "Injury Risk Predictor", "Mobility & Stretching", 
            "Mental Focus Training"
        ])
    with g2: goal = st.selectbox("Goal", ["Stamina", "Strength", "Speed", "Recovery", "Skill Improvement"])
    with g3: intensity_level = st.select_slider("Intensity Level", options=["Low", "Moderate", "High"])
    with g4: days = st.number_input("Duration (Days)", 1, 30, 7)

    # Dynamic Nutrition inputs (Conditional Logic)
    allergy, pref = "None", "N/A"
    if feature in ["Nutrition Plan", "Hydration Strategy"]:
        st.info("🍎 Nutrition Details Required")
        f1, f2 = st.columns(2)
        with f1: pref = st.selectbox("Meal Preference", ["Non-Veg", "Vegetarian", "Vegan"])
        with f2: allergy = st.text_input("Food Allergies", "None")

    if st.button("Generate Plan", type="primary"):
        # Initializing Gemini 2.5 Flash
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = (
            f"Act as a professional coach for a {age}yo {sport} {position}. Goal: {goal}. "
            f"Intensity: {intensity_level}. Injury History: {injury}. "
            f"Diet: {pref}. Allergies: {allergy}. Task: Provide a {feature} for {days} days. "
            "STRICT RULES: Output ONLY a Markdown table. NO HTML tags like <br>. "
            "Ensure the content is technically accurate for the specific athlete position."
        )
        
        with st.spinner("AI Coach calculating performance data..."):
            result = get_ai_response(model, prompt)
            res_col, vis_col = st.columns([2, 1])
            with res_col:
                st.success(f"📋 AI Coaching Output: {feature}")
                st.markdown(result)
            with vis_col:
                # Step 6: Data Visualization Requirement
                st.subheader("📊 Session Load Split")
                fig, ax = plt.subplots(figsize=(5,4))
                ax.pie([20, 60, 20], labels=['Warm-up', 'Core Work', 'Recovery'], 
                       autopct='%1.1f%%', colors=['#FFD700','#1E90FF','#32CD32'])
                st.pyplot(fig)

with tab2:
    st.subheader("🧠 Custom Coach Consultation")
    user_query = st.text_area("Ask a specific coaching question:", 
                             placeholder="e.g., Suggest 3 drills for explosive speed.")
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        # Intensity 1-100 slider mapping to model temperature (Hyperparameter Tuning)
        intensity_val = st.slider("Advice Intensity", 1, 100, 40)
        ai_temp = intensity_val / 100.0

    if st.button("Ask AI Coach", type="primary"):
        if user_query:
            # Re-initializing model with custom temperature (Intensity)
            custom_model = genai.GenerativeModel("gemini-2.5-flash", 
                                               generation_config={"temperature": ai_temp})
            
            custom_prompt = (
                f"User Question: {user_query}. Advice Intensity: {intensity_val}/100. "
                "STRICT RULES: Output ONLY a short, technical Markdown table. NO HTML tags like <br>. "
                "Keep descriptions extremely concise."
            )
            
            with st.spinner("Consulting AI Coach..."):
                answer = get_ai_response(custom_model, custom_prompt)
                st.info("📋 Quick Coaching Chart:")
                st.markdown(answer)

st.markdown("---")
