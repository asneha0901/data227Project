import altair as alt
import pandas as pd
import geopandas as gpd
from utils.io import chicago_wards_df, cats_sorted, costs_wide, costs_lon_nostreets, points_df2


cat_radio = alt.binding_radio(options=cats_sorted, name="Category: ")
cat_sel = alt.param(name="cat_sel", value=cats_sorted[0], bind=cat_radio)

chicago_wards = alt.topo_feature(
"https://raw.githubusercontent.com/asneha0901/data227_content/refs/heads/main/chicago-ward-boundaries.topojson",
feature="data"
)
spend_by_type = (
    alt.Chart(chicago_wards)
    .mark_geoshape(stroke="#D9D6CD")
    .project(type="mercator")
    .add_params(cat_sel)
    .transform_lookup(
        lookup="ward",
        from_=alt.LookupData(
            costs_wide,
            key="ward",
            fields=list(cats_sorted)  
        )
    )
    .transform_calculate(selected_cost="datum[cat_sel] || 0")
    .encode(
        color=alt.Color("selected_cost:Q", scale=alt.Scale(scheme="warmgreys"), title="Total cost").legend(
            orient="bottom", title='TOTAL COST', padding=50),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("selected_cost:Q", title="Total cost", format=",")
        ],
    ).properties(height=500, width=450)
)

brush = alt.selection_point(fields=['neighborhoods'], bind='legend')
basemap=alt.Chart(
    chicago_wards, title='Most Popular Property Type by Ward'
).mark_geoshape(  
    stroke='#706545', fill="white"
).encode(
    opacity=alt.value(0.3),
).project(
    type='mercator'
)
points = alt.Chart(points_df2).mark_circle().encode(
    longitude="long:Q",
    latitude="latt:Q",
    color=alt.Color('neighborhoods:N',scale=alt.Scale(scheme="dark2")).legend(
            orient="left", title='neighborhoods ', padding=40),
    opacity=alt.condition(brush, alt.value(1), alt.value(0.05)),
    tooltip=["ward:N"]
).add_params(
    brush
)
bar_chart1 = alt.Chart(points_df2).mark_bar().encode(
    x=alt.X('category:N', title='Property Type'),
    y=alt.Y('mean(cost):Q', title='Average Spent', scale=alt.Scale(domain=[0,1000000])),
    color=alt.Color('category:N', legend=None),
    tooltip=['category:N', 'mean(cost):Q']
).transform_filter(
    brush 
).properties(
    width=400,
    height=400,
    title='Menu-Money Spent By Category (per Side) (static scale)'
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
    title='Menu-Money Spent By Category (per Side) (refactored scale)'
)
map_view = (spend_by_type + points).project(type="mercator")

barchartcost=(map_view | (bar_chart1))
