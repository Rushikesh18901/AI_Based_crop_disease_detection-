def health_score(disease):

    if "healthy" in disease.lower():
        return 100
    elif "virus" in disease.lower():
        return 40
    else:
        return 70