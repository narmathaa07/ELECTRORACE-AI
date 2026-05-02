# core/nilm_engine.py

def disaggregate_series(total_power):
    """Simple device disaggregation based on power levels"""
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
