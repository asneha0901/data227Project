import streamlit as st
import altair as alt
from charts.charts_overview import spend_by_type, barchartcost

st.set_page_config(page_title="Overview", layout="wide")

st.title("Overview of Chicago Menu-Money Spending Patterns")

st.header("Chicago Menu-Money Total Spending by Category (minus Lighting and Streets/Transportation)")
st.write("To interactively see exactly how different geographical sections of wards deal with spending their Chicago Menu Money we can look at a selection of them")

st.subheader("What is the data being visualized?")
st.write("There are nine categories under which the alders can allocate/ spend their menu-money. Spending in each category reflects severity of the concerns faced by neighborhoods and their priorities. In understanding which categories get priority in the menu-money spending, it is essential to understand alternate funding sources for categories. While categories like parks and recreation, schools and libraries and Plants, Gardens, & Sustainability, may have alternate private funding sources (like tuition, resident neighborhood associations, private organizations, etc.), certain categories like Streets & Transportation, Lighting and Beautification are almost entirely dependent on the city’s resources and the menu-money for maintenance. The choropleth below shows how different wards spend on each category (chosen using the radio buttons below) relative to each other. While majority of the menu-money spending for all wards is attributed to Streets & Transportation and Lighting, the relative quantities of money allocated to these necessities differ. Furthermore, the map below divides the wards into multiple Chicago sides to show how these trends reflect the segregated nature of Chicago based on geographical regions. Navigating by clicking on the different sides on the legend will allow you to see the average amount of menu-money between 2012 and 2023 spent on the different categories in the Chicago side selected in the bar chart. The categories in the bar chart exclude Streets & Transportation and Lighting to allow for a more even scale and a clear visualization of trends in spending in other categories. ")

st.altair_chart(barchartcost, width='stretch')
st.markdown("#### Figure 1:Summary of Spending by Ward on different categories with corresponding bar chart aggregating by neighborhood")
st.subheader("What can we learn from relative spending on the choropleth?")
st.markdown("""
            Some notable observations throughout the categories include:
            * Streets & Transportation: increased relative spending on Streets & Transportation as wards move further from central Chicago
            * Bike infrastructure: minimal spending for most wards except for a few confined specifically to the North Side
            * Schools & Libraries and Plants, Gardens & Sustainability: densest in the north side, far north side and northwest side
            * Beautification: most prevalent in the central area possibly owing to high tourism density in the center
            
            While trends in relative spending indicates major differences in how wards allocate their resources, looking at the average absolute spending by category by side allows us to note how many resources are allocated to necessities (Streets & Transportation and Lighting as they don’t have other funding sources) and how many are allocated to secondary needs that could have alternate funding sources. It is reasonable to assume that in an order of priority, menu-money is spent on non-essential categories only when there is surplus to spare after addressing needs of Streets & Transportation and Lighting
""")

st.subheader("What can we learn from spending on non-essential categories by Chicago Side?")
st.markdown("""
            Some General obersavations include:
            * Far South Side and South Side: unable to expend more than 300,000 dollars at most on any category on average per ward with most remaining money (after expenditure on Streets & Transportation and Lighting) being expended on security cameras and parks and recreation
            * Far North Side and North Side: can spend up to 700,000 on a singular category on average per ward with most remaining money being expended on Parks & Recreation and Schools & Libraries
            * Central Chicago: large portion of their allocated money on security cameras possibly owing to the high-density population of the central area wards.
            * West Side, Northwest Side and Southwest side: spend a considerable amount of money on parks and recreation possibly due to the low population density in these wards and proximity to Chicago suburbs

            This reflects that different Chicago sides have differing infrastructure concerns outside of the necessities of Streets & Transportation and Lighting. While the northern Chicago wards, are able to expend more money on non-essentials with bulk of their focus on Parks & Recreation and Schools & Libraries, the southern Chicago wards have on average a smaller budget for non-essentials with bulk of their focus on security cameras and Parks & Recreation. Infrastructure in other Chicago sides not just reflects infrastructure needs but also infrastructure priorities with tourism rich wards expending more on beautification and security
""")