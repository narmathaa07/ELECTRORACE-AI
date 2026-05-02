import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="ElectroRace AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-title {
        font-size: 4rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        transition: transform 0.3s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .stat-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">⚡ ElectroRace AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart Energy Management with NILM Technology</div>', unsafe_allow_html=True)

st.markdown("---")

# Hero Section with columns
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("https://cdn-icons-png.flaticon.com/512/3038/3038512.png", width=150)
    st.markdown("### Transform Your Energy Usage")
    st.write("""
    **ElectroRace AI** uses Non-Intrusive Load Monitoring (NILM) to analyze your electricity consumption,
    detect waste, and provide AI-powered recommendations to save energy and reduce bills.
    """)

st.markdown("---")

# Features Section
st.subheader("🎯 Key Features")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊</h3>
        <h4>Live Dashboard</h4>
        <p>Real-time energy monitoring</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🤖</h3>
        <h4>NILM Analysis</h4>
        <p>Device-level disaggregation</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🗑️</h3>
        <h4>Waste Detection</h4>
        <p>Identify energy waste</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <h3>💰</h3>
        <h4>Bill Prediction</h4>
        <p>Forecast monthly costs</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Data Upload Section
st.subheader("📂 Get Started - Upload Your Energy Data")

uploaded_file = st.file_uploader(
    "Choose a CSV file with energy consumption data",
    type=['csv'],
    help="File should contain 'timestamp' and 'power' columns"
)

# Sample data generator
with st.expander("📊 Or use sample data"):
    st.write("Don't have data? Generate a sample dataset:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        days = st.slider("Number of days", 1, 30, 7)
    
    with col2:
        household_type = st.selectbox("Household type", ["Small (1-2 people)", "Medium (3-4 people)", "Large (5+ people)"])
    
    if st.button("🎲 Generate Sample Dataset"):
        # Generate sample data based on household type
        hours = days * 24
        start_date = datetime.now() - timedelta(hours=hours)
        
        if household_type == "Small (1-2 people)":
            base_peak = 1500
            base_avg = 300
        elif household_type == "Medium (3-4 people)":
            base_peak = 2500
            base_avg = 500
        else:
            base_peak = 3500
            base_avg = 800
        
        timestamps = [start_date + timedelta(hours=i) for i in range(hours)]
        
        # Generate realistic pattern
        power = []
        for i in range(hours):
            hour = i % 24
            # Morning peak
            if 7 <= hour <= 9:
                p = np.random.normal(base_peak * 0.6, 100)
            # Afternoon AC
            elif 13 <= hour <= 17:
                p = np.random.normal(base_peak * 0.5, 150)
            # Evening peak
            elif 18 <= hour <= 23:
                p = np.random.normal(base_peak * 0.8, 200)
            # Night low
            elif 0 <= hour <= 5:
                p = np.random.normal(base_avg * 0.3, 50)
            else:
                p = np.random.normal(base_avg, 100)
            
            power.append(max(p, 50))
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'power': [round(p, 2) for p in power],
            'power_used': [round(p * 0.92, 2) for p in power]
        })
        
        st.session_state["energy_data"] = df
        st.success(f"✅ Sample dataset generated! {len(df)} data points created.")
        st.dataframe(df.head(10))
        
        if st.button("🚀 Go to Dashboard"):
            st.switch_page("pages/Dashboard.py")

# Process uploaded file
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # Check required columns
        if 'power' not in df.columns:
            st.error("❌ CSV must contain a 'power' column")
        else:
            # Convert timestamp if exists
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            else:
                df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='H')
            
            # Add power_used if not present
            if 'power_used' not in df.columns:
                df['power_used'] = df['power'] * 0.95
            
            st.session_state["energy_data"] = df
            st.success(f"✅ Successfully loaded {len(df)} data points!")
            
            # Show preview
            st.subheader("Data Preview")
            st.dataframe(df.head(10))
            
            # Show stats
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Records", len(df))
            col2.metric("Avg Power (W)", f"{df['power'].mean():.1f}")
            col3.metric("Peak Power (W)", f"{df['power'].max():.1f}")
            
            if st.button("📊 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/Dashboard.py")
                
    except Exception as e:
        st.error(f"Error reading file: {e}")

st.markdown("---")

# Quick Stats
st.subheader("📈 Energy Insights")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <h3>⚡</h3>
        <h4>0-2000W</h4>
        <p>Typical Home Load</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <h3>💰</h3>
        <h4>RM0.22/kWh</h4>
        <p>Average TNB Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <h3>🌍</h3>
        <h4>0.5kg CO2</h4>
        <p>Saved per kWh</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <h3>🎯</h3>
        <h4>30%</h4>
        <p>Potential Savings</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.caption("© 2024 ElectroRace AI | Smart Energy Management System | Powered by NILM Technology")
