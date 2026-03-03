import streamlit as st
import altair as alt
from charts.charts import spend_by_type

st.set_page_config(page_title="Story", layout="wide")

st.title("Overview of Chicago Menu-Money Spending Patterns")
st.markdown("**Central question:** *How do different wards allocate their Chicago Menu-Money Over the Years*")

st.header("Chicago Menu-Money Spending by Category")
st.write("To begin with let us see which each type of category is prioritized in different wards.")
st.altair_chart(spend_by_type, width='stretch')
st.caption("Takeaway:")
