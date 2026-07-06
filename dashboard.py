import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from config import REFRESH_TIME, WINDOW_SIZE
from src.predict import predict_health

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Grinding Machine Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Auto Refresh
# -----------------------------
st_autorefresh(
    interval=REFRESH_TIME * 1000,
    key="machine_refresh"
)

# -----------------------------
# Session State
# -----------------------------
if "event_log" not in st.session_state:
    st.session_state.event_log = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("⚙️ Grinding Machine")

    st.markdown("---")

    st.subheader("📡 System")

    st.success("Monitoring Active")

    st.markdown("### Communication")
    st.write("ESP32")
    st.write("⬇")
    st.write("RS485 (MAX485)")
    st.write("⬇")
    st.write("WiFi")
    st.write("⬇")
    st.write("Flask Server")
    st.write("⬇")
    st.write("CSV Storage")

    st.markdown("---")

    st.subheader("🤖 AI")

    st.write("Model : Machine Health")
    st.write(f"Refresh : {REFRESH_TIME} sec")

    st.markdown("---")

    st.caption("Lee Spring Internship")

# -----------------------------
# Load Live Data
# -----------------------------
try:
    df = pd.read_csv("data/live_machine_data.csv")

    if df.empty:
        st.warning("No machine data available.")
        st.stop()

except FileNotFoundError:
    st.error("live_machine_data.csv not found.")
    st.stop()

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# -----------------------------
# Process Data
# -----------------------------
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

current_row = df.iloc[-1]
graph_df = df.tail(WINDOW_SIZE)

latest_voltage = current_row["Voltage"]
latest_current = current_row["Current"]
latest_frequency = current_row["Frequency"]
latest_kw = current_row["kW"]
latest_kva = current_row["kVA"]
latest_pf = current_row["PowerFactor"]
latest_time = current_row["Timestamp"]

# -----------------------------
# ML Prediction
# -----------------------------
result = predict_health(
    latest_voltage,
    latest_current,
    latest_frequency,
    latest_kw,
    latest_kva,
    latest_pf
)

# -----------------------------
# Event History
# -----------------------------
event = {
    "Timestamp": latest_time,
    "Status": result["prediction"],
    "Confidence (%)": round(result["confidence"], 2),
    "AHI (%)": round(result["ahi"], 2)
}

if result["prediction"] != "Idle":

    if (
        len(st.session_state.event_log) == 0
        or st.session_state.event_log[-1]["Timestamp"] != latest_time
    ):
        st.session_state.event_log.append(event)

st.session_state.event_log = st.session_state.event_log[-100:]

history_df = pd.DataFrame(st.session_state.event_log)

# -----------------------------
# Header
# -----------------------------
st.title("⚙️ Grinding Machine Predictive Maintenance System")

st.markdown("""
### Live Monitoring Dashboard
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("🏭 **Machine:** Surface Grinding Machine")

with c2:

    from datetime import datetime

    # Time since last saved reading
    time_diff = (datetime.now() - latest_time).total_seconds()

    # If no new data for >10 sec, machine is idle
    if time_diff > 10:
        st.info("🔵 Machine State : IDLE")
    else:
        st.success("🟢 Machine State : RUNNING")

with c3:
    st.info(f"🕒 **Last Reading:** {latest_time}")

st.divider()

st.divider()

st.subheader("📊 Live Machine Overview")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="⚡ Voltage",
        value=f"{latest_voltage:.2f} V"
    )

with col2:
    st.metric(
        label="🔌 Current",
        value=f"{latest_current:.2f} A"
    )

with col3:
    st.metric(
        label="⚙️ Frequency",
        value=f"{latest_frequency:.2f} Hz"
    )

col4, spacer, col5 = st.columns([1, 1, 1])

with col4:
    st.metric(
        label="⚡ Power",
        value=f"{latest_kw:.2f} kW"
    )

with col5:
    st.metric(
        label="📈 Power Factor",
        value=f"{latest_pf:.2f}"
    )
st.divider()

st.subheader("🤖 AI Health Prediction")
if result["alert_level"] == "blue":

    st.info("🔵 MACHINE STATUS : IDLE")

elif result["alert_level"] == "green":

    st.success("🟢 MACHINE STATUS : HEALTHY")

elif result["alert_level"] == "yellow":

    st.warning("🟡 MACHINE STATUS : WARNING")

else:

    st.error("🔴 MACHINE STATUS : FAULT")

c1, c2 = st.columns(2)

if result["prediction"] == "Idle":

    with c1:
        st.metric("Prediction Confidence", "--")

    with c2:
        st.metric("Asset Health Index", "--")

else:

    with c1:
        st.metric(
            "Prediction Confidence",
            f"{result['confidence']:.2f}%"
        )

    with c2:
        st.metric(
            "Asset Health Index",
            f"{result['ahi']:.2f}%"
        )


st.info(result["recommendation"])

st.divider()

st.subheader("📈 Live Machine Trends")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Voltage")
    st.line_chart(
        graph_df.set_index("Timestamp")["Voltage"],
       width="stretch"
    )

with col2:
    st.markdown("### 🔌 Current")
    st.line_chart(
        graph_df.set_index("Timestamp")["Current"],
        width="stretch"
    )

col3, col4 = st.columns(2)

with col3:
    st.markdown("### ⚙️ Power")
    st.line_chart(
        graph_df.set_index("Timestamp")["kW"],
        width="stretch"
    )

with col4:
    st.markdown("### 📊 Power Factor")
    st.line_chart(
        graph_df.set_index("Timestamp")["PowerFactor"],
        width="stretch"
    )

st.markdown("### 🌀 Frequency")

st.line_chart(
    graph_df.set_index("Timestamp")["Frequency"],
    width="stretch"
)

st.divider()

st.subheader("📋 Event History")

st.dataframe(
    history_df.iloc[::-1].head(15),
    width="stretch",
    hide_index=True
)

st.divider()

st.subheader("🗄 Latest Machine Readings")

st.dataframe(
    df.tail(10).iloc[::-1],
    width="stretch",
    hide_index=True
)