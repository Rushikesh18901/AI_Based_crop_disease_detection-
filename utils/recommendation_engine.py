# Recommendation engine utility
import pandas as pd

# Load database once
db = pd.read_csv("database/disease_database.csv")

def get_recommendation(disease):

    result = db[db["Disease"] == disease]

    if result.empty:
        return "Not Available", "0", "0"

    pesticide = result.iloc[0]["Pesticide"]
    dosage = result.iloc[0]["Dosage_per_Litre"]
    interval = result.iloc[0]["Spray_Interval"]

    return pesticide, dosage, interval