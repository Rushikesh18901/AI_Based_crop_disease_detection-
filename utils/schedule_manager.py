import pandas as pd
import os
from datetime import datetime


def save_schedule(plant, disease, next_date):
    data = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Plant": plant,
        "Disease": disease,
        "Next_Spray": next_date,
    }

    df = pd.DataFrame([data])

    csv_path = "database/spray_schedule.csv"

    if os.path.exists(csv_path):
        df.to_csv(csv_path, mode="a", header=False, index=False)
    else:
        df.to_csv(csv_path, mode="w", header=True, index=False)
