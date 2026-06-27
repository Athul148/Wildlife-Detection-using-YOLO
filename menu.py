import streamlit as st

def show_menu():
    col1,col2,col3,col4,col5,col6 = st.columns(6)

    with col1:
        if st.button("🏠 Home"):
            st.switch_page("app.py")

    with col2:
        if st.button("🌲 Detection"):
            st.switch_page("pages/Detection.py")

    with col3:
        if st.button("🚨 Alerts"):
            st.switch_page("pages/Alert_Center.py")

    with col4:
        if st.button("📊 Analytics"):
            st.switch_page("pages/Analytics.py")

    with col5:
        if st.button("📄 Reports"):
            st.switch_page("pages/Report_Generation.py")

    with col6:
        if st.button("🕒 History"):
            st.switch_page("pages/History.py")