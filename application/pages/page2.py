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
    
    
def line_chart(df,x,y,group, title="Line Chart"):
    """
    Creates a figure to show a line chart for different lines
    """
    data = df
    liste = set(data['batteryname_'])
    colormap = {0:'green',
                1:'lightgreen',
                2:'yellow',
                3:'orange',
                4:'red'
               }
    data['color'] = [colormap[x] for x in df[group]]

    p = figure(title=title, x_axis_label=x, y_axis_label=y)
    for i in liste: 
        color = colormap[data[group][data.batteryname_== i].to_list()[0]]
        source = ColumnDataSource(data[data.batteryname_== i])
        p.line(source=source,x=x, y= y, line_color =color, legend_label=i)
    return p
    
    
def app():
    st.markdown("## Data Classification")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder}\\df_batterie_klasse.csv", sep=',')

    # blockchart auf reference discharge muss noch in plotly o.ä. geändert werden.
    titel = "Klassifizierung der Daten nach Anzahl Referenz Entladungen"
    figure = bar_chart(df.sort_values(['anzahl'], ascending=False),'batteryname_','anzahl','klasse', titel)
    st.bokeh_chart(figure,use_container_width=True)

    st.write(df)
    
    # line chart
    
    df = pd.read_csv(f"{folder}\\df_reference_discharges.csv", sep=',')
    st.write("Datensätze Reference Discharge",df)
    
    figure = line_chart(df,'zyklus_','amperestunden','klasse')
    st.bokeh_chart(figure,use_container_width=True)
    

