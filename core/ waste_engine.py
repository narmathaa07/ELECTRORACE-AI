def detect_waste(power, occupied):
    if power > 1000 and not occupied:
        return "⚠ AC running in empty room!"
    return "No abnormal usage detected"
