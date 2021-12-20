import functions as fu
import pandas as pd
import streamlit as st
import altair as alt

from application.bokeh_chart import *

c_fold = fu.get_folder()
p_fold = c_fold + '\data\Prepared'
folder = c_fold + '\data\Processed\Zyklus'
folder_final = c_fold + '\data\Processed\\final'

df = pd.read_csv(f"{folder_final}\\df_fertige_features.csv", sep=',')

strHead = "Datenanalyse der Batteryzyklen"

st.title(strHead)

# Datensätze je Battery
df2 = pd.DataFrame(df[['batteryname_','comment_']])
df2 = df2.groupby(['batteryname_','comment_']).agg({'batteryname_':'count'})
st.write("Übersicht Dateneinträge nach Battery und Zyklus Typ\n", df2)

# Auswahl der Batterien ( Mehrfachauswahl möglich)

selectbox = st.sidebar.multiselect(
    "Select Batterys on Name",
    df['batteryname_'].sort_values().unique()
)
st.write(f"You selected {selectbox}")

# hinzufügen klassifizierung aufgrund Anzahl reference discharges

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
figure = bar_chart(df3.reset_index().sort_values(['anzahl'], ascending=False),'batteryname_','anzahl','klasse', "Klassifizierung der Daten nach Anzahl Referenz Entladungen")
st.bokeh_chart(figure,use_container_width=True)


# Line Chart auf Reference Discharge
st.write(df3)


# KLassifikation der Batterien nach Gut / Mittel / Schlecht