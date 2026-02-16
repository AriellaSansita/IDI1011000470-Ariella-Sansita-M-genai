import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
# Requirement: Integrate Gemini 1.5 Pro with specific configuration
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel(
    "gemini-2.5-flash", 
    generation_config={
        "temperature": 0.4, # Conservative for youth safety
        "top_p": 0.9
    }
)

st.set_page_config(page_title="CoachBot AI", layout="wide", page_icon="🏆")

# ---------------- DATA MAPPING ----------------
# Expanded sports list to bridge coaching gaps
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

# ---------------- TOP NAVIGATION & INPUTS ----------------
st.title("🏆 CoachBot AI: Smart Fitness Assistant")
st.info("Empowering the next generation of athletes with AI-driven training.")

# Page Selection via Tabs (instead of sidebar)
tab1, tab2 = st.tabs(["📊 Smart Coaching Assistant", "🧠 Custom AI Coach"])

with tab1:
    # Organize features into columns at the TOP
    with st.container():
        st.subheader("1. Athlete Profile")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            sport = st.selectbox("Sport", list(positions_map.keys()))
        with col2:
            position = st.selectbox("Position", positions_map[sport])
        with col3:
            age = st.number_input("Age", 10, 25, 16)
        with col4:
            injury = st.text_input("Injury History", "None")

    with st.container():
        st.subheader("2. Training Goals")
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            goal = st.selectbox("Primary Goal", ["Stamina", "Strength", "Speed", "Recovery", "Tactical IQ"])
        with col6:
            intensity = st.select_slider("Intensity", options=["Low", "Moderate", "High"])
        with col7:
            schedule_days = st.number_input("Schedule Days", 1, 30, 7)
        with col8:
            feature = st.selectbox("Coaching Focus", [
                "Weekly Training Plan", "Nutrition & Macros", "Injury Prevention", "Mental Focus Training"
            ])

    st.markdown("---")

    if st.button("Generate My AI Coaching Plan"):
        # Prompt Engineering: Combines user profile + goal + context
        prompt = (f"Act as a professional youth coach. Provide a {feature} for a {age}yo {sport} {position}. "
                  f"Goal: {goal}. Duration: {schedule_days} days. Injury: {injury}. Intensity: {intensity}. "
                  f"Format: Provide the response ONLY in a Markdown TABLE for high readability.")
        
        with st.spinner("Analyzing sports science data..."):
            try:
                response = model.generate_content(prompt)
                
                # UI Layout for results and graphs
                res_col, vis_col = st.columns([2, 1])
                
                with res_col:
                    st.success(f"Generated {feature}")
                    st.markdown(response.text)
                
                with vis_col:
                    st.subheader("📊 Session Breakdown")
                    # Visualizing training segments using matplotlib
                    fig, ax = plt.subplots(figsize=(5, 5))
                    colors = ['#ff9999','#66b3ff','#99ff99']
                    ax.pie([15, 70, 15], labels=['Warmup', 'Core', 'Cool-down'], autopct='%1.1f%%', colors=colors)
                    st.pyplot(fig)
                    st.caption("Estimated time allocation per training session.")
            except Exception as e:
                st.error(f"Error generating plan: {e}")

with tab2:
    st.subheader("Direct Coach Consultation")
    st.write("Type specific questions for personalized tactical advice or nutrition tips.")
    
    # Requirement: Prompt Engineering and Hyperparameter tuning
    user_custom_prompt = st.text_area("Ask the Coach anything:", placeholder="e.g., How should I hydrate for a 3-hour cricket match?")
    
    custom_col1, custom_col2 = st.columns([1, 2])
    with custom_col1:
        custom_temp = st.slider("Coaching Style (Temperature)", 0.0, 1.0, 0.4, help="Lower = Conservative/Safe, Higher = Creative")

    if st.button("Get Custom Advice"):
        if user_custom_prompt:
            try:
                # Configuring model based on user tuning
                custom_model = genai.GenerativeModel("gemini-1.5-pro", generation_config={"temperature": custom_temp})
                custom_res = custom_model.generate_content(user_custom_prompt)
                st.info("Coach Bot says:")
                st.markdown(custom_res.text)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a query.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("NextGen Sports Lab | Developed by [Your Name] | IDAI103 Assignment")
