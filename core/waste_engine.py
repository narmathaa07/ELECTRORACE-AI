# core/waste_engine.py

def compute_loss(df):
    """Calculate energy loss from the dataframe"""
    if df is None or df.empty:
        return df
    
    df = df.copy()
    if "power_used" in df.columns:
        df["loss"] = df["power"] - df["power_used"]
    else:
        df["loss"] = df["power"] * 0.1
    return df

def detect_waste(power, occupied=False):
    """Detect energy waste based on power consumption"""
    if power > 1000 and not occupied:
        return "⚠ High power usage in empty condition - Consider turning off devices"
    elif power > 500 and not occupied:
        return "⚡ Moderate power usage while unoccupied - Some devices may be left on"
    elif power > 1000 and occupied:
        return "💡 High power usage - Check for energy efficiency opportunities"
    else:
        return "✅ Normal energy usage"
