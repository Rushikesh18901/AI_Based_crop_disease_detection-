# Reminder utility
from datetime import datetime, timedelta

def next_spray(interval):

    if interval in ["None", "0"]:
        return "No spray required"

    try:
        days = int(interval.split()[0])
        next_date = datetime.today() + timedelta(days=days)
        return next_date.strftime("%d-%m-%Y")

    except:
        return "Invalid interval data"