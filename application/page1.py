"""
Erzeugt die ersten Übersichten über die Daten - Anzahl Einträge je Batterie etc.

"""

import streamlit as st
import pandas as pd
import functions as fu

def app():
    st.markdown("## Data Overview")
    
    c_fold = fu.get_folder()
    p_fold = c_fold + '\data\Prepared'
    folder = c_fold + '\data\Processed\Zyklus'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder_final}\\df_fertige_features.csv", sep=',')



    # Datensätze je Battery
    df2 = pd.DataFrame(df[['batteryname_','comment_']])
    df2 = df2.groupby(['batteryname_','comment_']).agg({'batteryname_':'count'})
    st.write("Übersicht Dateneinträge nach Battery und Zyklus Typ\n", df2)

    # hinzufügen klassifizierung aufgrund Anzahl reference discharges

    # KLassifikation der Batterien nach Gut / Mittel / Schlecht

