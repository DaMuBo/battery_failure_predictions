import functions as fu
import pandas as pd
import streamlit as st
import altair as alt

from application.bokeh_chart import *
from application.multipage import *
from application import page1, page2 # import pages here



# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Analysis of Battery Failure Predictions")

# Add all your applications (pages) here
app.add_page("Data Overview", page1.app)
app.add_page("Data Classification", page2.app)
#app.add_page("Machine Learning", machine_learning.app)
#app.add_page("Data Analysis",data_visualize.app)
#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()


