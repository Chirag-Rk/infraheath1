import time
import requests
import pandas as pd
import streamlit as st
import base64
import os

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────

API_BASE = "http://127.0.0.1:8001"

# Encode background image to base64
bg_image_path = r"C:\Users\hp\Downloads\Infrastructure\w-1200_h-630_m-crop__MCG Construction - Recruitment and Logistics-06.png"
if os.path.exists(bg_image_path):
    with open(bg_image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
else:
    img_base64 = None

st.set_page_config(
    page_title="Urban Infrastructure Health Dashboard",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Industrial / Brutalist dark theme
# ─────────────────────────────────────────────

# Build CSS with or without background image
if img_base64:
    bg_css = f"""
    .stApp {{
        background: linear-gradient(rgba(13, 15, 20, 0.82), rgba(13, 15, 20, 0.82)), 
                    url('data:image/png;base64,{img_base64}') center/cover no-repeat fixed;
        background-attachment: fixed;
        color: #c8cdd8;
    }}
    """
else:
    bg_css = """
    .stApp {
        background: #0d0f14;
        color: #c8cdd8;
    }
    """

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@300;400;600;700;900&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Barlow', sans-serif;
    }}

    {bg_css}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: #111318 !important;
        border-right: 1px solid #2a2e3a;
    }}

    /* Headers */
    h1, h2, h3 {{
        font-family: 'Barlow', sans-serif;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #e8ecf4;
    }}

    /* Metric cards */
    [data-testid="metric-container"] {{
        background: #161a23;
        border: 1px solid #2a2e3a;
        border-radius: 4px;
        padding: 12px;
    }}

    /* Status badges */
    .badge-healthy  {{ background:#0d3320; color:#2ecc71; border:1px solid #2ecc71; }}
    .badge-warning  {{ background:#332b0a; color:#f1c40f; border:1px solid #f1c40f; }}
    .badge-critical {{ background:#331209; color:#e67e22; border:1px solid #e67e22; }}
    .badge-failure  {{ background:#2d0a0a; color:#e74c3c; border:1px solid #e74c3c; }}
    .status-badge {{
        display:inline-block; font-family:'Share Tech Mono',monospace;
        font-size:1.1rem; font-weight:700; padding:6px 20px;
        border-radius:3px; letter-spacing:2px; text-transform:uppercase;
    }}

    /* Score bar */
    .score-bar-wrap {{ margin: 8px 0 4px; }}
    .score-label {{ font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:#6b7280; margin-bottom:4px; }}

    /* Anomaly log */
    .anomaly-item {{
        background: #1a0e0e;
        border-left: 3px solid #e74c3c;
        padding: 8px 14px;
        margin: 6px 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.82rem;
        color: #f5a5a5;
        border-radius: 0 3px 3px 0;
    }}
    .no-anomaly {{
        background: #0d1f15;
        border-left: 3px solid #2ecc71;
        padding: 8px 14px;
        margin: 6px 0;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.82rem;
        color: #7de8a0;
        border-radius: 0 3px 3px 0;
    }}

    /* Crack card */
    .crack-card {{
        background: #161a23;
        border: 1px solid #2a2e3a;
        border-radius: 4px;
        padding: 16px 20px;
    }}

    /* Dividers */
    hr {{ border-color: #2a2e3a !important; }}

    /* Button */
    .stButton > button {{
        background: #1a4f8a;
        color: #e8ecf4;
        border: 1px solid #2a6fca;
        border-radius: 3px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.9rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 10px 28px;
        width: 100%;
        transition: background 0.2s;
    }}
    .stButton > button:hover {{
        background: #2a6fca;
        border-color: #5090e0;
    }}

    /* Chart area */
    [data-testid="stArrowVegaLiteChart"] {{
        background: #161a23 !important;
    }}

    /* Section title accent */
    .section-title {{
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.70rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #4a6080;
        margin-bottom: 10px;
        margin-top: 24px;
        border-bottom: 1px solid #2a2e3a;
        padding-bottom: 6px;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

STATUS_COLOR = {
    "Healthy": "#2ecc71",
    "Warning": "#f1c40f",
    "Critical": "#e67e22",
    "Failure": "#e74c3c",
}

BADGE_CLASS = {
    "Healthy": "badge-healthy",
    "Warning": "badge-warning",
    "Critical": "badge-critical",
    "Failure": "badge-failure",
}

CRACK_RISK_COLOR = {
    "LOW": "#2ecc71",
    "MONITOR": "#f1c40f",
    "MODERATE": "#e67e22",
    "HIGH": "#e74c3c",
}


@st.cache_data(ttl=0)
def fetch_asset_list():
    try:
        r = requests.get(f"{API_BASE}/assets", timeout=5)
        return r.json()
    except Exception:
        return [
            {"asset_id": "INF-001", "bridge_name": "Millbrook Crossing"},
            {"asset_id": "INF-002", "bridge_name": "Northgate Viaduct"},
            {"asset_id": "INF-003", "bridge_name": "Riverside Steel Arch"},
            {"asset_id": "INF-004", "bridge_name": "Eastside Overpass"},
        ]


def fetch_asset_report(asset_id: str) -> dict:
    r = requests.get(f"{API_BASE}/simulate-asset", params={"asset_id": asset_id}, timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_sensor_data(asset_id: str) -> dict:
    r = requests.get(
        f"{API_BASE}/sensor-data",
        params={"asset_id": asset_id, "n": 200},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()


def score_color(score: float) -> str:
    if score >= 80:
        return "#2ecc71"
    elif score >= 60:
        return "#f1c40f"
    elif score >= 40:
        return "#e67e22"
    return "#e74c3c"


def render_gauge(score: float, label: str = "HEALTH SCORE"):
    """Render a lightweight SVG gauge."""
    color = score_color(score)
    pct = score / 100.0
    # Arc math (stroke-dasharray trick on a circle r=40, circ≈251)
    circ = 251.3
    dash = pct * circ
    st.markdown(
        f"""
        <div style="text-align:center; padding: 10px 0;">
            <svg width="140" height="140" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" fill="none" stroke="#2a2e3a" stroke-width="10"/>
                <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="10"
                    stroke-dasharray="{dash:.1f} {circ:.1f}"
                    stroke-dashoffset="{circ * 0.25:.1f}"
                    stroke-linecap="round"/>
                <text x="50" y="46" text-anchor="middle"
                    font-family="Share Tech Mono, monospace"
                    font-size="17" fill="{color}" font-weight="bold">{score:.1f}</text>
                <text x="50" y="60" text-anchor="middle"
                    font-family="Barlow, sans-serif"
                    font-size="7" fill="#6b7280" letter-spacing="1">{label}</text>
            </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🏗️ INFRA·HEALTH")
    st.markdown('<div class="section-title">Asset Selector</div>', unsafe_allow_html=True)

    assets = fetch_asset_list()
    asset_options = {f"{a['asset_id']} — {a['bridge_name']}": a["asset_id"] for a in assets}
    selected_label = st.selectbox("Select Asset", list(asset_options.keys()), label_visibility="collapsed", key="asset_selector")
    selected_asset_id = asset_options[selected_label]

    # image uploader for crack analysis
    st.markdown("### 📤 Crack Image Analysis")
    uploaded_image = st.file_uploader(
        "Upload crack image",
        type=["jpg", "jpeg", "png"],
        key="crack_upload"
    )

    st.markdown("")
    simulate_btn = st.button("⟳  SIMULATE NEW CONDITION")

    st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)
    st.markdown(
        "<small style='color:#4a6080'>Urban Infrastructure Health & Anomaly Analysis System v1.0 — "
        "Real-time physics-aware health evaluation for bridge assets using "
        "crack detection, vibration Z-scores, stress thresholds, and temperature trend analysis.</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────

if "report" not in st.session_state or simulate_btn or st.session_state.get("last_asset") != selected_asset_id:
    st.session_state["last_asset"] = selected_asset_id
    if uploaded_image is not None:
        with st.spinner("Running CNN crack analysis..."):
            files = {
                "image": (
                    uploaded_image.name,
                    uploaded_image.getvalue(),
                    uploaded_image.type,
                )
            }
            response = requests.post(
                f"{API_BASE}/analyze-full-health",
                files=files,
                data={"asset_id": selected_asset_id},
            )
            st.session_state["report"] = response.json()
    else:
        with st.spinner("⚙️ Running health evaluation pipeline..."):
            try:
                response = requests.get(
                    f"{API_BASE}/simulate-asset",
                    params={"asset_id": selected_asset_id},
                )
                st.session_state["report"] = response.json()
                st.session_state["sensor"] = fetch_sensor_data(selected_asset_id)
                st.session_state["error"] = None
            except Exception as e:
                st.session_state["error"] = str(e)

report = st.session_state.get("report")
sensor = st.session_state.get("sensor")
error = st.session_state.get("error")

# ─────────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────────

st.markdown(
    "<h1 style='font-size:1.8rem; margin-bottom:2px;'>Urban Infrastructure Health Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color:#4a6080; font-size:0.85rem; margin-top:0; font-family:Share Tech Mono,monospace;'>"
    "ANOMALY DETECTION · STRUCTURAL HEALTH MONITORING · PREDICTIVE MAINTENANCE</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

if error:
    st.error(f"❌ Could not connect to backend API ({API_BASE}). Start the FastAPI server with:\n\n"
             "`uvicorn main:app --reload` from the `/backend` directory.")
    st.stop()

if not report:
    st.info("Loading data…")
    st.stop()

# ── TOP ROW: Gauge + Status + Key Metrics ──────────────────────────────────

col_gauge, col_status, col_m1, col_m2, col_m3, col_m4 = st.columns([1.4, 1.4, 1, 1, 1, 1])

with col_gauge:
    render_gauge(report["HealthScore"])

with col_status:
    st.markdown('<div class="section-title">Asset Info</div>', unsafe_allow_html=True)
    status = report["Status"]
    badge_cls = BADGE_CLASS.get(status, "badge-critical")
    st.markdown(
        f'<span class="status-badge {badge_cls}">{status}</span>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**{report.get('BridgeName', report['AssetID'])}**")
    st.markdown(
        f"<small style='color:#4a6080;font-family:Share Tech Mono,monospace'>"
        f"{report['AssetID']} · {report.get('Material','—')} · "
        f"Built {report.get('ConstructionYear','—')} · "
        f"{report.get('SpanLengthMeters','—')} m span</small>",
        unsafe_allow_html=True,
    )

sb = report.get("ScoreBreakdown", {})
with col_m1:
    st.metric("🔍 Crack Score", f"{sb.get('raw_crack_score', 0):.1f}")
with col_m2:
    st.metric("📳 Vibration", f"{sb.get('raw_vibration_score', 0):.1f}")
with col_m3:
    st.metric("⚖️ Stress", f"{sb.get('raw_stress_score', 0):.1f}")
with col_m4:
    st.metric("🌡️ Temperature", f"{sb.get('raw_temperature_score', 0):.1f}")

st.markdown("---")

# ── SECOND ROW: Crack Analysis + Score Breakdown ───────────────────────────

col_crack, col_breakdown = st.columns([1, 1])

with col_crack:
    st.markdown('<div class="section-title">Crack Analysis · CNN Visual Inspection</div>', unsafe_allow_html=True)
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
    ca = report.get("CrackAnalysis", {})
    risk_label = ca.get("crack_risk_label", "LOW")
    risk_color = CRACK_RISK_COLOR.get(risk_label, "#888")
    crack_confirmed = ca.get("crack_confirmed", False)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"<div class='crack-card'>"
            f"<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#4a6080;letter-spacing:2px'>CRACK DETECTED</div>"
            f"<div style='font-size:1.6rem;font-weight:900;color:{'#e74c3c' if crack_confirmed else '#2ecc71'}'>"
            f"{'YES' if crack_confirmed else 'NO'}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"<div class='crack-card'>"
            f"<div style='font-family:Share Tech Mono,monospace;font-size:0.7rem;color:#4a6080;letter-spacing:2px'>RISK LABEL</div>"
            f"<div style='font-size:1.6rem;font-weight:900;color:{risk_color}'>{risk_label}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("")
    d1, d2, d3 = st.columns(3)
    with d1:
        st.metric("Length (mm)", f"{ca.get('crack_length', 0):.2f}")
    with d2:
        st.metric("Orientation (°)", f"{ca.get('crack_orientation', 0):.1f}")
    with d3:
        st.metric("CNN Confidence", f"{ca.get('cnn_confidence', 0):.1%}")


with col_breakdown:
    st.markdown('<div class="section-title">Score Contribution Breakdown</div>', unsafe_allow_html=True)
    breakdown_data = {
        "Component": ["Crack (40%)", "Vibration (30%)", "Stress (20%)", "Temp (10%)"],
        "Raw Score": [
            sb.get("raw_crack_score", 0),
            sb.get("raw_vibration_score", 0),
            sb.get("raw_stress_score", 0),
            sb.get("raw_temperature_score", 0),
        ],
        "Weighted": [
            sb.get("crack_contribution", 0),
            sb.get("vibration_contribution", 0),
            sb.get("stress_contribution", 0),
            sb.get("temperature_contribution", 0),
        ],
    }
    df_breakdown = pd.DataFrame(breakdown_data)

    for _, row in df_breakdown.iterrows():
        raw = row["Raw Score"]
        color = score_color(raw)
        pct_bar = int(raw)
        st.markdown(
            f"<div style='margin:8px 0;'>"
            f"<div style='display:flex;justify-content:space-between;margin-bottom:3px;'>"
            f"<span style='font-family:Share Tech Mono,monospace;font-size:0.78rem;color:#9098a8'>{row['Component']}</span>"
            f"<span style='font-family:Share Tech Mono,monospace;font-size:0.78rem;color:{color}'>{raw:.1f} → {row['Weighted']:.1f} pts</span>"
            f"</div>"
            f"<div style='background:#2a2e3a;border-radius:2px;height:6px;'>"
            f"<div style='background:{color};width:{pct_bar}%;height:6px;border-radius:2px;'></div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── SENSOR TIME-SERIES CHARTS ──────────────────────────────────────────────

st.markdown('<div class="section-title">Sensor Time-Series — Live Data Stream</div>', unsafe_allow_html=True)

if sensor and "data" in sensor:
    df_sensor = pd.DataFrame(sensor["data"])
    df_sensor["timestamp"] = pd.to_datetime(df_sensor["timestamp"])
    df_sensor = df_sensor.set_index("timestamp")

    ch1, ch2, ch3 = st.columns(3)
    with ch1:
        st.markdown("**📳 Vibration** (mm/s)")
        st.line_chart(
            df_sensor[["vibration_mm_s"]],
            color=["#3b82f6"],
            height=180,
        )
    with ch2:
        st.markdown("**⚖️ Stress Load** (%)")
        st.line_chart(
            df_sensor[["stress_pct"]],
            color=["#f59e0b"],
            height=180,
        )
    with ch3:
        st.markdown("**🌡️ Temperature** (°C)")
        st.line_chart(
            df_sensor[["temperature_c"]],
            color=["#ef4444"],
            height=180,
        )
else:
    st.warning("Sensor data unavailable.")

st.markdown("---")

# ── ANOMALY LOG ────────────────────────────────────────────────────────────

st.markdown('<div class="section-title">Anomaly Log</div>', unsafe_allow_html=True)

anomalies = report.get("Anomalies", [])
if anomalies:
    st.markdown(
        f"<p style='font-family:Share Tech Mono,monospace;font-size:0.78rem;color:#e74c3c;'>"
        f"⚠ {len(anomalies)} ANOMAL{'Y' if len(anomalies)==1 else 'IES'} DETECTED</p>",
        unsafe_allow_html=True,
    )
    for msg in anomalies:
        st.markdown(f"<div class='anomaly-item'>⚡ {msg}</div>", unsafe_allow_html=True)
else:
    st.markdown(
        "<div class='no-anomaly'>✔ No anomalies detected — all sensor readings within nominal parameters.</div>",
        unsafe_allow_html=True,
    )

# ── FOOTER ─────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#2a2e3a;font-family:Share Tech Mono,monospace;font-size:0.7rem;'>"
    "URBAN INFRASTRUCTURE HEALTH & ANOMALY ANALYSIS SYSTEM · EVALUATION ENGINE v1.0</p>",
    unsafe_allow_html=True,
)
