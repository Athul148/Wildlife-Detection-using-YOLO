import streamlit as st

st.set_page_config(
    page_title="WildGuard AI",
    page_icon="🌿",
    layout="wide"
)

# ==========================================
# MODERN PROFESSIONAL DARK THEME
# ==========================================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: white;
}

/* Hide Streamlit Menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* HERO SECTION */
.hero {
    text-align: center;
    padding: 80px 30px 50px 30px;
}

.hero-title {
    font-size: 64px;
    font-weight: 900;
    background: linear-gradient(90deg,#10b981,#3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 22px;
    color: #cbd5e1;
    margin-top: 10px;
    font-weight: 600;
}

.hero-desc {
    max-width: 850px;
    margin: auto;
    margin-top: 20px;
    color: #94a3b8;
    font-size: 17px;
    line-height: 1.8;
}

/* STATUS */
.status {
    margin-top: 30px;
    padding: 14px;
    border-radius: 14px;
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.25);
    color: #a7f3d0;
    font-size: 14px;
}

/* SECTION TITLE */
.section-title {
    font-size: 26px;
    font-weight: 700;
    color: white;
    margin-top: 40px;
    margin-bottom: 20px;
}

/* FEATURE CARDS */
.tile {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 25px;
    min-height: 180px;
    transition: 0.3s;
}

.tile:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(16,185,129,0.4);
}

.tile h3 {
    color: white;
    margin-bottom: 15px;
}

.tile p {
    color: #94a3b8;
    line-height: 1.7;
    font-size: 14px;
}

/* METRICS */
.metric-box {
    text-align: center;
    padding: 20px;
}

.metric-box h2 {
    color: #10b981;
    margin: 0;
    font-size: 36px;
}

.metric-box p {
    color: #94a3b8;
    margin-top: 8px;
}

/* WORKFLOW */
.workflow {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 35px;
    text-align: center;
    font-size: 22px;
    line-height: 2;
    color: #cbd5e1;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================
st.markdown("""
<div class="hero">

<div class="hero-title">
 WildGuard AI
</div>

<div class="hero-subtitle">
Wildlife Monitoring & Detection Analytics
</div>

<div class="hero-desc">
An AI-powered platform for automated wildlife detection,
species monitoring, activity analysis, rare animal identification,
and ecological reporting using deep learning and computer vision technologies.
</div>


""", unsafe_allow_html=True)


# ==========================================
# QUICK HIGHLIGHTS
# ==========================================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="metric-box">
    <h2>8+</h2>
    <p>Supported Species</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-box">
    <h2>YOLO</h2>
    <p>Deep Learning Engine</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-box">
    <h2>MySQL</h2>
    <p>Detection Database</p>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-box">
    <h2>AI</h2>
    <p>Automated Reports</p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# CORE MODULES
# ==========================================
st.markdown(
    '<div class="section-title"> Core Modules</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="tile">
        <h3> Wildlife Detection</h3>
        <p>
        Upload surveillance videos and automatically identify
        wildlife species using deep learning-based object detection.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="tile">
        <h3>Analytics Dashboard</h3>
        <p>
        Visualize species distribution, activity levels,
        historical trends, and ecological statistics.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="tile">
        <h3>Report Generation</h3>
        <p>
        Generate downloadable wildlife monitoring reports
        for ecological research and forest management.
        </p>
    </div>
    """, unsafe_allow_html=True)




# ==========================================
# SYSTEM ARCHITECTURE
# ==========================================
st.markdown(
    '<div class="section-title"> System Architecture</div>',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="tile">
        <h3> YOLO Detection Engine</h3>
        <p>
        Custom-trained object detection model optimized
        for wildlife identification in forest environments.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="tile">
        <h3> MySQL Database</h3>
        <p>
        Detection results, activity scores, and species
        statistics are securely stored for analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="tile">
        <h3> Analytics Engine</h3>
        <p>
        Interactive dashboards provide insights into
        species activity patterns and rare wildlife events.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# SYSTEM WORKFLOW
# ==========================================
st.markdown(
    '<div class="section-title"> System Workflow</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="workflow">

 Upload Wildlife Video

⬇️

 YOLO Detection

⬇️

 Species Identification

⬇️

 Rare Species Alerts

⬇️

 Analytics Dashboard

⬇️

 Automated Report Generation

</div>
""", unsafe_allow_html=True)