import streamlit as st

st.set_page_config(page_title="Energy Dashboard", layout="wide")

st.title("🏠 Energy Dashboard")
st.caption("AI-powered real-time energy monitoring")

# -------------------------------
# SAFE IMPORTS (NO CRASH)
# -------------------------------
try:
    from core.waste_engine import detect_waste
    from core.nilm_engine import disaggregate
    modules_loaded = True
except Exception as e:
    st.error("⚠ Backend modules not found. Using demo mode.")
    modules_loaded = False

# -------------------------------
# DATA INPUT (UPLOAD OR DEFAULT)
# -------------------------------
uploaded_file = st.file_uploader("Upload Energy Dataset (optional)", type=["csv"])

total_power = 2400  # default fallback

if uploaded_file:
    import pandas as pd
    try:
        df = pd.read_csv(uploaded_file)
        if "power" in df.columns:
            total_power = df["power"].mean()
            st.success("Dataset loaded successfully")
        else:
            st.warning("Column 'power' not found. Using default data.")
    except:
        st.warning("Error reading file. Using default data.")
else:
    st.info("Using simulated real-time data")

# -------------------------------
# NILM AI (DEVICE BREAKDOWN)
# -------------------------------
if modules_loaded:
    devices = disaggregate(total_power)
else:
    # fallback demo data
    devices = {
        "Air Conditioner": total_power * 0.5,
        "Fan": total_power * 0.1,
        "TV": total_power * 0.15,
        "Fridge": total_power * 0.25
    }

# -------------------------------
# TOP METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("⚡ Total Load", f"{round(total_power,2)} W")
col2.metric("📊 Energy Score", "78 / 100")
col3.metric("💰 Estimated Bill", "RM 185")

# -------------------------------
# DEVICE LIST
# -------------------------------
st.subheader("🔌 Live Appliance Breakdown")

for device, power in devices.items():
    st.write(f"{device}: {round(power,2)} W")

# -------------------------------
# AI INSIGHT (AC WASTE DETECTION)
# -------------------------------
st.subheader("🧠 AI Insight")

ac_power = 0

for key in devices:
    if "air" in key.lower() or "ac" in key.lower():
        ac_power = devices[key]
        break

if modules_loaded:
    if ac_power > 0:
        result = detect_waste(ac_power, False)
        st.warning(result)
    else:
        st.info("No AC detected")
else:
    st.warning("⚠ Demo mode: AC may be wasting energy")

# -------------------------------
# VISUAL CHART
# -------------------------------
import pandas as pd

df_devices = pd.DataFrame({
    "Device": list(devices.keys()),
    "Power": list(devices.values())
})

st.subheader("📊 Energy Distribution")

st.bar_chart(df_devices.set_index("Device"))

# -------------------------------
# FOOTER
# -------------------------------
st.caption("ElectroTrace AI • Smart Energy Monitoring System")
st.bar_chart(df_devices.set_index("Device"))
