import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Heatmap & Waste Analysis", page_icon="🔥", layout="wide")

st.title("🔥 Peak Hours Heatmap & Top Waste Devices")
st.markdown("---")

# Check data
if "energy_data" not in st.session_state:
    st.warning("⚠️ Please upload dataset from the Home page first")
    st.info("Go to the **Home** page to upload your energy data")
    st.stop()

df = st.session_state["energy_data"].copy()

if df.empty or "power" not in df.columns:
    st.error("Invalid data format. Make sure your data has a 'power' column.")
    st.stop()

# Ensure timestamp is datetime
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date
else:
    # Create synthetic timestamp if not exists
    df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['date'] = df['timestamp'].dt.date

# Define functions
def detect_top_waste_devices(df, n_devices=5):
    """Detect top energy waste devices based on consumption patterns"""
    
    # Device profiles with typical power ranges (Watts)
    devices = {
        "Air Conditioner": {"min": 800, "max": 2500, "efficiency": 0.7},
        "Water Heater": {"min": 1500, "max": 3000, "efficiency": 0.6},
        "Refrigerator": {"min": 100, "max": 400, "efficiency": 0.85},
        "Washing Machine": {"min": 400, "max": 1200, "efficiency": 0.65},
        "Dryer": {"min": 2000, "max": 4000, "efficiency": 0.55},
        "Dishwasher": {"min": 1200, "max": 2400, "efficiency": 0.7},
        "Electric Oven": {"min": 2000, "max": 3500, "efficiency": 0.6},
        "Microwave": {"min": 600, "max": 1500, "efficiency": 0.65},
        "TV": {"min": 50, "max": 300, "efficiency": 0.9},
        "Computer": {"min": 100, "max": 500, "efficiency": 0.85},
        "Lighting": {"min": 20, "max": 200, "efficiency": 0.95},
        "Pump": {"min": 300, "max": 1000, "efficiency": 0.7},
        "Iron": {"min": 800, "max": 2000, "efficiency": 0.6},
        "Vacuum Cleaner": {"min": 500, "max": 1500, "efficiency": 0.65},
        "Fan": {"min": 30, "max": 100, "efficiency": 0.85},
    }
    
    waste_scores = []
    total_energy = df['power'].sum()
    
    for device, specs in devices.items():
        # Estimate device energy based on typical usage patterns
        device_energy = 0
        waste = 0
        
        # Check each hour for device signatures
        for hour in range(24):
            hour_mask = df['hour'] == hour
            if hour_mask.any():
                avg_power = df.loc[hour_mask, 'power'].mean()
                
                # Check if power matches device range
                if specs['min'] <= avg_power <= specs['max']:
                    # Estimate device contribution
                    device_contribution = avg_power * len(df.loc[hour_mask]) * 0.3
                    device_energy += device_contribution
                    
                    # Calculate waste (inefficiency + off-hours usage)
                    efficiency_loss = device_contribution * (1 - specs['efficiency'])
                    
                    # Check for waste during off-peak hours (midnight to 6 AM)
                    if hour < 6 or hour > 23:
                        off_hour_waste = device_contribution * 0.5
                    else:
                        off_hour_waste = 0
                    
                    waste += efficiency_loss + off_hour_waste
        
        if device_energy > 0:
            waste_percentage = (waste / device_energy) * 100 if device_energy > 0 else 0
            waste_scores.append({
                'device': device,
                'estimated_energy_kwh': round(device_energy / 1000, 2),
                'waste_kwh': round(waste / 1000, 2),
                'waste_percentage': round(waste_percentage, 1),
                'efficiency': round(specs['efficiency'] * 100, 1)
            })
    
    # Sort by waste percentage
    waste_scores.sort(key=lambda x: x['waste_percentage'], reverse=True)
    
    return waste_scores[:n_devices]

# Create heatmap data
st.subheader("🗺️ Peak Hours Heatmap")

# Prepare data for heatmap
heatmap_data = df.groupby(['hour', 'day_of_week'])['power'].mean().reset_index()

# Order days correctly
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
heatmap_data['day_of_week'] = pd.Categorical(heatmap_data['day_of_week'], categories=day_order, ordered=True)

# Create pivot table for heatmap
pivot_table = heatmap_data.pivot(index='hour', columns='day_of_week', values='power')

# Create heatmap using plotly
fig = px.imshow(
    pivot_table.values,
    labels=dict(x="Day of Week", y="Hour", color="Power (W)"),
    x=pivot_table.columns,
    y=pivot_table.index,
    color_continuous_scale='RdYlGn_r',
    aspect="auto",
    title="Energy Consumption Heatmap by Hour and Day"
)

fig.update_layout(
    height=500,
    title_font_size=20,
    xaxis_title="Day of Week",
    yaxis_title="Hour of Day"
)

st.plotly_chart(fig, use_container_width=True)

# Peak hour insights
st.subheader("⏰ Peak Hour Insights")

col1, col2, col3 = st.columns(3)

# Find peak hour overall
peak_hour = df.groupby('hour')['power'].mean().idxmax()
peak_value = df.groupby('hour')['power'].mean().max()

with col1:
    st.metric("🌙 Overall Peak Hour", f"{int(peak_hour)}:00", f"{peak_value:.0f} W avg")

# Find peak day
peak_day = df.groupby('day_of_week')['power'].mean().idxmax()
peak_day_value = df.groupby('day_of_week')['power'].mean().max()

with col2:
    st.metric("📅 Peak Day", peak_day, f"{peak_day_value:.0f} W avg")

# Find lowest consumption period
lowest_hour = df.groupby('hour')['power'].mean().idxmin()
lowest_value = df.groupby('hour')['power'].mean().min()

with col3:
    st.metric("🌙 Lowest Hour", f"{int(lowest_hour)}:00", f"{lowest_value:.0f} W avg")

# Peak periods analysis
st.subheader("📊 Peak Periods Analysis")

peak_periods = {
    "Morning Peak (6-9 AM)": df[(df['hour'] >= 6) & (df['hour'] <= 9)]['power'].mean(),
    "Afternoon Peak (1-5 PM)": df[(df['hour'] >= 13) & (df['hour'] <= 17)]['power'].mean(),
    "Evening Peak (6-11 PM)": df[(df['hour'] >= 18) & (df['hour'] <= 23)]['power'].mean(),
    "Night Low (12-5 AM)": df[(df['hour'] >= 0) & (df['hour'] <= 5)]['power'].mean()
}

peak_df = pd.DataFrame(list(peak_periods.items()), columns=['Period', 'Average Power (W)'])

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(peak_df.set_index('Period'))

with col2:
    for period, power in peak_periods.items():
        st.write(f"**{period}:** {power:.1f} W")
        percentage = (power / df['power'].mean()) * 100
        st.progress(min(percentage / 100, 1.0))

st.markdown("---")

# Top Waste Devices Section
st.subheader("🗑️ Top Waste Devices Analysis")

# Detect top waste devices
waste_devices = detect_top_waste_devices(df)

if waste_devices:
    # Display waste devices in a table
    waste_df = pd.DataFrame(waste_devices)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            waste_df,
            column_config={
                "device": "Device",
                "estimated_energy_kwh": st.column_config.NumberColumn("Energy (kWh)", format="%.2f"),
                "waste_kwh": st.column_config.NumberColumn("Waste (kWh)", format="%.2f"),
                "waste_percentage": st.column_config.NumberColumn("Waste %", format="%.1f%%"),
                "efficiency": st.column_config.NumberColumn("Efficiency %", format="%.1f%%")
            },
            use_container_width=True
        )
    
    with col2:
        # Show top waste device prominently
        top_waste = waste_devices[0]
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%); 
                    padding: 1.5rem; 
                    border-radius: 1rem; 
                    color: white;
                    text-align: center;">
            <h3>🔥 Top Waste Device</h3>
            <h2>{top_waste['device']}</h2>
            <p>Waste: {top_waste['waste_kwh']} kWh ({top_waste['waste_percentage']}%)</p>
            <p>Efficiency: {top_waste['efficiency']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Waste visualization
    st.subheader("📊 Waste Breakdown")
    
    fig2 = go.Figure(data=[
        go.Bar(name='Energy Used', x=[d['device'] for d in waste_devices], 
               y=[d['estimated_energy_kwh'] for d in waste_devices]),
        go.Bar(name='Energy Wasted', x=[d['device'] for d in waste_devices], 
               y=[d['waste_kwh'] for d in waste_devices])
    ])
    
    fig2.update_layout(
        barmode='group',
        title="Energy vs Waste by Device",
        xaxis_title="Device",
        yaxis_title="Energy (kWh)",
        height=400
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
else:
    st.info("No significant waste patterns detected")

st.markdown("---")

# Waste Reduction Recommendations
st.subheader("💡 Waste Reduction Recommendations")

if waste_devices:
    for device in waste_devices[:3]:
        if device['waste_percentage'] > 30:
            st.error(f"🔴 **{device['device']}** - High waste ({device['waste_percentage']}%)")
            st.write(f"   *Recommendation:* Check for inefficient operation or replace with energy-efficient model")
        elif device['waste_percentage'] > 15:
            st.warning(f"🟡 **{device['device']}** - Moderate waste ({device['waste_percentage']}%)")
            st.write(f"   *Recommendation:* Optimize usage schedule and maintenance")
        else:
            st.info(f"🟢 **{device['device']}** - Low waste ({device['waste_percentage']}%)")
            st.write(f"   *Recommendation:* Continue monitoring")

# Potential savings
total_waste = sum([d['waste_kwh'] for d in waste_devices])
if total_waste > 0:
    st.markdown("---")
    st.subheader("💰 Potential Savings")
    
    # Assuming RM 0.22 per kWh (TNB rate)
    cost_per_kwh = 0.22
    monthly_waste = total_waste * 30 / len(df) if len(df) > 0 else total_waste
    monthly_cost = monthly_waste * cost_per_kwh
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Waste (Period)", f"{total_waste:.2f} kWh")
    col2.metric("Est. Monthly Waste", f"{monthly_waste:.2f} kWh")
    col3.metric("Monthly Cost Savings", f"RM {monthly_cost:.2f}")

# Refresh button
if st.button("🔄 Refresh Analysis", use_container_width=True):
    st.rerun()
