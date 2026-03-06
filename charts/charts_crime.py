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
    alt.Chart(chicago_wards, title="Money Spent on Cameras / Crime / Person")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            yr2021sec,
            key="ward",
            fields=['spent per crime per person'] 
        )).encode(
        color=alt.Color("spent per crime per person:Q", scale=alt.Scale(scheme="greens"), title="Money on Cameras Per Crime Per Person", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("spent per crime per person:Q", title="Money on cameras per crime per person", format=",")
        ],
    ).properties(width=270)
)
crimetot = (
    alt.Chart(chicago_wards, title="Total Public Crimes by Ward in 2021")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            crime21,
            key="ward",
            fields=['Year'] 
        )).encode(
        color=alt.Color("Year:Q", scale=alt.Scale(scheme="blues"), title="Total Public Crimes in 2021", legend=alt.Legend(orient="bottom")),
        tooltip=[
            alt.Tooltip("ward:O", title="Ward"),
            alt.Tooltip("Year:Q", title="Rate of crimes", format=",")
        ],
    )
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
spatial=(race_dist | crimeperk | crimetot).resolve_scale(color="independent")

crimefullchart=(timeline & spatial)