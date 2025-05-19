import pandas as pd

def detect_bias(df):
    # Simulated example: outcome variance by gender
    if "gender" in df.columns and "outcome" in df.columns:
        group_outcomes = df.groupby("gender")["outcome"].value_counts(normalize=True).unstack()
        return group_outcomes.to_dict()
    return "Insufficient data for bias detection"
