import streamlit as st
import altair as alt
from charts.charts_crime import crimefullchart, timeline, spatial, transporttot

st.set_page_config(page_title="Story", layout="wide")
st.title("Overview of Chicago Menu-Money Spending Patterns")

st.header("Correlations between race and under-resourced neighborhoods can lead to misconceived stereotypes")
st.altair_chart(crimefullchart, use_container_width=True)
st.write("here is the analysis")

st.header('Even though most money is spent on Streets & Transportation + Lighting, the spending is still insufficient for some neighborhoods')
st.altair_chart(transporttot, use_container_width=True)
st.write("here is the analysis")

