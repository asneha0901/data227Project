import altair as alt
import pandas as pd
from utils.io import chicago_wards_df,costs_wide, yr2021sec, secdf, crime21, races3, acs, costs_long_top2, wardlitcrashcount, wardcrashcount, acsinc, school_by_ward_ambition, school_by_ward_fam, school_by_ward_safety, school_by_ward_support, color_scale

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

secbase = alt.Chart(secdf, title="Correlation between Public Crimes and Money spent by Wards on Security Cameras").encode(x='Year')
crimeline = secbase.mark_line(color='blue').encode(
    alt.Y('count').axis(title='Number of Public Crimes', titleColor='#5276A7'))
camline = secbase.mark_line(color='green').encode(
    alt.Y('cost').axis(title='Amount spent on Security Cameras', titleColor='green'))
timeline=alt.layer(crimeline, camline).resolve_scale(
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
            orient="bottom", title='Most Common Race'),
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
        color=alt.Color("Year:Q", scale=alt.Scale(scheme="blues"), title="Total number of crimes", legend=alt.Legend(orient='bottom')),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("Year:Q", title="Total Number of Crimes", format=",")
        ],
        stroke=alt.Stroke('Most Common Race:N', scale=alt.Scale(scheme='tableau10')).legend(
            orient="bottom", title='Most Common Race'),
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
            fields=list(races3) 
        )
    )
    .transform_calculate(selected_race="datum[cat_sel] || 0")
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
    y=alt.Y('neighborhoods:N', title='Neighborhood'),
    color=alt.Color('average(area):Q', scale=alt.Scale(scheme='blues'), legend=alt.Legend(orient='right', padding=67)),
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
        color=alt.Color("crash per 1k res:Q", scale=alt.Scale(scheme="purples"), title="Number of Crashes / 1k residents", legend=alt.Legend(orient='right', padding=50)),
        tooltip=[alt.Tooltip("properties.ward:O", title="Ward"), alt.Tooltip("crash per 1k res:Q", title="Number of Crashes / 1k residents")]
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
        color=alt.Color("unlit_to_lit_ratio:Q", scale=alt.Scale(scheme="greens"), title="Crash Ratio Relative to Lit Roads", legend=alt.Legend(orient='right', padding=50)),
        tooltip=[alt.Tooltip("properties.ward:O", title="Ward"), alt.Tooltip("unlit_to_lit_ratio:Q", title="Crashes on Unlit Roads/ on Lit Roads")]
    )
).properties(height=400)

transporttot=(percentage | areanorm).resolve_scale(color='independent') & (crash_chart | ratiolight_chart).resolve_scale(color='independent')
transporttot



##ALL THE GRAPHS FOR SCHOOLS

neiselect = alt.selection_point(
    fields=['neighborhoods'],
    bind='legend',
    value=[{'neighborhoods': 'Central'}]
)
income_chart = (
    alt.Chart(chicago_wards, title="Average Income by Ward")
    .mark_geoshape(strokeWidth=2.5)
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            acsinc,
            key="ward",
            fields=['average_income','neighborhoods'] 
        )).encode(
        color=alt.Color("average_income:Q", scale=alt.Scale(scheme="purples"), title="Average Income", legend=alt.Legend(orient='bottom')),
        stroke=alt.Stroke('neighborhoods:N', scale=alt.Scale(scheme='dark2')).legend(
            orient="top", title='neighborhoods ', padding=40),
        strokeOpacity=alt.condition(neiselect, alt.value(1), alt.value(0.1)),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("average_income:Q", title="Average Income")]
    )
).properties(width=360).add_params(
    neiselect
)

ambbase = alt.Chart(school_by_ward_ambition,title='School Ambition Assessment').mark_bar().transform_filter(neiselect)

ambpos_chart = ambbase.mark_bar().transform_filter(
    alt.datum.percentage >= 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', scale=alt.Scale(domain=[-100, 100]), axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='ascending')
)

ambneg_chart = ambbase.mark_bar().transform_filter(
    alt.datum.percentage < 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='descending')
)

ambchart = alt.layer(ambpos_chart, ambneg_chart).add_params(neiselect)

safbase = alt.Chart(school_by_ward_safety, title='School Safety Assessment').mark_bar().transform_filter(neiselect)

safpos_chart = safbase.mark_bar().transform_filter(
    alt.datum.percentage >= 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', scale=alt.Scale(domain=[-100, 100]), axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='ascending')
)

safneg_chart = safbase.mark_bar().transform_filter(
    alt.datum.percentage < 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='descending')
)

safchart = alt.layer(safpos_chart, safneg_chart).add_params(neiselect)

fambase = alt.Chart(school_by_ward_fam, title='Family Involvement Assessment').mark_bar().transform_filter(neiselect)

fampos_chart = fambase.mark_bar().transform_filter(
    alt.datum.percentage >= 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', scale=alt.Scale(domain=[-100, 100]), axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='ascending')
)

famneg_chart = fambase.mark_bar().transform_filter(
    alt.datum.percentage < 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='descending')
)

famchart = alt.layer(fampos_chart, famneg_chart).add_params(neiselect)

supbase = alt.Chart(school_by_ward_support, title='Supportive Environment Assessment').mark_bar().transform_filter(neiselect)

suppos_chart = supbase.mark_bar().transform_filter(
    alt.datum.percentage >= 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', scale=alt.Scale(domain=[-100, 100]), axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='ascending')
)

supneg_chart = supbase.mark_bar().transform_filter(
    alt.datum.percentage < 0
).encode(
    x=alt.X('ward:N', axis=alt.Axis(title='wards')),
    y=alt.Y('percentage:Q', axis=alt.Axis(labels=False, title='Relative Proportions')),
    color=alt.Color('response:N', scale=color_scale),
    order=alt.Order('sort_order:Q', sort='descending')
)

supchart = alt.layer(suppos_chart, supneg_chart).add_params(neiselect)

school_spending = (
    alt.Chart(chicago_wards, title="Spending on Schools & Libraries")
    .mark_geoshape(strokeWidth=2.3)
    .project(type="mercator")
    .transform_lookup(
        lookup="properties.ward",
        from_=alt.LookupData(
            costs_wide,
            key="ward",
            fields=['Schools & Libraries','neighborhoods']
        )
    )
    .encode(
        color=alt.Color("Schools & Libraries:Q", scale=alt.Scale(scheme="oranges"), title="Total SPENT").legend(
            orient="bottom", title='TOTAL SPENT', padding=50),
        tooltip=[
            alt.Tooltip("properties.ward:O", title="Ward"),
            alt.Tooltip("Schools & Libraries:Q", title="Total cost", format=",")
        ],
        stroke=alt.Stroke('neighborhoods:N', scale=alt.Scale(scheme='dark2')).legend(
            orient="top", title='neighborhoods ', padding=40),
        strokeOpacity=alt.condition(neiselect, alt.value(1), alt.value(0.1)),
    )
).add_params(
    neiselect
).properties(width=360)

schools_view= (income_chart| school_spending) | (ambchart & safchart | famchart & supchart)