def calculate_dosage(dosage_per_litre, tank_size):
    if dosage_per_litre in ["None", "0"]:
        return "No pesticide required", "", "none"

    try:
        if "g" in dosage_per_litre:
            value = float(dosage_per_litre.replace("g", ""))

            total = value * tank_size

            per_litre = f"1 Litre → {value} g"
            total_text = f"{tank_size} Litres → {total} g"

            return per_litre, total_text, "g"

        elif "ml" in dosage_per_litre:
            value = float(dosage_per_litre.replace("ml", ""))

            total = value * tank_size

            per_litre = f"1 Litre → {value} ml"
            total_text = f"{tank_size} Litres → {total} ml"

            return per_litre, total_text, "ml"

    except:
        return "Invalid dosage", "", ""
