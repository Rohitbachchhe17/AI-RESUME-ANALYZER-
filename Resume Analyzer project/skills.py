skills_list = [
    "python", "java", "c++", "machine learning",
    "data science", "sql", "deep learning",
    "html", "css", "javascript"
]

def extract_skills(text):
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill)
    return found