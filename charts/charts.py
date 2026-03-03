import altair as alt
import pandas as pd
from utils.io import chicago_wards_df, cats_sorted, costs_wide


cat_radio = alt.binding_radio(options=cats_sorted, name="Category: ")
cat_sel = alt.param(name="cat_sel", value=cats_sorted[0], bind=cat_radio)

chicago_wards = alt.topo_feature(
"https://raw.githubusercontent.com/asneha0901/data227_content/refs/heads/main/chicago-ward-boundaries.topojson",
feature="data"
)
spend_by_type = (
    alt.Chart(chicago_wards)
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
        color=alt.Color("selected_cost:Q", scale=alt.Scale(scheme="greens"), title="Total cost").legend(
            orient="left", title=' ', padding=50),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("selected_cost:Q", title="Total cost", format=",")
        ],
    )
)