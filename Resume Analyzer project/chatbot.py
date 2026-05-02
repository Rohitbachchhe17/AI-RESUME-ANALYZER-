def analyze_resume(text):
    try:
        import os
        import json
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.getenv("OPENAI_API_KEY")
        )

        prompt = f"""Analyze the following resume text comprehensively. 
Return a JSON object with the following structure:
{{
  "candidate_name": "Full Name of Candidate (or 'Unknown' if not explicitly stated)",
  "summary": "A 2-3 sentence professional evaluation of the candidate's profile.",
  "skills": [
    {{"name": "Python", "category": "Programming", "level": "Expert"}},
    {{"name": "SQL", "category": "Databases", "level": "Advanced"}},
    {{"name": "Communication", "category": "Soft Skills", "level": "Intermediate"}}
  ],
  "roles": [
    {{
      "title": "Role Title (e.g., Senior Data Scientist)", 
      "match_percentage": 95, 
      "reasoning": "High-quality, deep analysis of why this candidate fits this role...",
      "matching_skills": ["Skill 1", "Skill 2"],
      "skill_gap_analysis": {{
        "critical_missing_skills": ["Crucial Skill 1", "Crucial Skill 2"],
        "bonus_missing_skills": ["Nice-to-have Skill"],
        "recommended_learning_path": ["Specific advanced course or project 1", "Specific topic 2"]
      }}
    }}
  ],
  "data_analyst_screening": {{
    "SQL & Databases": 85,
    "Programming (Python/R)": 75,
    "Data Visualization": 90,
    "Statistics & Math": 60,
    "Business Intelligence": 80
  }},
  "market_analysis": {{
    "market_alignment": "A paragraph explaining how the candidate's profile aligns with current industrial market trends and demands.",
    "hot_skills_possessed": ["Skill 1", "Skill 2"],
    "skills_to_acquire": ["Recommended Skill 1", "Recommended Skill 2"]
  }}
}}

Note: For 'roles', you MUST generate EXACTLY 5 diverse roles: 1. Primary Best Fit, 2. Secondary Fit, 3. Tertiary Fit, 4. Lateral/Pivot Role, 5. Aspirational/Stretch Role. For 'data_analyst_screening', score from 0 to 100 based on the resume. For 'skills', exhaustively extract ALL technical and soft skills (aim for 15-20+), categorize each skill, and determine proficiency. For 'market_analysis', accurately analyze the current industrial market to provide real-world insights and highly accurate recommendations for this specific profile.

Resume Text:
{text[:4000]}"""
        
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini" if "openrouter" in os.getenv("OPENAI_BASE_URL", "") else "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print(f"Analyze error: {e}")
        return {
            "summary": "Failed to analyze resume.",
            "skills": ["python", "sql", "data analysis"],
            "roles": [{"title": "Data Analyst", "match_percentage": 50, "reasoning": "Fallback data due to error."}]
        }

def chatbot_response(query, skills, role):
    try:
        import os
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        client = OpenAI(
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            api_key=os.getenv("OPENAI_API_KEY")
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini" if "openrouter" in os.getenv("OPENAI_BASE_URL", "") else "gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a career counselor. The user's skills are {', '.join([s.get('name', str(s)) if isinstance(s, dict) else str(s) for s in skills])} and their predicted role is {role}. Give helpful career advice."},
                {"role": "user", "content": query}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Chatbot error: {e}")
        # fallback (your old chatbot)
        if "skill" in query.lower():
            return "Learn Python, ML, SQL"
        elif "job" in query.lower():
            return f"You can apply for {role}"
        else:
            return "Try asking about skills or career 😊"