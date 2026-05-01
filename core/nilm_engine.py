def disaggregate(total_power):

    return {
        "AC": total_power * 0.55,
        "Fridge": total_power * 0.15,
        "TV": total_power * 0.10,
        "Fan": total_power * 0.05,
        "Others": total_power * 0.15
    }
