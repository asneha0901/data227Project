import streamlit as st
import altair as alt
from charts.charts_crime import crimefullchart, timeline, spatial

st.set_page_config(page_title="Story", layout="wide")
left, middle, right = st.columns((2, 6, 1))

with middle:
    st.header("Correlations between race and under-resourced neighborhoods can lead to misconceived stereotypes")
    st.altair_chart(crimefullchart, use_container_width=True)
