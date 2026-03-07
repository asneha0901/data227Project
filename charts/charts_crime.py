import altair as alt
import pandas as pd
from utils.io import chicago_wards_df, yr2021sec, secdf, crime21, races3, acs, costs_long_top2, wardlitcrashcount, wardcrashcount

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

brush2 = alt.selection_point(fields=['Most Common Race'], bind='legend')

crimeperk = (
    alt.Chart(chicago_wards, title="Money Spent on Cameras / Crime / Person")
    .mark_geoshape(strokeWidth=2.3)
    .project(type="mercator")
    .add_params(brush2).transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            yr2021sec,
            key="ward",
            fields=['spent per crime per person', 'Most Common Race'] 
        )).encode(
        color=alt.Color("spent per crime per person:Q", scale=alt.Scale(scheme="greens"), title="Money on Cameras Per Crime Per Person", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("spent per crime per person:Q", title="Money on cameras per crime per person", format=",")
        ],
        stroke=alt.Stroke('Most Common Race:N', scale=alt.Scale(scheme='tableau10')).legend(
            orient="right", title='Most Common Race'),
        strokeOpacity=alt.condition(brush2, alt.value(1), alt.value(0.1))
    ).properties(width=270))


crimetot = (
    alt.Chart(chicago_wards, title="Total Public Crimes by Ward in 2021")
    .mark_geoshape(strokeWidth=2.3)
    .project(type="mercator")
    .add_params(brush2).transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            crime21,
            key="ward",
            fields=['Year', 'Most Common Race'] 
        )).encode(
        color=alt.Color("Year:Q", scale=alt.Scale(scheme="greens"), title="Total number of crimes", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("Year:Q", title="Total Number of Crimes", format=",")
        ],
        stroke=alt.Stroke('Most Common Race:N', scale=alt.Scale(scheme='tableau10')).legend(
            orient="right", title='Most Common Race'),
        strokeOpacity=alt.condition(brush2, alt.value(1), alt.value(0.1))
    ).properties(width=270))

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
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("selected_race:Q", title="Proportion", format=",")
        ],
    ).properties(width=270)
)
spatial=(race_dist | crimeperk | crimetot).resolve_scale(color="independent")

crimefullchart=(timeline & spatial)


percentage1=alt.Chart(costs_long_top2, title='Proportion of Menu-Money Spent').mark_bar().encode(
    x=alt.X('average(Percentage spent on Category):Q', scale=alt.Scale(domain=[0,1], clamp=True), title='Proportion of Menu-Money Spent'),
    yOffset="category:N",
    y=alt.Y('neighborhoods:N'),
    color=alt.Color('average(area):Q', scale=alt.Scale(scheme='blues'), legend=alt.Legend(orient='bottom')),
    stroke=alt.Stroke('category', scale=alt.Scale(scheme='accent'), legend=None))
text = percentage1.mark_text(
    align="left",
    baseline="middle",
    dx=2,
).encode(text="category", color=alt.Color('category', scale=alt.Scale(scheme='accent'), legend=None))

percentage=(percentage1 + text).properties(width=550)

areanorm=alt.Chart(costs_long_top2, title='Amount of Money Spent Relative to Ward Area').mark_bar(height=30).encode(
    x=alt.X('average(cost on category by area):Q', title='Average of cost per area of ward'),
    y=alt.Y('neighborhoods:N', title=''),
    color=alt.Color('category:N', scale=alt.Scale(scheme='accent'), title='Category',legend=alt.Legend(orient='bottom'))
).properties(height=300)

crash_chart = (
    alt.Chart(chicago_wards, title="Number of Crashes Due to Road Defects")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            wardcrashcount,
            key="ward",
            fields=['crash per 1k res'] 
        )).encode(
        color=alt.Color("crash per 1k res:Q", scale=alt.Scale(scheme="purples"), title="Number of Crashes / 1k residents", legend=alt.Legend(orient='right', padding=50))
    )
).properties(height=400)

ratiolight_chart = (
    alt.Chart(chicago_wards, title="Number of Crashes Due to Unlit Roads")
    .mark_geoshape(stroke="#706545")
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            wardlitcrashcount,
            key="ward",
            fields=['unlit_to_lit_ratio'] 
        )).encode(
        color=alt.Color("unlit_to_lit_ratio:Q", scale=alt.Scale(scheme="greens"), title="Crash Ratio Relative to Lit Roads", legend=alt.Legend(orient='right', padding=50))
    )
).properties(height=400)

transporttot=(percentage | areanorm).resolve_scale(color='independent') & (crash_chart | ratiolight_chart).resolve_scale(color='independent')
transporttot