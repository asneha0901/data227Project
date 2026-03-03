import streamlit as st
import altair as alt
from utils.io import chicago_wards_df, cats_sorted, costs_wide

st.set_page_config(page_title="Story", layout="wide")

cat_radio = alt.binding_radio(options=cats_sorted, name="Category: ")
cat_sel = alt.param(name="cat_sel", value=cats_sorted[0], bind=cat_radio)



chicago_wards = alt.topo_feature(
"https://raw.githubusercontent.com/asneha0901/data227_content/refs/heads/main/chicago-ward-boundaries.topojson",
feature="data"
)

chicago_projection = alt.Chart(
    chicago_wards, 
    title="Albers Projection (map looks ok)"
).mark_geoshape(
    fill='#d3d3d3', # '#2a1d0c', 
    stroke='#706545',  # Optional: Outline color
    strokeWidth=0.75    # Optional: Outline width
).project(
    type='mercator'
).encode(tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward")
        ]
) 

joint_chart = (
    alt.Chart(chicago_wards, title="Expenditure by Ward (select category)")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .add_params(cat_sel)
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            costs_wide,
            key="ward",
            fields=list(cats_sorted)  
        )
    )
    .transform_calculate(selected_cost="datum[cat_sel] || 0")
    .encode(
        color=alt.Color("selected_cost:Q", scale=alt.Scale(scheme="greens"), title="Total cost"),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("selected_cost:Q", title="Total cost", format=",")
        ],
    )
)


st.title("Overview of Chicago Menu-Money Spending Patterns")
st.markdown("**Central question:** *How do different wards allocate their Chicago Menu-Money Over the Years*")

st.header("Chicago Menu-Money Spending by Category")
st.write("To begin with let us see which each type of category is prioritized in different wards.")
st.altair_chart(joint_chart)
st.caption("Takeaway:")

st.write("Geo ward dtype:", chicago_wards_df["ward"].dtype)
st.write("Costs ward dtype:", costs_wide["ward"].dtype)
st.write("Example categories:", cats_sorted[:5])
st.write("Costs_wide columns include first category?", cats_sorted[0] in costs_wide.columns)