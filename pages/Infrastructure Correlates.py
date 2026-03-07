import streamlit as st
import altair as alt
from charts.charts_crime import crimefullchart, timeline, spatial, transporttot

st.set_page_config(page_title="Correlates", layout="wide")
st.title("Overview of Chicago Menu-Money Spending Patterns")

st.header("Correlations between race and under-resourced neighborhoods can lead to misconceived stereotypes")
st.subheader("What is the graph below addressing?")
st.write("[Stuart et al (2024)](%s) conducted a sentiment analysis on articles by the Chicago Tribune mentioning one of the 77 Chicago community areas. The sentiment analysis was then used to score the overall reputation of each community area to reflect public perception or media-propagated perception of Chicago neighborhoods. A key finding from this thorough analysis was that the reputation of a neighborhood and their status in a neighborhood hierarchy is negatively related to the proportion of black residents in the neighborhood. Adding on to this concern, they also noted that the strength of this relationship increased with time. The paper reveals the importance of media reporting in forming such perceptions. " % "https://journals.sagepub.com/doi/full/10.1177/00420980241297088")
st.write("Moreover, articles such as [this](%s) listing most “dangerous” neighborhoods in Chicago often strengthen such biases and ignore confounding variables like availability of resources to certain neighborhoods. The graph below shows how public crime rates in Chicago have changed between 2012 and 2023 along with changes in amount of money spent by the city (through the menu-money fund) overall on security cameras. This data is supplemented with a spatial analysis of race demographics, amount of money spent on security cameras per crime per person in each ward in 2021 and the total number of crimes in each ward in 2021." % "https://www.fox32chicago.com/news/chicago-most-dangerous-neighborhoods")
st.altair_chart(crimefullchart, use_container_width=True)
st.write("here is the analysis")

st.header('Even though most money is spent on Streets & Transportation + Lighting, the spending is still insufficient for some neighborhoods')
st.altair_chart(transporttot, use_container_width=True)
st.write("here is the analysis")

