import streamlit as st
from PIL import Image

st.set_page_config(page_title="Infrastructure in Chicago", layout="wide")

st.title("An Analysis of Chicago Menu Money Expenditure to reveal the status of Infrastructure concerns in Chicago")
st.write("The main aim of this project is to help understand what kind of infrastructure concerns are faced by different wards in Chicago and possible correlates they may reveal.\n")
st.write(
    "Some sub questions we hope to elucidate more on:\n"
    "- **Chicago Menu-Money Spending Over Time**: How have Chicago menu-money spending patterns changed over time. Such an analysis could indicate how different wards have developed over time and the signature concerns faced by wards.\n"
    "- **Correlations with Infrastructure Concerns**: In an effort to characterize what the infrastructure concerns indicate about each neighborhood, we plan to evaluate whether data about resident demographics, tourism, crime or education can reveal patterns in Chicago menu-money spending. \n"
    "- **What does this all mean**: Combining these two approaches could reveal underlying problems in wards providing a rationale for current Chicago menu-money spending habits but also provide another perspective on the history of segregation in Chicago. \n"
)
st.info("Datasets: Chicago menu-money dataset, Airbnb Data, Crimes Dataset, ACS Census Data, Chicago Public School Performance")