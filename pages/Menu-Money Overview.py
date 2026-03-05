import streamlit as st
import altair as alt
from charts.charts_overview import spend_by_type, barchartcost

st.set_page_config(page_title="Story", layout="wide")

st.title("Overview of Chicago Menu-Money Spending Patterns")
st.markdown("**Central question:** *How do different wards allocate their Chicago Menu-Money Over the Years*")

st.header("Chicago Menu-Money Total Spending by category (minus Lighting and Streets/Transportation)")
st.write("To interactively see exactly how different geographical sections of wards deal with spending their Chicago Menu Money we can look at a selection of them")
st.altair_chart(barchartcost, width='stretch')
