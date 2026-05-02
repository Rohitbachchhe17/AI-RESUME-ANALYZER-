import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier

def train_model():
    data = pd.read_csv("data.csv")
    
    X = data["skills"]
    y = data["job_role"]
    
    vectorizer = CountVectorizer()
    X_vec = vectorizer.fit_transform(X)
    
    model = DecisionTreeClassifier()
    model.fit(X_vec, y)
    
    return model, vectorizer


def predict_role(model, vectorizer, skills_text):
    X = vectorizer.transform([skills_text])
    return model.predict(X)[0]
