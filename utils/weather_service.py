import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    if not API_KEY:
        print("API key not found")
        return None

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        print(f"Weather API response: {data}")

        if data.get("cod") != 200:
            print(f"API error: {data.get('message', 'Unknown error')}")
            return None

        weather = {
            "temperature": round(data["main"]["temp"]),
            "humidity": data["main"]["humidity"],
            "condition": data["weather"][0]["main"],
        }

        return weather

    except Exception as e:
        print(f"Weather Error: {e}")
        return None


def spray_advice(weather):
    if weather is None:
        return "Weather data not available"

    temp = weather["temperature"]
    humidity = weather["humidity"]
    condition = weather["condition"]

    if condition.lower() in ["rain", "drizzle"]:
        return "Avoid spraying - Rain will wash pesticide"

    elif humidity > 80:
        return "High humidity - Risk of fungal disease"

    elif temp > 35:
        return "Too hot - Spray in morning or evening"

    else:
        return "Good weather for spraying"
