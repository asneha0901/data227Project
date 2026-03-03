import streamlit as st
from PIL import Image

st.set_page_config(page_title="EPL DASHBOARD", layout="wide")

st.title("English Premier League Statistics between Year 23-24 and Year 24-25")
st.write("This project is meant to help teams understand what are some strategies they can employ to increase their chances of overall game winning\n")
st.write(
    "Some sub questions I hope to be able answer using this story are:\n"
    "- **Home Advantage**:How much of an advantage is home advantage? Does home advantage usually correlate with a stronger defense or offense or both? .\n"
    "- **Success Rates**: Is there a correlation between shots taken, shots on target, goals and winning the game? Is it perhaps better to attempt more shots even if shot success rate is low?\n"
    "- **Changes through seasons**:  Did certain teams perform better in the first season as opposed to the second?\n"
)
st.info("Dataset: EPL 2324 AND 2425")