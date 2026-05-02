def disaggregate_series(power_series):
    return {
        "Air Conditioner": power_series * 0.5,
        "Fridge": power_series * 0.2,
        "Fan": power_series * 0.1,
        "TV": power_series * 0.2
    }
