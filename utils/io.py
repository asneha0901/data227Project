import streamlit as st
import pandas as pd
from vega_datasets import data
import numpy as np
import geojson
import altair as alt
menu=pd.read_csv("data/menu.csv")
chicago_wards_df = pd.read_json('data/chicago-ward-boundaries.geojson')
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
costs_wide["ward"] = costs_wide["ward"].astype(int)
costs_long['ward']=costs_long['ward'].astype(int)
# dictionary from earlier
ward_to_side = {
    1: "North Side", 2: "Central", 3: "South Side", 4: "Central", 5: "South Side",
    6: "South Side", 7: "South Side", 8: "South Side", 9: "South Side", 10: "South Side",
    11: "West Side", 12: "West Side", 13: "Southwest Side", 14: "Southwest Side",
    15: "Southwest Side", 16: "Southwest Side", 17: "Southwest Side", 18: "Southwest Side",
    19: "Southwest Side", 20: "South Side", 21: "Southwest Side", 22: "West Side",
    23: "Southwest Side", 24: "West Side", 25: "West Side", 26: "Northwest Side", 27: "Central",
    28: "West Side", 29: "West Side", 30: "Northwest Side", 31: "Northwest Side",
    32: "North Side", 33: "North Side", 34: "South Side", 35: "Northwest Side",
    36: "Northwest Side", 37: "Northwest Side", 38: "Northwest Side", 39: "Far North Side",
    40: "Far North Side", 41: "Far North Side", 42: "Central", 43: "North Side",
    44: "North Side", 45: "Northwest Side", 46: "North Side", 47: "North Side",
    48: "Far North Side", 49: "Far North Side", 50: "Far North Side"
}

# add neighborhoods column
costs_wide["neighborhoods"] = costs_wide["ward"].map(ward_to_side)
costs_long['neighborhoods']=costs_long["ward"].map(ward_to_side)
chicago_wards_df["ward"] = chicago_wards_df["ward"].astype(int)
menu["ward"] = pd.to_numeric(menu["ward"], errors="coerce").astype("Int64")

costs_lon_nostreets = costs_long[costs_long['category']!='Streets & Transportation']
costs_lon_nostreets = costs_lon_nostreets[costs_lon_nostreets['category']!='Lighting']
def mid_ward(row): 
    '''Get a geometry column and return the middle of the geo area'''
    return np.array(row['coordinates'][0][0]).mean(axis=0)



chicago_wards_df['middle'] = chicago_wards_df['geometry'].apply(lambda x: mid_ward(x))
chicago_wards_df['middle'].head()

chicago_wards_df['ward']=chicago_wards_df['ward'].astype(int)
merged_data2 = chicago_wards_df.merge(
    costs_lon_nostreets[['ward', 'category', 'cost', 'neighborhoods']], 
    on='ward', 
    how='left'
)
merged_data2['long'] = merged_data2['middle'].apply(lambda x: x[0])
merged_data2['latt'] = merged_data2['middle'].apply(lambda x: x[1])
points_df2 = merged_data2[["long", "latt", "ward", "cost", "category", "neighborhoods"]].copy()
