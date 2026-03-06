import altair as alt
import pandas as pd
from utils.io import chicago_wards_df, yr2021sec, secdf, crime21, races3, acs

chicago_wards = alt.topo_feature(
"https://raw.githubusercontent.com/asneha0901/data227_content/refs/heads/main/chicago-ward-boundaries.topojson",
feature="data"
)

seccamchart = (
    alt.Chart(chicago_wards, title="Money spent on security cameras in 2021")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            yr2021sec,
            key="ward",
            fields=['cost'] 
        )).encode(
        color=alt.Color("cost:Q", scale=alt.Scale(scheme="greens"), title="Total Dollars", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("cost:Q", title="Proportion of Race", format=",")
        ],
    ).properties(width=270)
)

base = alt.Chart(secdf, title="Correlation between Public Crimes and Money spent by Wards on Security Cameras").encode(x='Year')
line1 = base.mark_line(color='blue').encode(
    alt.Y('count').axis(title='Number of Public Crimes', titleColor='#5276A7'))
line2 = base.mark_line(color='green').encode(
    alt.Y('cost').axis(title='Amount spent on Security Cameras', titleColor='green'))
timeline=alt.layer(line1, line2).resolve_scale(
    y='independent'
).properties(width=750)

crimeperk = (
    alt.Chart(chicago_wards, title="Public Crimes by Ward in 2021")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            crime21,
            key="ward",
            fields=['Crime per 1k'] 
        )).encode(
        color=alt.Color("Crime per 1k:Q", scale=alt.Scale(scheme="blues"), title="Rate of crimes per 1k residents", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("Crime per 1k:Q", title="Rate of crimes per 1k residents", format=",")
        ],
    ).properties(width=270)
)

cat_radio = alt.binding_radio(options=races3, name="Race: ")
cat_sel = alt.param(name="cat_sel", value=races3[0], bind=cat_radio)
race_dist = (
    alt.Chart(chicago_wards, title="Proportion of Race By Ward")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .add_params(cat_sel)
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            acs,
            key="Ward",
            fields=races3 
        )
    )
    .transform_calculate(selected_race="datum[cat_sel]")
    .encode(
        color=alt.Color("selected_race:Q", scale=alt.Scale(scheme="purples"), title="Proportion of Race", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("Ward:O", title="Ward"),
            alt.Tooltip("selected_race:Q", title="Proportion", format=",")
        ],
    ).properties(width=270)
)
spatial=(seccamchart | crimeperk | race_dist).resolve_scale(color="independent")

crimefullchart=(timeline & spatial)