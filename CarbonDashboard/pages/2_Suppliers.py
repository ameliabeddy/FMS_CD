import streamlit as st
import pandas as pd

# Load CSV with correct encoding
df = pd.read_csv("Data/suppliers.csv", encoding='unicode_escape')

st.title("Supplier Sustainability Overview")

st.markdown("""
<div style="display: flex; gap: 20px; flex-wrap: wrap;">

  <div style="flex: 1; min-width: 250px; background-color: #e6f2ff; padding: 15px; border-radius: 8px;">
    <h4>Governance</h4>
      <p>Company level policies, certifications & frameworks demonstrating accountability and transparency such as ISO 14001, B Corp, ESG strategies</p>
  </div>

  <div style="flex: 1; min-width: 250px; background-color: #e6f2ff; padding: 15px; border-radius: 8px;">
    <h4>Materials</h4>
      <p>Certifications or properties of materials used, like FSC for wood or ISO 14001 for steel production, and recyclability/recycled content.</p>
  </div>

  <div style="flex: 1; min-width: 250px; background-color: #e6f2ff; padding: 15px; border-radius: 8px;">
    <h4>Operations</h4>
      <p>Factory processes that show sustainable practice — including Scope 1 & 2 emissions, net zero pledges, and zero waste operations.</p>
  </div>

  <div style="flex: 1; min-width: 250px; background-color: #e6f2ff; padding: 15px; border-radius: 8px;">
    <h4>Initiatives</h4>
      <p>Projects or goals that go beyond compliance, like tree planting, removing plastic waste, ethical sourcing, or circular economy principles</p>
  </div>

</div>
""", unsafe_allow_html=True)



view = st.radio("Select View", ["By Supplier", "By Category"])

# Turn string into bullet points
def bullet_list(text):
    if pd.isna(text) or not text.strip():
        return ["Not stated"]
    return [f"- {item.strip()}" for item in text.split(',') if item.strip()]

# Rating classification by bullet point count
def get_rating_and_color(score):
    if score <= 7:
        return "Poor", "#FFCDD2"   # Light red
    elif score <= 13:
        return "OK", "#FFF9C4"     # Light yellow
    elif score <= 18:
        return "Great", "#C8E6C9"  # Light green
    else:
        return "Incredible", "#B3E5FC"  # Light blue

# Rating box display
def display_rating(score):
    label, color = get_rating_and_color(score)
    st.markdown(
        f"<div style='background-color:{color};padding:10px;border-radius:5px;text-align:center;font-weight:bold'>"
        f"Sustainability Rating: {label} ",
        unsafe_allow_html=True
    )

if view == "By Supplier":
    supplier = st.selectbox("Choose a Supplier", df["Company"].dropna().unique())
    row = df[df["Company"] == supplier].iloc[0]

    # Title and website button
    col_title, col_button = st.columns([4, 1])
    with col_title:
        st.subheader(supplier)

    with col_button:
        if pd.notna(row['Website']) and row['Website'].strip():
            st.markdown(
                f"<a href='{row['Website']}' target='_blank'>"
                f"<button style='padding:6px 12px; background-color:#1f77b4; color:white; border:none; border-radius:4px;'>Website</button>"
                f"</a>",
                unsafe_allow_html=True
            )

    # Category content
    col1, col2 = st.columns(2)
    cols = ["Governance", "Materials", "Operations", "Initiatives"]
    total_points = 0

    for i, col_name in enumerate(cols):
        with col1 if i % 2 == 0 else col2:
            items = bullet_list(row[col_name])
            st.markdown(f"### {col_name}")
            for item in items:
                st.markdown(item)
            total_points += len(items)

    display_rating(total_points)

    

elif view == "By Category":
    category = st.selectbox("Choose a Category", ["Governance", "Materials", "Operations", "Initiatives"])

    for i in df[df["Company"].notna()].index:
        company = str(df.loc[i, "Company"])
        items = bullet_list(df.loc[i, category])

        with st.expander(company):
            for item in items:
                st.markdown(item)

            # Calculate total bullet points across all categories
            total_points = (
                len(bullet_list(df.loc[i, "Governance"])) +
                len(bullet_list(df.loc[i, "Materials"])) +
                len(bullet_list(df.loc[i, "Operations"])) +
                len(bullet_list(df.loc[i, "Initiatives"]))
            )
            display_rating(total_points)

