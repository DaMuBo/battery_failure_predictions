"""
Erzeugt die ersten Übersichten über die Daten - Anzahl Einträge je Batterie etc.

"""

import streamlit as st
import pandas as pd
import functions as fu

def app():
    st.markdown("## Data Overview")
    
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder}\\df_count_data_battery.csv", sep=',')
    st.write("Übersicht Dateneinträge nach Battery und Zyklus Typ\n", df)

    # hinzufügen klassifizierung aufgrund Anzahl reference discharges

    # KLassifikation der Batterien nach Gut / Mittel / Schlecht

