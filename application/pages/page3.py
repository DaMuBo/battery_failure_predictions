"""
Erzeugt die Seite für die analyse der unterschiedlichen Features und 
Auswirkungen auf die Batterie Laufzeit
"""
import streamlit as st
import pandas as pd

import functions as fu

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6

def app():
    st.markdown("## Analyse der Features Importance auf die Batterielaufzeit)
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'


    