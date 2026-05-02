def compute_loss(df):
    if "power_used" in df.columns:
        df["loss"] = df["power"] - df["power_used"]
    else:
        df["loss"] = df["power"] * 0.1
    return df

def detect_waste(power, occupied=False):
    if power > 1000 and not occupied:
        return "⚠ High power usage in empty condition"
    return "Normal usage"
