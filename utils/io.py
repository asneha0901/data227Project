import streamlit as st
import pandas as pd
from vega_datasets import data
import numpy as np
import geopandas as gpd
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
    1: "North Side", 2: "Central", 3: "South Side", 4: "South Side", 5: "South Side",
    6: "South Side", 7: "South Side", 8: "South Side", 9: "Far South Side", 10: "Far South Side",
    11: "South Side", 12: "Southwest Side", 13: "Southwest Side", 14: "Southwest Side",
    15: "Southwest Side", 16: "South Side", 17: "Southwest Side", 18: "Southwest Side",
    19: "Far South Side", 20: "South Side", 21: "Far South Side", 22: "Southwest Side",
    23: "Southwest Side", 24: "West Side", 25: "Central", 26: "West Side", 27: "Central",
    28: "West Side", 29: "West Side", 30: "Northwest Side", 31: "Northwest Side",
    32: "North Side", 33: "North Side", 34: "Far South Side", 35: "Northwest Side",
    36: "Northwest Side", 37: "West Side", 38: "Northwest Side", 39: "Northwest Side",
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
#MAKING THE YEAR BASED DB
def yearward(menu, category) -> pd.DataFrame:
    """
    For a given category, return a dataframe with one row per ward per year (1..50 x 2012-2023)
    and the total cost in that ward for the category. Missing wards get 0.
    """
    all_wards = pd.Index(range(1, 51), name="ward")

    out = (
        menu.loc[menu["category"] == category, ["ward", "cost", "year"]]
        .dropna(subset=["ward"])
        .groupby(by=["ward",'year'])["cost"]
        .sum()
        .reset_index()
    )
    return out 

results2 = {cat: yearward(menu, cat) for cat in cats}
year_long = pd.concat(
    [df.assign(category=cat) for cat, df in results2.items()],
    ignore_index=True
)
year_total=year_long.groupby(["year","category"]).sum().reset_index()
year_total_nost = year_total[year_total['category']!="Streets & Transportation"]
year_total_nost = year_total_nost[year_total_nost['category']!= "Lighting"]
yr2021=year_long[year_long['year']==2021]
yr2021sec=yr2021[yr2021['category']=='Security Cameras']
yr2021sec=yr2021sec.rename(columns={"ward":"WARDS"})
yr2021sec=yr2021sec.groupby("WARDS", as_index=True)["cost"].sum().reindex(all_wards, fill_value=0).reset_index()
yr2021sec['cost']=yr2021sec['cost'].astype(int)


#ADDING THE NECESSARY DATABASES FOR THE CRIME VISUALIZATION
crime21=pd.read_csv("data/Crimes2021.csv")
crime21=crime21[crime21['Domestic']==False]
crime21['Primary Type'].unique()
public=['MOTOR VEHICLE THEFT', 'THEFT', 'ASSAULT', 'BURGLARY', 'BATTERY', 'ROBBERY','CRIMINAL TRESPASS', 'KIDNAPPING', 'HOMICIDE']
crime21=crime21[crime21['Primary Type'].apply(lambda x: x in public)]
crime21=crime21.groupby("Ward", as_index=True)["Year"].count().reindex(all_wards, fill_value=0).reset_index()

#database for crime time
crimetime=pd.read_csv("data/Crimetime.csv")
crimetime['count'] = (
    crimetime['count']
    .replace(r'[$,]', '', regex=True)
    .astype(float)
    .astype(int)
)
crimetime['year']= (
    crimetime['Year']
    .replace(r'[$,]', '', regex=True)
    .astype(int)
)
seccam=year_total_nost[year_total_nost['category']=="Security Cameras"]
secdf=pd.merge(seccam, crimetime)
secdf['Year']=secdf['Year'].astype(str)

#database for demos
acs = pd.read_csv('data/ACS_5_Year_Data_by_Ward.csv')
crime21['Pop per 1k']=acs['Total Population']/1000
crime21['Crime per 1k']=crime21['Year']/crime21['Pop per 1k']
acs['White Ratio']=acs['White']/acs['Total Population']
acs['American Indian Ratio']=acs['American Indian or Alaska Native']/acs['Total Population']
acs['Black/AA Ratio']=acs['Black or African American']/acs['Total Population']
acs['Asian Ratio']=acs['Asian']/acs['Total Population']
acs['Native Hawaiian or Pacific Islander Ratio']=acs['Native Hawaiian or Pacific Islander']/acs['Total Population']
acs['Other Race Ratio']=acs['Other Race']/acs['Total Population']
acs['Multiracial Ratio']=acs['Multiracial']/acs['Total Population']
acs['White Not Hispanic or Latino Ratio']=acs['White Not Hispanic or Latino']/acs['Total Population']
acs['Hispanic or Latino Ratio']=acs['Hispanic or Latino']/acs['Total Population']
acs['All Other Ratio']= 1 - (acs['Black/AA Ratio']+acs['White Not Hispanic or Latino Ratio']+acs['Hispanic or Latino Ratio'])
races=['White Ratio', 'American Indian Ratio', 'Black/AA Ratio', 'Asian Ratio', 'Native Hawaiian or Pacific Islander Ratio', 'Other Race Ratio', 'Multiracial Ratio', 'White Not Hispanic or Latino Ratio', 'Hispanic or Latino Ratio' ]
races3=['Black/AA Ratio','All Other Ratio', 'White Not Hispanic or Latino Ratio', 'Hispanic or Latino Ratio' ]
acssub=acs[['Ward','Black/AA Ratio','All Other Ratio', 'White Not Hispanic or Latino Ratio', 'Hispanic or Latino Ratio']]

acssub['Most Common Race']=acssub[['Black/AA Ratio','All Other Ratio', 'White Not Hispanic or Latino Ratio', 'Hispanic or Latino Ratio']].idxmax(axis=1)
acssub['Ward']=acssub['Ward'].astype(int)
acssub=acssub.sort_values(by='Ward', ascending=True).reset_index()

yr2021sec['crime per 1k']=crime21['Crime per 1k']
yr2021sec['cost']=yr2021sec['cost'].replace(0,1)
yr2021sec['spent per crime per 1k']=yr2021sec['cost']/yr2021sec['crime per 1k']
yr2021sec['spent per crime per person']=yr2021sec['spent per crime per 1k']/1000
yr2021sec['Most Common Race']=acssub['Most Common Race']
yr2021sec['Most Common Race']=yr2021sec['Most Common Race'].str.replace(' Ratio', '', regex=False)
crime21['Most Common Race']=yr2021sec['Most Common Race']

#database for streets
sumspent=np.array(costs_long.groupby('ward').sum()['cost'])
sumspent2=np.append(sumspent, sumspent)
costs_long_st=costs_long[costs_long['category']=="Streets & Transportation"]
costs_long_lighting=costs_long[costs_long['category']=="Lighting"]
costs_long_top2=pd.concat([costs_long_st, costs_long_lighting], axis=0)
costs_long_top2['Total Spent by Ward']=sumspent2
costs_long_top2['Percentage spent on Category']=costs_long_top2['cost']/costs_long_top2['Total Spent by Ward']
chicago_wards_df['area'] = chicago_wards_df.features.apply(lambda x: x['properties']['shape_area'])
chicago_wards_df['ward']=chicago_wards_df['ward'].astype(int)
area=chicago_wards_df.sort_values(by='ward', ascending=True)['area']
area2=np.append(area, area)
costs_long_top2['area']=area2.astype(float)
costs_long_top2['neighborhoods']=costs_long_top2['ward'].map(ward_to_side)
costs_long_top2['cost on category by area']=costs_long_top2['cost']/costs_long_top2['area']

#database for crashs
crashs = pd.read_csv('data/crashes.csv')
defectcrash=crashs[crashs['ROAD_DEFECT']!='NO DEFECTS']
wardcrashcount=pd.read_csv('data/wardcrashcount.csv')


wardlitcrashcount=pd.read_csv('data/wardlitcrashcount.csv')


##DATA FOR SCHOOLS
school_with_ward=pd.read_csv('data/school_ward.csv')
school_by_ward = (
    school_with_ward.groupby("ward")
    .agg('sum')
    .reset_index()
)
school_by_ward['row_count'] = school_with_ward.groupby("ward").size().values
school_by_ward['ward']=school_by_ward['ward'].astype(int)
acs['average_income'] = (
    acs['Under $25,000'] * 12500 +
    acs['$25,000 to $49,999'] * 37500 +
    acs['$50,000 to $74,999'] * 62500 +
    acs['$75,000 to $125,000'] * 100000 +
    acs['$125,000 +'] * 150000
) / acs[['Under $25,000', '$25,000 to $49,999', '$50,000 to $74,999', '$75,000 to $125,000', '$125,000 +']].sum(axis=1)
acsinc=acs[['Ward','average_income']]
acsinc = acsinc.rename(columns={'Ward': 'ward'})
acsinc['neighborhoods']=acsinc['ward'].map(ward_to_side)

def create_diverging_df(df, prefix, row_count_col='row_count', ward_col='ward'):
    cols = [c for c in df.columns if c.startswith(prefix)]
    working = df[[ward_col, row_count_col] + cols].copy()
    
    working['data pres'] = working[row_count_col] - working[[c for c in cols if 'NOT ENOUGH DATA' in c or 'INSUFFICIENT' in c]].sum(axis=1)
    for col in cols:
        working[col] = (working[col] / working['data pres']) * 100
    
    neutral_col = [c for c in cols if 'NEUTRAL' in c and 'neg' not in c and 'pos' not in c][0]
    working[f'{prefix}_NEUTRAL_pos'] = working[neutral_col] / 2
    working[f'{prefix}_NEUTRAL_neg'] = working[neutral_col] / -2
    working[[c for c in cols if 'VERY WEAK' in c or c.endswith('_WEAK')]] *= -1
    
    final_cols = [f'{prefix}_STRONG', f'{prefix}_VERY STRONG', 
                  f'{prefix}_VERY WEAK', f'{prefix}_WEAK', ward_col]
    result = working[final_cols].copy()
    
    result.columns = ['strong', 'very_strong', 
                      'very_weak', 'weak', 'ward']
    
    result = result.melt(id_vars='ward', var_name='response', value_name='percentage')

    order_map = {r: i for i, r in enumerate(['very_weak', 'weak', 'strong', 'very_strong'])}
    result['sort_order'] = result['response'].map(order_map)
    label_map = {
        'very_weak': 'Very Weak',
        'weak': 'Weak',
        'strong': 'Strong',
        'very_strong': 'Very Strong'
    }
    result['response'] = result['response'].map(label_map)

    result=pd.merge(result, acsinc, on="ward")
    return result

school_by_ward_ambition=create_diverging_df(school_by_ward, "Ambition")
school_by_ward_safety=create_diverging_df(school_by_ward, "Safety")
school_by_ward_collab=create_diverging_df(school_by_ward, "Collaborative Teachers")
school_by_ward_lead=create_diverging_df(school_by_ward, "Effective Leaders")
school_by_ward_support=create_diverging_df(school_by_ward, "Supportive Environment")
school_by_ward_fam=create_diverging_df(school_by_ward, "Involved Families")

color_scale = alt.Scale(
    domain=['Very Weak','Weak','Strong','Very Strong'],
    range=['#e03c2d', '#f4a582', "#aff518","#00a60b"]
)