def detect_waste(ac_power, motion_detected):

    if ac_power > 1000 and motion_detected == False:
        return "⚠ Waste Detected: AC running in empty room"

    if ac_power > 1200:
        return "⚠ High energy usage detected"

    return "✔ Normal usage"
