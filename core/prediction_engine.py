# core/prediction_engine.py

def predict_bill(df, rate_per_kwh=0.12):
    """Predict electricity bill based on usage"""
    if df is None or df.empty:
        return 0
    
    if "power" in df.columns:
        total_wh = df["power"].sum()
        total_kwh = total_wh / 1000
        predicted_bill = total_kwh * rate_per_kwh
        return round(predicted_bill, 2)
    else:
        return 0

def predict_future_usage(df, days=30):
    """Predict future energy usage"""
    if df is None or df.empty:
        return 0
    
    avg_daily = df["power"].sum() / len(df) / 1000 if len(df) > 0 else 0
    return avg_daily * days
