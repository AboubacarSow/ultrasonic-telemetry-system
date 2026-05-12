import streamlit as st
import serial
import time
from collections import deque
import plotly.graph_objects as go

# ---------- CONFIG ----------
PORT = "/dev/ttyUSB0"
BAUD = 9600

# ---------- INIT ----------
st.set_page_config(page_title="Ultrasonic Telemetry", layout="wide")
st.title("📡 Ultrasonic Telemetry System")

# ---------- SESSION STATE ----------
if "data" not in st.session_state:
    st.session_state.data = deque(maxlen=100)

if "running" not in st.session_state:
    st.session_state.running = False

if "ser" not in st.session_state:
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)
        ser.flushInput()
        st.session_state.ser = ser
        st.success("Serial connected")
    except Exception as e:
        st.error(f"Serial connection failed: {e}")
        st.stop()

ser = st.session_state.ser

# ---------- SENSOR ----------
def read_sensor():
    try:
        line = ser.readline().decode(errors="ignore").strip()
        value = int(line)
        return value if value >= 0 else None
    except:
        return None

# ---------- UI CONTROLS ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("Start"):
        st.session_state.running = True

with col2:
    if st.button("Stop"):
        st.session_state.running = False

# ---------- PLOT PLACEHOLDER ----------
placeholder = st.empty()

# ---------- LIVE UPDATE ----------
if st.session_state.running:

    value = read_sensor()

    if value is not None:
        st.session_state.data.append(value)

    # ---- DISPLAY CURRENT VALUE ----
    if len(st.session_state.data) > 0:
        st.metric("Current Distance (cm)", st.session_state.data[-1])

    # ---- PLOT ----
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=list(st.session_state.data),
        mode="lines+markers",
        name="Distance (cm)"
    ))

    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis_range=[0, 200],
        template="plotly_dark"
    )

    placeholder.plotly_chart(fig, use_container_width=True)

    time.sleep(0.1)
    st.rerun()