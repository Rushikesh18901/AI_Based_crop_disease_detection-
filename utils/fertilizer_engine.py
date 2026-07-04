import pandas as pd


# ==============================
# LOAD DATABASE (once)
# ==============================
try:
    df = pd.read_csv("database/fertilizer_database.csv")
except Exception as e:
    print("❌ Error loading fertilizer database:", e)
    df = pd.DataFrame()


# ==============================
# MAIN FUNCTION
# ==============================
def get_fertilizer(disease):

    try:
        # Find matching row
        row = df[df["Disease"] == disease]

        if not row.empty:

            fert = row.iloc[0]["Fertilizer"]
            usage = row.iloc[0]["Usage"]
            freq = row.iloc[0]["Frequency"]

            # Handle healthy case
            if fert == "None":
                return (
                    "No fertilizer needed",
                    "Crop is healthy",
                    "No schedule required"
                )

            return fert, usage, freq

        # If disease not found
        return (
            "General NPK 19:19:19",
            "5g per litre foliar spray",
            "Weekly"
        )

    except Exception as e:
        print("❌ Fertilizer Engine Error:", e)

        return (
            "NPK 19:19:19",
            "5g per litre",
            "Weekly"
        )