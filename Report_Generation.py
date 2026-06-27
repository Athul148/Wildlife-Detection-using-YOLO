import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime


# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Wildlife Reports",
    page_icon="📄",
    layout="wide"
)


# ==========================================
# THEME (SAME AS APP.PY)
# ==========================================
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: white;
}

/* HERO */
.hero {
    padding: 60px 40px;
    text-align: center;
}

.hero-title {
    font-size: 52px;
    font-weight: 900;
    background: linear-gradient(90deg, #10b981, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 18px;
    color: #cbd5e1;
    max-width: 700px;
    margin: auto;
    margin-top: 15px;
}

/* SECTION */
.section-title {
    font-size: 22px;
    font-weight: 700;
    margin: 35px 0 15px 0;
    color: #e2e8f0;
}

/* REPORT CARDS */
.report-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

.report-card h2 {
    color: #10b981;
    margin: 0;
}

.report-card p {
    color: #94a3b8;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HERO SECTION
# ==========================================
st.markdown("""
<div class="hero">

<div class="hero-title">
Wildlife Report Center
</div>

<div class="hero-subtitle">
Generate wildlife monitoring reports, species statistics,
activity scores, and ecological insights from AI detection records.
</div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# DATABASE CONNECTION
# ==========================================
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Athul5555@",
        database="wildguard_ai"
    )


try:

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM detection_results1")
    detection_rows = cursor.fetchall()

    cursor.execute("SELECT * FROM species_results")
    species_rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not detection_rows:

        st.warning("No report data available.")
        st.stop()

    df = pd.DataFrame(detection_rows)
    species_df = pd.DataFrame(species_rows)


    # ==========================================
    # ACTIVITY & RARE SPECIES REPORT
    # ==========================================
    st.markdown(
        '<div class="section-title">Activity & Rare Species Report</div>',
        unsafe_allow_html=True
    )

    avg_activity = round(df["risk_score"].mean(), 2)
    max_activity = df["risk_score"].max()

    rare_events = int(df["rare_found"].sum())

    rare_percentage = round(
        (rare_events / len(df)) * 100,
        2
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="report-card">
            <h2>{avg_activity}%</h2>
            <p>Average Activity Score</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="report-card">
            <h2>{max_activity}%</h2>
            <p>Maximum Activity Score</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="report-card">
            <h2>{rare_events}</h2>
            <p>Rare Species Events</p>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="report-card">
            <h2>{rare_percentage}%</h2>
            <p>Rare Detection Rate</p>
        </div>
        """, unsafe_allow_html=True)


    # ==========================================
    # SPECIES STATISTICS
    # ==========================================
    st.markdown(
        '<div class="section-title">Species Statistics</div>',
        unsafe_allow_html=True
    )

    if not species_df.empty:

        species_summary = (
            species_df
            .groupby("species_name")["count"]
            .sum()
            .reset_index()
            .sort_values(by="count", ascending=False)
        )

        st.dataframe(
            species_summary,
            use_container_width=True,
            hide_index=True
        )

    else:

        species_summary = pd.DataFrame()

        st.info("No species statistics available.")


    # ==========================================
    # DOWNLOAD REPORT
    # ==========================================
    st.markdown(
        '<div class="section-title">Download Report</div>',
        unsafe_allow_html=True
    )

    report_date = datetime.now().strftime("%Y-%m-%d")

    report_summary = pd.DataFrame({
        "Metric": [
            "Average Activity Score",
            "Maximum Activity Score",
            "Rare Species Events",
            "Rare Detection Rate (%)"
        ],
        "Value": [
            avg_activity,
            max_activity,
            rare_events,
            rare_percentage
        ]
    })

    csv_data = (
        "=== Wildlife Report Summary ===\n"
        + report_summary.to_csv(index=False)
        + "\n\n=== Species Statistics ===\n"
        + species_summary.to_csv(index=False)
    )

    st.download_button(
        label="📥 Download Full Wildlife Report (CSV)",
        data=csv_data,
        file_name=f"wildlife_report_{report_date}.csv",
        mime="text/csv"
    )


except Exception as e:

    st.error(f"Database Error: {e}")
