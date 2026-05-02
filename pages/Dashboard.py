import streamlit as st
import os
import sys

st.title("🔍 DIAGNOSTIC MODE")

# Show current directory
st.write("**Current working directory:**", os.getcwd())

# List all files in current directory
st.write("**Files in current directory:**")
for file in os.listdir("."):
    st.write(f"  - {file}")

# Check if core folder exists
if os.path.exists("core"):
    st.success("✅ 'core' folder exists")
    st.write("**Files in core folder:**")
    for file in os.listdir("core"):
        st.write(f"  - {file}")
        # Check if it's a file or directory
        full_path = os.path.join("core", file)
        if os.path.isfile(full_path):
            st.write(f"    (file, size: {os.path.getsize(full_path)} bytes)")
else:
    st.error("❌ 'core' folder does NOT exist!")

# Check for __init__.py
init_path = "core/__init__.py"
if os.path.exists(init_path):
    st.success(f"✅ {init_path} exists")
else:
    st.error(f"❌ {init_path} is MISSING - This is critical!")

# Check specific files
for filename in ["nilm_engine.py", "waste_engine.py"]:
    filepath = f"core/{filename}"
    if os.path.exists(filepath):
        st.success(f"✅ {filepath} exists")
        # Try to read first few lines
        try:
            with open(filepath, 'r') as f:
                first_lines = f.readlines()[:5]
                st.code(''.join(first_lines), language='python')
        except:
            st.error(f"Could not read {filepath}")
    else:
        st.error(f"❌ {filepath} is MISSING!")

# Show Python path
st.write("**Python sys.path:**")
for path in sys.path[:5]:
    st.write(f"  - {path}")

st.stop()  # Stop here to see diagnostic results
    

