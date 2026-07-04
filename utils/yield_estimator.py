def yield_loss(disease):

    if "healthy" in disease.lower():
        return "0%"
    elif "virus" in disease.lower():
        return "40-60%"
    else:
        return "20-30%"