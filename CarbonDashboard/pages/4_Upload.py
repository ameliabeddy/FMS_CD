import streamlit as st
import pandas as pd

st.title("Upload New Product Data")

required_cols = [
    "Product Name", "Supplier", "Category (e.g. Chair)", "Material", "Carbon data available",
    "Carbon Footprint", "Biggest contribution", "Recycled Material Used", "Recyclablility",
    "Weight", "Spec (e.g. H110 x W740 x D740)", "Notes"
]

with st.expander("How to format your Product CSV file"):
    st.markdown("""
    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px;">
    <h4 style="color:#00416A;">Your CSV must have exactly these columns (case-sensitive):</h4>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        for col in required_cols[:len(required_cols)//2]:
            st.markdown(f"- {col}")
    with col2:
        for col in required_cols[len(required_cols)//2:]:
            st.markdown(f"- {col}")

    st.markdown("""
    <br><i>Note:</i><br>
    • All columns must be present even if some values are blank.  
    </div>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a PRODUCT CSV file", type="csv")

if uploaded_file is not None:
    try:
        new_data = pd.read_csv(uploaded_file)

        # Check column structure
        if list(new_data.columns) != required_cols:
            st.error("Column names or order do not match the required format.")
            st.markdown("Expected columns: " + ", ".join(required_cols))

        # Check if 'Carbon Footprint' column is numeric
        elif not pd.to_numeric(new_data["Carbon Footprint"], errors="coerce").notna().all():
            st.error("Carbon Footprint' must be numeric (kg CO₂e).")

        else:
            st.success("Format is valid. Preview below:")
            st.dataframe(new_data)

            if st.button("Append to master list"):
                products_master = pd.read_csv("data/products.csv")
                combined = pd.concat([products_master, new_data]).drop_duplicates()
                combined.to_csv("data/products.csv", index=False)
                st.success("Products successfully added to master file.")

    except Exception as e:
        st.error(f"⚠️ Could not read file: {e}")


st.title("Upload New Supplier Data")

required_cols = [
    "Company", "Governance", "Materials", "Operations", "Initiatives", "Website"
]

with st.expander("How to format your Supplier CSV file"):
    st.markdown("""
    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px;">
    <h4 style="color:#00416A;">Your CSV must have exactly these columns (case-sensitive):</h4>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    midpoint = len(required_cols) // 2
    with col1:
        for col in required_cols[:midpoint]:
            st.markdown(f"- {col}")
    with col2:
        for col in required_cols[midpoint:]:
            st.markdown(f"- {col}")

    st.markdown("""
    <br><i>Note:</i><br>
    • All columns must be present, even if some values are blank.  
    • You can include line breaks, commas, or bullet-style content in cells.
    </div>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a SUPPLIER CSV file", type="csv")

if uploaded_file is not None:
    try:
        new_data = pd.read_csv(uploaded_file)

        # Check column structure
        if list(new_data.columns) != required_cols:
            st.error("Column names or order do not match the required format.")
            st.markdown("Expected columns: " + ", ".join(required_cols))


        else:
            st.success("Format is valid. Preview below:")
            st.dataframe(new_data)

            if st.button("Append to supplier list"):
                suppliers_master = pd.read_csv("data/suppliers.csv")
                combined = pd.concat([suppliers_master, new_data]).drop_duplicates()
                combined.to_csv("data/suppliers.csv", index=False)
                st.success("Suppliers successfully added to master file.")

    except Exception as e:
        st.error(f"⚠️ Could not read file: {e}")
