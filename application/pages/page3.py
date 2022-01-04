"""
Erzeugt die Seite für die analyse der Summeder geleisteten Amperestunden je Batterie über den gesamten Lebenszyklus
"""
import streamlit as st
import pandas as pd

import functions as fu
from application.bokeh_chart import *

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6






def app():
    st.markdown("## Analyse der geleisteten Amperestunden je Batterie")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder}\\df_battery_leistung.csv", sep=',')         
    st.write(df)
    
    titel = "Übersicht geleisteter Amperestunden je Batterie"
    figure = bar_chart(df.sort_values(['amperestunden_gesamt'], ascending=False),'batteryname_','amperestunden_gesamt',title=titel)
    st.bokeh_chart(figure,use_container_width=True)