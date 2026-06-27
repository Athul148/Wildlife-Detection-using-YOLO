import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="WildGuard AI Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# DARK THEME (SAME AS HOME PAGE)
# ==========================================

st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top, #0b1220, #050814);
    color: white;
}

/* HEADINGS */
.main-title {
    font-size: 42px;
    font-weight: 900;
    background: linear-gradient(90deg, #10b981, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}

.subtitle {
    color: #cbd5e1;
    font-size: 16px;
    margin-bottom: 30px;
}

/* SECTION TITLES */
.section-title {
    font-size: 22px;
    font-weight: 700;
    color: #e2e8f0;
    margin-top: 20px;
}

/* METRIC CARDS */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 15px;
}

/* DATAFRAME */
div[data-testid="stDataFrame"] {
    background: rgba(255,255,255,0.03);
    border-radius: 15px;
    padding: 10px;
}

/* PLOTLY CHART CONTAINER */
div[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 15px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
 WildGuard AI Analytics
</div>

<div class="subtitle">
Wildlife Monitoring & Detection Analytics
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
        st.warning("No analytics data available.")
        st.stop()

    df = pd.DataFrame(detection_rows)
    species_df = pd.DataFrame(species_rows)

    # Debug (remove later if needed)
    # st.write(df.columns)
    # st.write(species_df.head())

    # ==========================================
    # KPI CARDS
    # ==========================================

    st.markdown(
    '<div class="section-title">📌 System Overview</div>',
    unsafe_allow_html=True
   )

    total_records = len(df)
    total_animals = df["animal_count"].sum()
    avg_risk = round(df["risk_score"].mean(), 2)
    rare_events = df["rare_found"].sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Analyses", total_records)
    c2.metric("Animals Detected", int(total_animals))
    c3.metric("Rare Species Events", int(rare_events))
    c4.metric("Avg Activity Score", avg_risk)

    st.divider()

    # ==========================================
    # ROW 1
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        
        st.markdown(
       '<div class="section-title">Species Distribution</div>',
        unsafe_allow_html=True
        )

        if not species_df.empty:

            species_chart = (
                species_df.groupby("species_name")["count"]
                .sum()
                .reset_index()
                .sort_values(by="count", ascending=False)
            )

            fig1 = px.bar(
                species_chart,
                x="species_name",
                y="count",
                text="count",
                title="Detected Species"
            )

            st.plotly_chart(fig1, use_container_width=True)

    with col2:

        
        st.markdown(
       '<div class="section-title">Wildlife Activity Levels</div>',
        unsafe_allow_html=True
        )


        low = len(df[df["risk_score"] <= 30])

        medium = len(
            df[
                (df["risk_score"] > 30)
                & (df["risk_score"] <= 70)
            ]
        )

        high = len(df[df["risk_score"] > 70])

        activity_df = pd.DataFrame({
            "Level": [
                "Low Activity",
                "Medium Activity",
                "High Activity"
            ],
            "Count": [
                low,
                medium,
                high
            ]
        })

        fig2 = px.pie(
            activity_df,
            names="Level",
            values="Count",
            hole=0.5,
            title="Wildlife Activity Distribution"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ==========================================
    # ROW 2
    # ==========================================

    col3, col4 = st.columns(2)

    with col3:

       
        st.markdown(
       '<div class="section-title">Risk Score Trends</div>',
        unsafe_allow_html=True
        )
        

        if "created_at" in df.columns:

            fig3 = px.line(
                df,
                x="created_at",
                y="risk_score",
                markers=True,
                title="Risk Trend Over Time"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        else:
            st.info("created_at column not found.")

    with col4:

        
        st.markdown(
       '<div class="section-title">Top Wildlife Speciess</div>',
        unsafe_allow_html=True
        )

        if not species_df.empty:

            top_species = (
                species_df.groupby("species_name")["count"]
                .sum()
                .reset_index()
                .sort_values(
                    by="count",
                    ascending=False
                )
            )

            fig4 = px.bar(
                top_species,
                x="species_name",
                y="count",
                text="count",
                title="Most Detected Species"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

        else:
            st.info("No species data available.")

    # ==========================================
    # ROW 3
    # ==========================================

    
    st.markdown(
       '<div class="section-title"> Rare Species Monitoring</div>',
        unsafe_allow_html=True
        )

    rare_count = len(df[df["rare_found"] == 1])
    normal_count = len(df[df["rare_found"] == 0])

    rare_df = pd.DataFrame({
        "Category": [
            "Rare Species Found",
            "Normal Activity"
        ],
        "Count": [
            rare_count,
            normal_count
        ]
    })

    fig5 = px.pie(
        rare_df,
        names="Category",
        values="Count",
        hole=0.6,
        title="Rare Species Presence"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # ==========================================
    # SPECIES TABLE
    # ==========================================

    st.markdown(
       '<div class="section-title">Species Detection Statistics</div>',
        unsafe_allow_html=True
    )

    if not species_df.empty:

        species_summary = (
            species_df.groupby("species_name")["count"]
            .sum()
            .reset_index()
            .sort_values(
                by="count",
                ascending=False
            )
        )

        st.dataframe(
            species_summary,
            use_container_width=True,
            hide_index=True
        )

except Exception as e:

    st.error(f"Database Error: {e}")