import streamlit as st
import PyPDF2
from chatbot import chatbot_response, analyze_resume

# -------------------------------
# Title
# -------------------------------
st.title("📄 AI Resume Analyzer")

# -------------------------------
# Sidebar HR Database
# -------------------------------
import os
import pandas as pd
with st.sidebar:
    st.header("📁 HR Candidate Database")
    st.write("Automatically records all analyzed CVs into a local 'Google Sheets' style report.")
    
    DB_FILE = "candidates_report.csv"
    if os.path.exists(DB_FILE):
        db_df = pd.read_csv(DB_FILE)
        st.dataframe(db_df, hide_index=True)
        with open(DB_FILE, "rb") as f:
            st.download_button("📥 Download Report for Google Sheets", data=f, file_name="candidates_report.csv", mime="text/csv")
    else:
        st.info("No candidates processed yet.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# -------------------------------
# Extract Text from PDF
# -------------------------------
def extract_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

# Using AI to extract skills and predict role

# -------------------------------
# Main Logic
# -------------------------------
if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text(uploaded_file)
    with st.spinner("Analyzing resume with AI to extract skills and find the best fit positions..."):
        analysis = analyze_resume(text)

    skills = analysis.get("skills", [])
    roles = analysis.get("roles", [])
    summary = analysis.get("summary", "")
    
    top_role = roles[0]["title"] if roles else "General Role"

    # -------------------------------
    # Save to Report Database
    # -------------------------------
    import pandas as pd
    import os
    
    candidate_name = analysis.get("candidate_name", "Unknown Candidate")
    top_role_match = roles[0].get("match_percentage", 0) if roles else 0
    all_skills = ", ".join([s.get("name", str(s)) if isinstance(s, dict) else str(s) for s in skills])
    
    new_record = pd.DataFrame([{
        "Candidate Name": candidate_name,
        "Top Predicted Position": top_role,
        "Match %": top_role_match,
        "Overall Score": min(len(skills) * 10, 100),
        "Extracted Skills": all_skills
    }])
    
    if "last_processed" not in st.session_state or st.session_state.last_processed != uploaded_file.name:
        if os.path.exists(DB_FILE):
            existing_df = pd.read_csv(DB_FILE)
            updated_df = pd.concat([existing_df, new_record], ignore_index=True)
        else:
            updated_df = new_record
            
        updated_df.to_csv(DB_FILE, index=False)
        st.session_state.last_processed = uploaded_file.name

    # -------------------------------
    # Show Summary
    # -------------------------------
    st.subheader("📝 Professional Summary")
    st.info(summary)

    # -------------------------------
    # Show Skills
    # -------------------------------
    st.subheader("📌 Extracted Skills & Proficiency")
    if skills:
        import pandas as pd
        skills_df = pd.DataFrame(skills)
        if not skills_df.empty and "name" in skills_df.columns:
            skills_df.rename(columns={"name": "Skill", "category": "Category", "level": "Proficiency Level"}, inplace=True)
            st.dataframe(skills_df, use_container_width=True, hide_index=True)
            
            # -------------------------------
            # Skill Visualizations
            # -------------------------------
            import plotly.express as px
            
            st.markdown("<br>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                # Skill Distribution by Category (Donut Chart)
                if "Category" in skills_df.columns:
                    cat_counts = skills_df['Category'].value_counts().reset_index()
                    cat_counts.columns = ['Category', 'Count']
                    fig_cat = px.pie(cat_counts, values='Count', names='Category', hole=0.4, title="Skill Distribution by Category")
                    fig_cat.update_layout(margin=dict(t=40, b=0, l=0, r=0))
                    st.plotly_chart(fig_cat, use_container_width=True)
                    
            with col2:
                # Proficiency Level Distribution (Bar Chart)
                if "Proficiency Level" in skills_df.columns:
                    level_order = ["Beginner", "Intermediate", "Advanced", "Expert"]
                    prof_counts = skills_df['Proficiency Level'].value_counts().reset_index()
                    prof_counts.columns = ['Proficiency Level', 'Count']
                    fig_prof = px.bar(
                        prof_counts, x='Proficiency Level', y='Count', 
                        title="Proficiency Levels", 
                        color='Proficiency Level', 
                        category_orders={"Proficiency Level": level_order}
                    )
                    fig_prof.update_layout(margin=dict(t=40, b=0, l=0, r=0), showlegend=False)
                    st.plotly_chart(fig_prof, use_container_width=True)
                    
        else:
            st.write(", ".join([s.get('name', str(s)) if isinstance(s, dict) else str(s) for s in skills]))
    else:
        st.write("No skills found")

    # -------------------------------
    # Show Roles
    # -------------------------------
    st.subheader("🎯 Top Predicted Job Roles & Position Analysis")
    for r in roles:
        title = r.get("title", "Role")
        match = r.get("match_percentage", 0)
        reasoning = r.get("reasoning", "")
        with st.expander(f"{title} ({match}% Match)", expanded=True):
            st.progress(match / 100.0)
            st.write(reasoning)
            
            matching = r.get("matching_skills", [])
            gap = r.get("skill_gap_analysis", {})
            critical = gap.get("critical_missing_skills", [])
            bonus = gap.get("bonus_missing_skills", [])
            learning_path = gap.get("recommended_learning_path", [])

            if st.button(f"🔊 Listen to Detailed Analysis for {title}", key=f"tts_{title}"):
                with st.spinner("Generating High-Quality AI Voice..."):
                    try:
                        import os
                        from elevenlabs import ElevenLabs
                        client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
                        
                        match_text = f"My profile has a {match} percent alignment with this position. "
                        skills_text = f"My strongest matching skills include {', '.join(matching)}. " if matching else "I possess a strong foundational understanding of this field. "
                        gap_text = f"To fully secure this role, I need to focus on acquiring critical skills like {', '.join(critical)}. " if critical else "I am fully equipped and highly prepared for this position. "
                        learning_text = f"My recommended immediate learning path is to {learning_path[0]}." if learning_path else ""
                        
                        pitch = f"Hello! Let me explain my alignment with the {title} position. {match_text} {reasoning} {skills_text} {gap_text} {learning_text}"
                        
                        audio_generator = client.generate(
                            text=pitch,
                            voice="Brian",
                            model="eleven_multilingual_v2"
                        )
                        audio_bytes = b"".join(audio_generator)
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as e:
                        st.error(f"ElevenLabs Error: {e}")
            
            if matching or critical or bonus:
                st.markdown("---")
                col1, col2 = st.columns(2)
                with col1:
                    if matching:
                        st.markdown("##### ✅ Matching Skills")
                        for s in matching: st.markdown(f"- {s}")
                with col2:
                    if critical:
                        st.markdown("##### ❌ Critical Missing Skills")
                        for s in critical: st.markdown(f"- {s}")
                    if bonus:
                        st.markdown("##### ⚠️ Bonus Missing Skills")
                        for s in bonus: st.markdown(f"- {s}")
                        
            if learning_path:
                st.info("**📚 Recommended Learning Path to secure this Role:**\n\n" + "\n".join([f"- {p}" for p in learning_path]))

    # -------------------------------
    # Data Analyst Screening Profile
    # -------------------------------
    da_scores = analysis.get("data_analyst_screening", {})
    if da_scores:
        st.subheader("📈 Data Analyst Screening Profile")
        import pandas as pd
        import plotly.express as px
        
        # Convert dictionary to DataFrame for Plotly
        df = pd.DataFrame(dict(
            Score=list(da_scores.values()),
            Skill=list(da_scores.keys())
        ))
        
        # Create an interactive Radar Chart
        fig = px.line_polar(df, r='Score', theta='Skill', line_close=True, range_r=[0,100], markers=True)
        fig.update_traces(fill='toself', line_color='rgba(0, 150, 255, 0.8)')
        st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Score
    # -------------------------------
    score = min(len(skills) * 10, 100)

    st.subheader("📊 Overall Skill Score")
    st.progress(score / 100.0)
    st.write(f"Score: {score}/100")

    # -------------------------------
    # Industrial Market Analysis
    # -------------------------------
    market = analysis.get("market_analysis", {})
    if market:
        st.subheader("🌍 Industrial Market Analysis")
        st.info(market.get("market_alignment", ""))
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("🔥 High-Demand Skills Possessed")
            for s in market.get("hot_skills_possessed", []):
                st.markdown(f"- **{s}**")
        with col2:
            st.warning("📈 Recommended Skills to Acquire")
            for s in market.get("skills_to_acquire", []):
                st.markdown(f"- **{s}**")

    # -------------------------------
    # Resume Text View
    # -------------------------------
    with st.expander("📄 View Full Resume Text"):
        st.write(text)

    # -------------------------------
    # Chatbot UI (WhatsApp Style)
    # -------------------------------
    st.subheader("🤖 AI Career Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_query = st.chat_input("Type your message...")

    if user_query:
        response = chatbot_response(user_query, skills, top_role)

        st.session_state.messages.append({"role": "user", "content": user_query})
        
        # Generate Audio for Chatbot Response
        audio_bytes = None
        try:
            import os
            from elevenlabs import ElevenLabs
            client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
            audio_generator = client.generate(
                text=response,
                voice="Brian",
                model="eleven_multilingual_v2"
            )
            audio_bytes = b"".join(audio_generator)
        except Exception as e:
            st.error(f"ElevenLabs TTS Error: {e}")
            
        st.session_state.messages.append({"role": "assistant", "content": response, "audio": audio_bytes})

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])
                if msg.get("audio"):
                    st.audio(msg["audio"], format="audio/mp3", autoplay=True)
            