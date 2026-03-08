import streamlit as st
import altair as alt

st.set_page_config(page_title="Conclusion and Methodology", layout="wide")

st.header("TAKE HOME MESSAGES FROM THIS PROJECT")
st.write("<insert write-up here>")

st.header("OVERVIEW OF METHODOLOGY")
st.write("Our main approach to this project was to conduct first and foremost an exploratory analysis of how different Chicago wards spend their menu-money. As we proceeded with our exploratory analysis by using the scraped data from Jake Smith, we were able to not only noticed trends among wards that aggregated roughly with different Chicago Sides but we were also able to note trends along time and demographics. To further investigate this we picked out 4 categories that we found to be particularly interested to observe spatially: Streets & Transportation, Lighting, Schools & Libraries and Security Cameras. We brainstormed possible ways to test how the spending on these categories could have impacts on people and came up with a list of possible variables impacted by infrastructure spending in these categories listed below. ")
st.markdown("""
            **For Security Cameras:** 
            * Burglaries
            * Traffic Violations
            * General crime patrol
            * Density of Police Presence
            * CPD Spending
            
            After looking at available datasets on Chicago's open data portal, we chose to look at the crime dataset as that would give us freedom to choose what kind of crimes and test different effects""")
st.markdown("""
            **For Streets and Transportation:**
            * Potholes 311 requests
            * Vehicle accidents due to quality of roads
            * Amount of CTA ridership
            * Ratio of private vs public transporters
            
            **For Lighting:**
            * Vehicle crashes
            * Burglaries at night
            * Traffic 
            
            Since Vehicle crashes were common to both categories, we decided to focus on the data from Chicago's data portal on vehicle crashes that also notes the condition of the road (in terms of lighting and suitability) in each report. """)
st.markdown("""
            **For Schools and Libraries:**
            * Number of graduating students / suspensions
            * Post highschool outcomes
            * Mobility of students
            * Education levels in the district
            
            From the Chicago Data portal we were able to find information on 650 Chicago public Schools around the city and get their assessment reports from the year 2021-2022 to see how the cumulative funding over the past 10 years from the Menu-money fund affected outcomes. By choosing a year after our menu-money dataset ends, we decided to look at the impact of the spending as opposed to speculate on possible triggers for spending habits (the way we did for security cameras.)""")
st.write("Overall, we were able to clean the datasets and confine it to the selected durations that either overlapped with data from menu-money or followed directly after and analyse how spatially ward spending correlates with statistics on these different categories. Such an analysis allowed us to see how infrastructure spending by the ward plays a big role in general quality of life and well being in different neighborhoods possibly suggesting that the root solution to some of the issues lies in better budget allocation practices.")
st.write("To understand why we chose specific visualization choices and encodings over others please refer to our markdown notebook that details our choices based on exploratory figures constructed before-hand.")
st.link_button("JUPYTER MARKDOWN FOR DATA PROCESSING", "https://github.com/asneha0901/data227Project/blob/main/.ipynb_checkpoints/ORGANIZED227PROJ.ipynb")