"""
Erzeugt die Seite für die Untersuchung der Feature Importances der Daten

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
    st.write("## Analyse der Feature Importance")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'
    
    df = pd.read_csv(f"{folder}\\df_reference_discharges.csv", sep=',')
    selektion_b = st.multiselect("Wähle zu betrachtende Batterien aus",df['batteryname_'])
    selektion_a = st.multiselect("Wähle zu betrachtende Ampereentladungs Klassifizierung aus",df['verteilung'].unique())
    selektion_t = st.multiselect("Wähle zu betrachtende Raumtemperatur aus",df['raumtemperatur'].unique())
    selektion_r = st.multiselect("Wähle zu betrachtende Randomisierungsart aus",df['randomisiert'].unique())
    
    # filterungen für das bar chart
    if len(selektion_b) > 0:
        df = df[df.batteryname_.isin(selektion_b)]
    if len(selektion_a) > 0:
        df = df[df.verteilung.isin(selektion_a)]
    if len(selektion_t) > 0:
        df = df[df.raumtemperatur.isin(selektion_t)]
    if len(selektion_r) > 0:
        df = df[df.randomisiert.isin(selektion_r)]
        
    figure = line_chart(df,'zyklus_','amperestunden','klasse')
    st.bokeh_chart(figure,use_container_width=True)