import altair as alt
import pandas as pd
import geopandas as gpd
import numpy as np
from utils.io import chicago_wards_df, cats_sorted, costs_wide, costs_lon_nostreets, points_df2


cat_radio = alt.binding_radio(options=cats_sorted, name="Category: ")
cat_sel = alt.param(name="cat_sel", value=cats_sorted[0], bind=cat_radio)
cats_sorted2 = np.append(cats_sorted, 'neighborhoods')
chicago_wards = alt.topo_feature(
"https://raw.githubusercontent.com/asneha0901/data227_content/refs/heads/main/chicago-ward-boundaries.topojson",
feature="data"
)

brush = alt.selection_point(fields=['neighborhoods'], bind='legend')
spend_by_type = (
    alt.Chart(chicago_wards)
    .mark_geoshape(strokeWidth=2.3)
    .project(type="mercator")
    .add_params(cat_sel)
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            costs_wide,
            key="ward",
            fields=list(cats_sorted2)
        )
    )
    .transform_calculate(selected_cost="datum[cat_sel] || 0")
    .encode(
        color=alt.Color("selected_cost:Q", scale=alt.Scale(scheme="warmgreys"), title="Total cost").legend(
            orient="bottom", title='TOTAL COST', padding=50),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("selected_cost:Q", title="Total cost", format=",")
        ],
        stroke=alt.Stroke('neighborhoods:N', scale=alt.Scale(scheme='dark2')).legend(
            orient="left", title='neighborhoods ', padding=40),
        strokeOpacity=alt.condition(brush, alt.value(1), alt.value(0.1)),
    ).properties(height=500, width=450)
).add_params(
    brush
)


points = alt.Chart(points_df2).mark_circle().encode(
    longitude="long:Q",
    latitude="latt:Q",
    color=alt.Color('neighborhoods:N',scale=alt.Scale(scheme="dark2"), legend=None),
    opacity=alt.condition(brush, alt.value(1), alt.value(0.05)),
    tooltip=["ward:N"]
).add_params(
    brush
)
bar_chart1 = alt.Chart(points_df2).mark_bar().encode(
    x=alt.X('category:N', title='Spending Category'),
    y=alt.Y('mean(cost):Q', title='Average Spent by Chicago Side', scale=alt.Scale(domain=[0,1000000])),
    color=alt.Color('category:N', legend=None, scale=alt.Scale(scheme='accent')),
    tooltip=[alt.Tooltip("category:N", title="Category"), alt.Tooltip("mean(cost):Q", title="Mean of Amount Spent")]
).transform_filter(
    brush 
).properties(
    width=400,
    height=400,
    title='Menu-Money Spent By Category (static scale)'
)
bar_chart2 = alt.Chart(points_df2).mark_bar().encode(
    x=alt.X('category:N', title='Property Type'),
    y=alt.Y('mean(cost):Q', title='Average Spent'),
    color=alt.Color('category:N', legend=None),
    tooltip=['category:N', 'mean(cost):Q']
).transform_filter(
    brush 
).properties(
    width=300,
    height=300,
    title='Menu-Money Spent By Category (refactored scale)'
)
map_view = (spend_by_type).project(type="mercator")

barchartcost=(map_view | (bar_chart1))
