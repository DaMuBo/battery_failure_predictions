"""
Erzeugt die Seite für die analyse der Referenz Discharges
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
    st.markdown("## Analyse der Batterien / Referenz Entladungen")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder}\\df_batterie_klasse.csv", sep=',')
    # Auswahl Optionen erstellen
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
    # blockchart auf reference discharge
    titel = "Daten Klassifizierung nach Anzahl Referenz Discharges"
    figure = bar_chart(df.sort_values(['anzahl'], ascending=False),'batteryname_','anzahl','klasse', titel)
    st.bokeh_chart(figure,use_container_width=True)
    
    # line chart
    df = pd.read_csv(f"{folder}\\df_reference_discharges.csv", sep=',')
    
    # filterungen für die line charts
    if len(selektion_b) > 0:
        df = df[df.batteryname_.isin(selektion_b)]
    if len(selektion_a) > 0:
        df = df[df.verteilung.isin(selektion_a)]
    if len(selektion_t) > 0:
        df = df[df.raumtemperatur.isin(selektion_t)]
    if len(selektion_r) > 0:
        df = df[df.randomisiert.isin(selektion_r)]
        
    st.write("Datensätze Reference Discharge",df)
    
    figure = line_chart(df,'zyklus_','amperestunden','klasse')
    st.bokeh_chart(figure,use_container_width=True)
    
    st.write("Datensätze Reference Discharge nach Zeitverlauf in Sekunden")
    figure = line_chart(df, 'time_amin','amperestunden','klasse')
    st.bokeh_chart(figure,use_container_width=True)
    
    st.write("Datensätze Reference Discharge nach Zeitverlauf in Sekunden klassifiziert nach Ampereentladungsstärke")
    figure = line_chart(df, 'time_amin','amperestunden','verteilung')
    st.bokeh_chart(figure,use_container_width=True)
    
    st.write("Datensätze Reference Discharge nach Zeitverlauf in Sekunden klassifiziert nach raumtemperatur")
    figure = line_chart(df, 'time_amin','amperestunden','raumtemperatur')
    st.bokeh_chart(figure,use_container_width=True)
    
    st.write("Datensätze Reference Discharge nach Zeitverlauf in Sekunden klassifiziert nach Entlade/Aufladeart")
    figure = line_chart(df, 'time_amin','amperestunden','randomisiert')
    st.bokeh_chart(figure,use_container_width=True)
