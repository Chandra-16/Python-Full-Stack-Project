import streamlit as st
import requests
from datetime import datetime

# --- Backend API Base URL ---
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EnergyFlo Dashboard ⚡", layout="wide")
st.title("⚡ EnergyFlo: Home Energy Management 🏠")

# ----------------------------------
# Sidebar Navigation
# ----------------------------------
menu = [
    "Add User 👤",
    "Add Home 🏡",
    "Add Appliance 🔌",
    "Add Energy Reading 🔋",
    "View Home Summary 📊",
    "View Appliance Chart 📈"
]
choice = st.sidebar.selectbox("Menu", menu)

# ----------------------------------
# 1️⃣ Add User
# ----------------------------------
if choice == "Add User 👤":
    st.subheader("➕ Add a New User 👤")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Add User ✅"):
        # Users table is currently handled via API? If not, you can skip or mock user_id
        st.success("User added successfully! (Add users manually in DB for now) 🎉")

# ----------------------------------
# 2️⃣ Add Home
# ----------------------------------
elif choice == "Add Home 🏡":
    st.subheader("➕ Add a New Home 🏡")
    
    user_id = st.text_input("👤 User ID (UUID)")
    address = st.text_input("🏠 Address")
    utility_provider = st.text_input("⚡ Utility Provider")
    
    if st.button("Add Home ✅"):
        if not user_id or not address:
            st.error("❌ User ID and Address are required.")
        else:
            response = requests.post(f"{BASE_URL}/homes/", json={
                "user_id": user_id,
                "address": address,
                "utility_provider": utility_provider
            })
            if response.status_code == 201:
                st.success("🏡 Home added successfully! 🎉")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.text}")

# ----------------------------------
# 3️⃣ Add Appliance
# ----------------------------------
elif choice == "Add Appliance 🔌":
    st.subheader("➕ Add Appliance 🔌")
    
    home_id = st.text_input("🏠 Home ID (UUID)")
    name = st.text_input("🔌 Appliance Name")
    type_ = st.text_input("⚙️ Type")
    model = st.text_input("📝 Model")
    wattage = st.number_input("⚡ Wattage (W)", min_value=0)
    
    if st.button("Add Appliance ✅"):
        if not home_id or not name or not type_:
            st.error("❌ Home ID, Name, and Type are required.")
        else:
            response = requests.post(f"{BASE_URL}/appliances/", json={
                "home_id": home_id,
                "name": name,
                "type": type_,
                "model": model,
                "wattage": wattage
            })
            if response.status_code == 201:
                st.success("🔌 Appliance added successfully! 🎉")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.text}")

# ----------------------------------
# 4️⃣ Add Energy Reading
# ----------------------------------
elif choice == "Add Energy Reading 🔋":
    st.subheader("➕ Add Energy Reading 🔋")
    
    appliance_id = st.text_input("🔌 Appliance ID (UUID)")
    consumption_kwh = st.number_input("⚡ Consumption (kWh)", min_value=0.0, format="%.3f")
    duration_minutes = st.number_input("⏱ Duration (minutes)", min_value=0)
    
    if st.button("Add Reading ✅"):
        if not appliance_id:
            st.error("❌ Appliance ID is required.")
        else:
            response = requests.post(f"{BASE_URL}/readings/", json={
                "appliance_id": appliance_id,
                "consumption_kwh": consumption_kwh,
                "duration_minutes": duration_minutes
            })
            if response.status_code == 201:
                st.success("🔋 Energy reading added! 🎉")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.text}")

# ----------------------------------
# 5️⃣ View Home Summary
# ----------------------------------
elif choice == "View Home Summary 📊":
    st.subheader("📊 Home Energy Summary")
    home_id = st.text_input("🏠 Home ID (UUID)")
    cost_per_kwh = st.number_input("💲 Cost per kWh ($)", value=0.15, format="%.2f")
    
    if st.button("Get Summary ✅"):
        if not home_id:
            st.error("❌ Home ID is required.")
        else:
            response = requests.get(f"{BASE_URL}/homes/{home_id}/summary", params={"cost_per_kwh": cost_per_kwh})
            if response.status_code == 200:
                data = response.json()
                st.json(data)
                st.metric("⚡ Total kWh", data.get("total_kwh"))
                st.metric("💲 Total Cost ($)", data.get("total_cost"))
                st.write("🏆 Highest Consumption Appliance:", data.get("highest_consumer"))
                st.write("📊 Appliance Breakdown:")
                st.dataframe(data.get("appliance_breakdown"))
            else:
                st.error(f"❌ Error: {response.text}")

# ----------------------------------
# 6️⃣ View Appliance Chart
# ----------------------------------
elif choice == "View Appliance Chart 📈":
    st.subheader("📈 Appliance Energy Chart")
    appliance_id = st.text_input("🔌 Appliance ID (UUID)")
    
    if st.button("Show Chart ✅"):
        if not appliance_id:
            st.error("❌ Appliance ID is required.")
        else:
            response = requests.get(f"{BASE_URL}/appliances/{appliance_id}/chart_data")
            if response.status_code == 200:
                data = response.json()
                st.line_chart({"⚡ Consumption (kWh)": data["data"]}, use_container_width=True)
            else:
                st.error(f"❌ Error: {response.text}")