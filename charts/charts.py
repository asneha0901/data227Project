import altair as alt
import pandas as pd

def Intro_chart(chicago_wards_df: pd.DataFrame, cats_sorted, costs_wide: pd.DataFrame):
    cat_radio = alt.binding_radio(options=cats_sorted, name="Category: ")
    cat_sel = alt.param(name="cat_sel", value=cats_sorted[0], bind=cat_radio)

    joint_chart = (
        alt.Chart(chicago_wards_df, title="Expenditure by Ward (select category)")
        .mark_geoshape(stroke="#706545")
        .project(type="mercator")
        .add_params(cat_sel)
        .transform_lookup(
            lookup="ward",
            from_=alt.LookupData(costs_wide, key="ward", fields=list(cats_sorted))
        ).transform_calculate(selected_cost="datum[cat_sel]")
        .encode(
            color=alt.Color("selected_cost:Q", scale=alt.Scale(scheme="greens"), title="Total cost"),
            tooltip=[
                alt.Tooltip("ward:O", title="Ward"),
                alt.Tooltip("selected_cost:Q", title="Total cost", format=",")
            ],
        )
    )

    return joint_chart