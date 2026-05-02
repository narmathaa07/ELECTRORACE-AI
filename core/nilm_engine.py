# core/nilm_engine.py

def disaggregate_series(total_power):
    """
    Simple device disaggregation based on power levels
    Can handle both single values and pandas Series/DataFrames
    """
    # If total_power is a pandas Series or DataFrame, use the last value
    if hasattr(total_power, '__len__') and not isinstance(total_power, (int, float)):
        # For Series, get the latest value
        if hasattr(total_power, 'iloc'):
            total_power = total_power.iloc[-1]
        else:
            total_power = total_power[-1] if len(total_power) > 0 else 0
    
    # Ensure total_power is a numeric value
    total_power = float(total_power)
    
    devices = {
        "HVAC": 0,
        "Lighting": 0,
        "Electronics": 0,
        "Other": 0
    }
    
    if total_power > 2000:
        devices["HVAC"] = total_power * 0.5
        devices["Lighting"] = total_power * 0.1
        devices["Electronics"] = total_power * 0.25
        devices["Other"] = total_power * 0.15
    elif total_power > 1000:
        devices["HVAC"] = total_power * 0.45
        devices["Lighting"] = total_power * 0.12
        devices["Electronics"] = total_power * 0.28
        devices["Other"] = total_power * 0.15
    elif total_power > 500:
        devices["HVAC"] = total_power * 0.4
        devices["Lighting"] = total_power * 0.15
        devices["Electronics"] = total_power * 0.3
        devices["Other"] = total_power * 0.15
    else:
        devices["Lighting"] = total_power * 0.3
        devices["Electronics"] = total_power * 0.5
        devices["Other"] = total_power * 0.2
    
    return {k: round(v, 2) for k, v in devices.items() if v > 0}
