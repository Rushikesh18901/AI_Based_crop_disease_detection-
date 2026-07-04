# Safety alert utility
def pesticide_safety(pesticide):

    safety_data = {
        "Mancozeb": "Wear gloves and mask. Avoid inhalation.",
        "Chlorothalonil": "Avoid skin contact. Use protective clothing.",
        "Azoxystrobin": "Do not spray near water sources.",
        "Propiconazole": "Use mask and avoid inhalation.",
        "Copper Fungicide": "Avoid excessive use.",
        "Neem Oil": "Safe but avoid eye contact.",
        "None": "No pesticide required."
    }

    return safety_data.get(pesticide, "Follow general pesticide safety precautions.")