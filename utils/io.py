import streamlit as st
import pandas as pd
from vega_datasets import data
import numpy as np
import geojson
import json # just for viewing purposes
from pathlib import Path
import altair as alt
menu=pd.read_csv("/Users/snehaagarwal/data227Project/data/menu.csv")
chicago_wards_df = pd.read_json('/Users/snehaagarwal/Downloads/data/chicago-ward-boundaries.geojson')
chicago_wards_df['type'] = chicago_wards_df.features.apply(lambda x: x['type']) # Required! 
chicago_wards_df['geometry'] = chicago_wards_df.features.apply(lambda x: x['geometry'])
chicago_wards_df['ward'] = chicago_wards_df.features.apply(lambda x: x['properties']['ward'])
menu['cost'] = (
    menu['cost']
    .replace(r'[$,]', '', regex=True)
    .astype(float)
    .astype(int)
)
menu_schools=menu[menu['category']=='Schools & Libraries'][['ward','cost','year']]
menu_schools.groupby(['ward']).sum().reset_index()
cats = menu['category'].unique()

all_wards = pd.Index(range(1, 51), name='ward')
def category_cost_by_ward(menu, category) -> pd.DataFrame:
    """
    For a given category, return a dataframe with one row per ward (1..50)
    and the total cost in that ward for the category. Missing wards get 0.
    """
    all_wards = pd.Index(range(1, 51), name="ward")

    out = (
        menu.loc[menu["category"] == category, ["ward", "cost"]]
        .dropna(subset=["ward"])
        .groupby("ward", as_index=True)["cost"]
        .sum()
        .reindex(all_wards, fill_value=0)
        .reset_index()
    )
    return out 

results = {cat: category_cost_by_ward(menu, cat) for cat in cats}

costs_long = pd.concat(
    [df.assign(category=cat) for cat, df in results.items()],
    ignore_index=True
)
costs_wide = (
    costs_long
    .pivot_table(index="ward", columns="category", values="cost", aggfunc="sum", fill_value=0)
    .reset_index()
)

cats_sorted = sorted([c for c in costs_wide.columns if c != "ward"])


chicago_wards_df["ward"] = chicago_wards_df["ward"].astype(int)
menu["ward"] = pd.to_numeric(menu["ward"], errors="coerce").astype("Int64")

# after costs_wide is created
costs_wide["ward"] = costs_wide["ward"].astype(int)
