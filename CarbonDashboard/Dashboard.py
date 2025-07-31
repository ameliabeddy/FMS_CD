import streamlit as st
import pandas as pd

commitments = pd.read_csv("Data/commitments.csv")


st.set_page_config(page_title="CarbonDashboard", layout="wide")
st.image("assets/FMSlogo.png", width=150)
st.markdown("Welcome to FMS's Sustainability Dashboard")
st.markdown("Use the sidebar to navigate between our suppliers and their sustainability objectives as well as a selection of products")


st.title("FMS Interiors Sustainability Commitments")
st.markdown(
    "Our mission is to help you reduce your organisation’s carbon footprint "
    "by specifying durable, low-impact furniture and applying a repair, reuse, and recycle approach."
)

# Slide-style layout for each commitment
for _, row in commitments.iterrows():
    with st.container():
        st.markdown("---")  # Horizontal line to separate slides

        st.markdown(f"### {row['Title']}")
        st.markdown(f"**Category:** {row['Category']}")
        if pd.notna(row['Description']):
            if ',' in row['Description']:
                bullet_points = [item.strip() for item in row['Description'].split(',')]
                for point in bullet_points:
                    st.markdown(f"- {point}")
            else:
                st.markdown(row['Description'])
        st.markdown(" ")  # Spacer between slides
