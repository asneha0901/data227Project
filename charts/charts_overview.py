import altair as alt
import pandas as pd
from utils.io import chicago_wards_df, cats_sorted, costs_wide, costs_lon_nostreets, points_df2


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

brush = alt.selection_interval(encodings=["longitude", "latitude"])
basemap=alt.Chart(
    chicago_wards, title='Most Popular Property Type by Ward'
).mark_geoshape(  
    stroke='#706545', fill="white"
).encode(
    opacity=alt.value(0.3),
).project(
    type='mercator'
)
points = alt.Chart(points_df2).mark_circle(opacity=0.35, color="black").encode(
    longitude="long:Q",
    latitude="latt:Q",
    color=alt.condition(brush, alt.value("red"), alt.value("black")),
    opacity=alt.condition(brush, alt.value(0.9), alt.value(0.15)),
    tooltip=["ward:N"]
).add_params(
    brush
)
bar_chart1 = alt.Chart(points_df2).mark_bar().encode(
    x=alt.X('category:N', title='Property Type'),
    y=alt.Y('sum(cost):Q', title='Total Spent', scale=alt.Scale(domain=[0,22000000])),
    color=alt.Color('category:N', legend=None),
    tooltip=['category:N', 'sum(cost):Q']
).transform_filter(
    brush 
).properties(
    width=360,
    height=300,
    title='Sales by Property Type in Selected Wards (static scale)'
)
bar_chart2 = alt.Chart(points_df2).mark_bar().encode(
    x=alt.X('category:N', title='Property Type'),
    y=alt.Y('sum(cost):Q', title='Total Spent'),
    color=alt.Color('category:N', legend=None),
    tooltip=['category:N', 'sum(cost):Q']
).transform_filter(
    brush 
).properties(
    width=360,
    height=300,
    title='Sales by Property Type in Selected Wards (refactored scale)'
)
map_view = (spend_by_type + points).project(type="mercator")

barchartcost=(map_view | bar_chart1 | bar_chart2)
