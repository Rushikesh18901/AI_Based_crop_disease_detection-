# Confidence check utility
def check_confidence(confidence):
    if confidence < 0.75:
        return False
    return True