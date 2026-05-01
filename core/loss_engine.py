import pandas as pd

def compute_loss(df):
    """
    Computes energy loss based on difference between input power and used power
    """

    if "power" not in df.columns or "power_used" not in df.columns:
        return df, 0

    df["loss"] = df["power"] - df["power_used"]

    total_loss = df["loss"].sum()

    return df, round(total_loss, 2)


def loss_breakdown(df):
    """
    Estimate which appliances contribute most to loss
    (Simulated based on typical household patterns)
    """

    return {
        "Air Conditioner Standby": 0.42,
        "Fridge Inefficiency": 0.28,
        "Idle Devices": 0.18,
        "Other Losses": 0.12
    }


def detect_loss_spikes(df):
    """
    Detect abnormal spikes in energy loss
    """

    if "loss" not in df.columns:
        return []

    threshold = df["loss"].mean() * 1.5

    spikes = df[df["loss"] > threshold]

    return spikes
