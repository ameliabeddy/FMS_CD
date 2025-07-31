import streamlit as st
import pandas as pd

# Load data
products = pd.read_csv("Data/products.csv")
st.title("Products by Supplier")

suppliers_list = sorted(products["Supplier"].unique())
selected_supplier = st.selectbox("Select a supplier", suppliers_list)
filtered = products[products["Supplier"] == selected_supplier]

for _, row in filtered.iterrows():
    st.markdown(f"<a name='Product-{row['Product Name'].replace(' ', '_')}'></a>", unsafe_allow_html=True)
    with st.expander(row["Product Name"]):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Category:** {row['Category']}")
            st.markdown(f"**Material:** {row['Material']}")
            st.markdown(f"**Weight:** {row['Weight']} kg")
            st.markdown(f"**Specification:** {row['Spec']}")
        


        with col2:
            has_carbon = str(row["Carbon data available"]).strip().lower() == "yes"
            st.markdown(f"**Carbon Data Available:** {'✅' if has_carbon else '❌'}")

            if has_carbon and pd.notna(row["Carbon Footprint"]):
                st.metric(label="Carbon Footprint (kg CO₂e)", value=row["Carbon Footprint"])
            
        st.markdown(f"More Product Data:")
        st.markdown(f"- **Biggest Contribution:** {row['Biggest contribution']}")
        st.markdown(f"- **Recycled Material Used:** {row['Recycled Material Used']}%")
        st.markdown(f"- **Recyclability:** {row['Recyclablility']}%")
        st.markdown(f"- **Notes:** {row['Notes']}")
