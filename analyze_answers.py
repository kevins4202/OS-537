import pandas as pd
import os

def analyze_answers(exam):
    df = pd.read_csv("gemini_answers.csv")
    model_answers = df[exam]
    
    answer_df = pd.read_csv(f"answers/{exam}.csv")

    # dataframe of total points for each model

    total_points = pd.DataFrame(columns=["model"])
    
    points = sum([1 for i in range(len(model_answers)) if model_answers[i] == answer_df["answer"][i]])

    total_points.loc[exam][model] = points