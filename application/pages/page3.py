"""
Erzeugt die Seite für die analyse der Summeder geleisteten Amperestunden je Batterie über den gesamten Lebenszyklus
"""
import streamlit as st
import pandas as pd

import functions as fu

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6



def bar_chart(df,x,y,group=None, title="Bar Chart"):
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
    if group is not None:
        data['color'] = [colormap[x] for x in df[group]]
        source = ColumnDataSource(data)
        p = figure(title=title, x_range=data[x])
        p.vbar(source=source,x=x, top= y, fill_color='color')
    else:
        source = ColumnDataSource(data)
        p = figure(title=title, x_range=data[x])
        p.vbar(source=source,x=x, top= y, width = 0.9)
        p.xgrid.grid_line_color = None
    
    return p




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