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

import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def app():
    st.write("## Analyse der Feature Importance")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'
    
    df = pd.read_csv(f"{folder}\\df_feature_importance_data.csv", sep=',')
    
    # Histogramme erzeugen
    st.set_option('deprecation.showPyplotGlobalUse', False)
    df.hist(bins=50, figsize=(20,15))
    plt.show()
    st.pyplot()
    
    st.write("## Korrelationen der Features zu den Amperestunden")
    correlation = df.corr()
    plt.figure(figsize=(8,8))
    sns.heatmap(correlation[["amperestunden"]].sort_values(by=['amperestunden'], ascending=False), vmin=-1, cmap='coolwarm', annot=True)
    st.pyplot()