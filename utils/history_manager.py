# History manager utility
import pandas as pd
import os
from datetime import datetime

FILE_PATH = "database/history.csv"

def save_history(plant, disease, confidence, pesticide):
    data = {
        "Date": datetime.now().strftime("%d-%m-%Y"),
        "Plant": plant,
        "Disease": disease,
        "Confidence": round(confidence, 2),
        "Pesticide": pesticide
    }

    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    else:
        df = pd.DataFrame([data])

    df.to_csv(FILE_PATH, index=False)