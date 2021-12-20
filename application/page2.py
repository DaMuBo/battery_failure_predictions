"""
Erzeugt die Einstellungen zu den Klassifizierungen in den Daten 
"""

import streamlit as st
import pandas as pd

import functions as fu

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6


def bar_chart(df,x,y,group, title="Bar Chart"):
    """
    
    creates a figure for showing in streamlit
    """
    
    data = df
    colormap = {0:'green',
                1:'lightgreen',
                2:'yellow',
                3:'orange',
                4:'red'
               }
    data['color'] = [colormap[x] for x in df[group]]
    source = ColumnDataSource(data)

    p = figure(title=title, x_range=data[x])
    p.vbar(source=source,x=x, top= y, fill_color='color')
    
    return p
    
    

def app():
    st.markdown("## Data Classification")
    
    c_fold = fu.get_folder()
    p_fold = c_fold + '\data\Prepared'
    folder = c_fold + '\data\Processed\Zyklus'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder_final}\\df_fertige_features.csv", sep=',')

    # Auswahl der klassifizierung
    df3 = df[df.comment_ == 'reference discharge']
    df3 = df3[['batteryname_']].groupby(df['batteryname_']).count()
    df3.columns = ['anzahl']


    liste = []
    for n in df3['anzahl']:
        if n > 60:
            liste.append(0)
        elif n > 30:
            liste.append(2)
        elif n > 15:
            liste.append(3)
        else:
            liste.append(4)
    df3['klasse'] = liste

    # blockchart auf reference discharge muss noch in plotly o.ä. geändert werden.
    titel = "Klassifizierung der Daten nach Anzahl Referenz Entladungen"
    figure = bar_chart(df3.reset_index().sort_values(['anzahl'], ascending=False),'batteryname_','anzahl','klasse', titel)
    st.bokeh_chart(figure,use_container_width=True)


    # Line Chart auf Reference Discharge
    st.write(df3)

