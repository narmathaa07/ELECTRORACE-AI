def predict_bill(df):
    avg_power = df["power"].mean()
    tariff = 0.218  # RM per kWh approx
    daily_kwh = avg_power / 1000 * 24
    monthly_bill = daily_kwh * 30 * tariff
    return round(monthly_bill, 2)
