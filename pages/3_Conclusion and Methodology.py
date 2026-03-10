import streamlit as st
import altair as alt

st.set_page_config(page_title="Methodology", layout="wide")
st.header("CONCLUSION")

st.subheader("Main Take-Aways")
st.write("We began this project with a consideration of Chicago as one of the largest segregated cities in the U.S.A. As we explored this dataset, we wanted to point the few ways in which political practices like jerrymandering for ward maps can grossly influence social outcomes.")
st.write("""
         To this end, a few take-home messages from our understanding of this dataset would include:
         1. Streets & Transportation and Lighting comprises the bulk of a ward's budget. 
         2. While neighborhoods in the north, which tend to be smaller, are able to spare enough of the budget after spending on Streets & Transportation and Lighting, neighborhoods in the south, which tend to be larger, are unable to.
         3. Additionally, neighborhoods in the south are still unable to cover their needs full for even Streets & Transportation and Lighting
         4. Different wards have differing concerns/ priorities with infrastructure spending.
         5. While central neighborhoods are able to manage crime rates with security cameras as an infrastructure feature, prodominantly African American neighborhoods are struggling to implement the same security features due to inadequate funds.
         6. Neighborhoods in the north are also able to better supplement the quality of education additional to the advantages given by their average high income.
         7. Considerations of ward areas should be accounted for when re-drawing the ward map as it seems to skew resource allocation against historically underresourced communities.
         """)
st.subheader("Limitations")
st.write("Our dataset looks at spending from 2012-2021 but the wards were redrawn in 2015. This impacts our analysis to some extent since a large part of our analysis is dependent on spatial clustering. Moreover, our analysis doesn't take into account other provisions for infrastructure concerns like private donors, neighborhood councils, emergency funds, lobbying, etc. This might endanger some of the conclusions/ assumptions about source of 'essential' vs 'non-essential' infrastructure budgets. ")

st.subheader("Future Directions")
st.write("One future direction we wish to expand upon is to integrate lobbying data publically available to understand how many additional sources of income are there for different wards. Additionally, given that parks and recreation was a major spending point for multiple ward it would be interested to gather data about community areas in different wards and their maintainence status and usage.")

st.header("DISCLAIMER AND ETHICS STATEMENT")
st.write("Although the data used in this project was not directly involving the information derived from individually identifiable human subjects, the broader implications of our analyses certainly have tangible effects on the lives of the residents of Chicago. This analysis highlights the geographic inequities across active Chicago neighborhoods, which can at times result in the reinforcement of negative narratives about certain neighborhoods. The observed educational and socioeconomic disparities are influenced directly and indirectly by complex history and hundreds of years of societal factors. These findings should not be interpreted as attributing the cause of unequal circumstances to individual residents or schools. The data used was publicly available and aggregates of the larger population. Because our analysis was concerned with the ward-level structural patterns and outcomes, our claims and conclusions can be based upon trends, rather than individual neighborhoods or schools. The interpretation of our results was done with caution, merely representing correlations and confounding observations without insisting on direct causal inference. ")
st.write("Additionally, menu money merely represents only a portion of total public spending in Chicago, and does not take into account all investments (private, or other kinds) that go into infrastructure and/or education. Exact demographic differences and state funding formulas were not fully incorporated. This analysis scratches the surface of a much larger, multifaceted issue involving historical segregation and longstanding differences across Chicago neighborhoods.")
st.write("With more time, incorporating other sources of data would provide the analysis with an even more robust view into Chicago resource allocations. Property taxes or other demographic data, as well as a more detailed view into school funding and individual programs would accomplish this goal. Additionally, building an analysis that stretches across multiple years to further observe the outcomes of certain menu money allocations would build a more robust analysis.")

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
st.write("For each visualization, here is a rationale behind our choices")
st.markdown(""" 
            **For Figure 1:**
            1. Stroke color for neighborhoods: We initially used centroid points to indicate neighborhoods and allowed users to have more freedom to select groups of wards to take a closer look at. However, as we conducted out literature search on the differences in Chicago neighborhoods/ sides, we decided it would be more concise and informative to guide the selection of groups of wards by restricting it to neighborhoods. This couldn't be done by fill color since we were using fill color to indicate the relative amount of spending per category.
            2. Fill Color for Spending per category: We chose to use fill color to show spending because it was the clearest way of demonstrating where spending on each category is concentrated spatially. We chose the single hue gray scale so it wouldn't interfere with visualizations of the different neighborhoods or suggest any lines of correlation between the fill color and the bar chart.
            3. Bar chart for category spending: We chose to use a bar chart for this quantitative variable to best demonstrate how the bars move/ values increase or decrease with the changes in neighborhoods. This was fairly effective due to the static scale we used that allowed users to see the magnitude of spending on categories by neighborhoods.
            """)
st.markdown(""" 
            **For Figure 2:**
            1. Dual Axis Line Chart: We chose using a line chart to show trends along time as it is the most cohesive way of establishing whether both variables change similarly to each other. Furthermore, by using a dual axis we were able to keep them on the same chart and make the comparison more feasible. The color of the axis labels also act as legends for what the lines denote making the dual axis line chart a minimalist visualization of trends along time.
            2. Race distribution choropleth: We used a choropleth with a radio button to select for which race to observe in the color purple so it wouldn't clash with the colors that already have attached meaning from the line graph. Since the values are in proportions, a choropleth is effective since it doesn't have extremes in any of the categories. moreover, the main focus of our project is to look at data spatially so a choropleth is an audience-friendly way to do so.
            3. Stroke color for most common race: To make our analysis more clear and guided, we also decided to encode the most common race in our two choropleths using stroke color which would prevent viewers from having to switch between looking at choropleths to make observations about race with money spent on cameras and crime
            4. Colors for the choropleths: We decided to use greens for the choropleth on money spent on cameras and blues for the choropleth on number of crimes as they corresponded well with the colors in the line graph allowing for visual continuity and representation of the same variable with the same encoding across figures.
            """)
st.markdown("""
            **For Figure 3:**
            1. Bar graphs for both proportions: We wanted to use a type of chart that could be repeated twice to show the difference between the proportion of money spent on the categories and how quickly that changes when normalized over area. To make the comparison clear we used bar charts for both.
            2. Hue for area: In the first bar chart we also wanted to represent area before normalizing it and showing the output to illustrate the differences in average area that we noticed by eye on the ward map but is more evidently quantified using color in the bar graph.
            3. Colors on the choropleth: In the interest of concistency and visual continuity, we used the same colors that were present in the bar graphs (green and purple) to represent the two variables in the choropleths (Lighting and Streets)
            """)
st.markdown("""
            **For Figure 4:**
            1. Diverging bar charts for school assessments: Since we had two scales of values (positive assessments and negative assessments) we decided to use a diverging bar chart with a stable center (0). This makes it easy to compare values that move in opposite directions.
            2. Colors for diverging bar charts: We used green to evoke positive and reds to evoke negatives owing to classic color combinations that are intuitive for viewers.
            3. Stroke color for neighborhoods: We wanted to stay consistent with our groupings and so used stroke color for neighborhoods.
            """)
st.write("To understand more about how we conducted our analysis please refer to our markdown notebook that details our choices based on exploratory figures constructed before-hand.")
st.link_button("JUPYTER MARKDOWN FOR DATA PROCESSING", "https://github.com/asneha0901/data227Project/blob/main/.ipynb_checkpoints/ORGANIZED227PROJ.ipynb")