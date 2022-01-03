import functions as fu
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

from application.bokeh_chart import *
from application.multipage import *
from application.pages import page1,page2,page3,page4 # import pages here

def create_appdata(location):
    """
    Erzeugt zu den Features weitere Informationen die für die Analyse notwendig sind und legt diese ab.
    """
    folder = location + '\data\Application' # application folder
    folder_final = location + '\data\Processed\\final'

    df = pd.read_csv(f"{folder_final}\\df_fertige_features.csv", sep=',')

    # Datensätze je Battery
    df2 = pd.DataFrame(df[['batteryname_','comment_']])
    df2 = df2.groupby(['batteryname_','comment_']).agg({'batteryname_':'count'})
    df2.to_csv(f"{folder}\\df_count_data_battery.csv", sep=',', index=True)
    
    df_sum = df[df.type_ == 'D'][['batteryname_','amperestunden']].groupby(['batteryname_']).agg({'amperestunden':'sum'}).rename(columns={'amperestunden':'amperestunden_gesamt'}).reset_index()
    
    # Berechnung anzahl Reference discharges je battery
    df2 = df[df.comment_ == 'reference discharge'].copy()
    df3 = df2[['batteryname_']].groupby(df2['batteryname_']).count().copy()
    df3.columns = ['anzahl']
    
    # KLassifikation nach anzahl Discharges
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
    
    df3 = df3.reset_index()
    # klassifikation nach Amperezahl
    liste = []
    for n in df3['batteryname_']:
        if n in ['RW17','RW18','RW19','RW20','RW25','RW26','RW27','RW28']:
            liste.append('hohe Ampere')
        elif n in ['RW13','RW14','RW15','RW16','RW21','RW22','RW23','RW24']:
            liste.append('niedrige Ampere')
        else:
            liste.append('neutrale Ampere')
    df3['verteilung'] = liste
    
    # klassifikaton nach raumtemperatur
    liste = []
    for n in df3['batteryname_']:
        if n in ['RW21','RW22','RW23','RW24','RW25','RW26','RW27','RW28']:
            liste.append('40')
        else:
            liste.append('20-25')
    df3['raumtemperatur'] = liste
    
    # klassifikation nach auf und entladungs randomisierung
    liste = []
    for n in df3['batteryname_']:
        if n in ['RW9','RW10','RW11','RW12']:
            liste.append('auf- und entladen')
        else:
            liste.append('entladen')
    df3['randomisiert'] = liste
            
    

    df3.to_csv(f"{folder}\\df_batterie_klasse.csv", sep=',', index=True)
    
    df2 = df2.merge(df3, left_on="batteryname_",right_on="batteryname_")
    df2.to_csv(f"{folder}\\df_reference_discharges.csv", sep=',', index=False)
    
    df = df.merge(df3, left_on="batteryname_",right_on="batteryname_")
    df = df.merge(df_sum, left_on="batteryname_",right_on="batteryname_")
    df.to_csv(f"{folder}\\df_app_data.csv", sep=',', index=False)
    
    df_sum.to_csv(f"{folder}\\df_battery_leistung.csv", sep=',', index=False)
    
    # aufbereitung für feature importance
    daten = pd.read_csv(f"{folder_final}\\df_fertige_features.csv", sep=',')
    daten = daten[daten.comment_ == 'reference discharge']
    daten.drop(["batteryname_","comment_","type_"], axis=1, inplace=True) #brauch ich hier nicht
    daten.drop(["time_amin"], axis=1, inplace=True) #zu viel überschneidung mit *_leicht_vorher
    daten = daten[daten["amperestunden"] != 0]
    spalten_mit_ausreißern = ["temperature_amax","temperature_amin",'temperature_mean']
    for spalte in spalten_mit_ausreißern:
        neuer_wert = daten[daten[spalte] > np.percentile(daten[spalte],10)][spalte].median() #ersetzen durch den Median der Restwerte
        daten.loc[daten[spalte] < np.percentile(daten[spalte],10),spalte] = neuer_wert
    daten.to_csv(f"{folder}\\df_feature_importance_data.csv", sep=',', index=False)
    
    return True



c_fold = fu.get_folder()


# Create an instance of the app 
app = MultiPage()

if st.sidebar.button("reload data preparations for Application"):
    create_appdata(c_fold)
# Title of the main page
st.title("Analysis of Battery Failure Predictions")

# Add all your applications (pages) here
app.add_page("Data Overview", page1.app)
app.add_page("Reference Discharge Analysis", page2.app)
app.add_page("Battery Ampere Hour Analysis", page3.app)
app.add_page("Feature Importance Analysis", page4.app)
#app.add_page("Data Analysis",data_visualize.app)
#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()


