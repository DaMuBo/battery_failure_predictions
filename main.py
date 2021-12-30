import functions as fu
import pandas as pd
import streamlit as st
import altair as alt

from application.bokeh_chart import *
from application.multipage import *
from application.pages import page1,page2 # import pages here

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
    df3.reset_index()
    df3.to_csv(f"{folder}\\df_batterie_klasse.csv", sep=',', index=True)
    
    df2 = df2.merge(df3, left_on="batteryname_",right_on="batteryname_")
    df2.to_csv(f"{folder}\\df_reference_discharges.csv", sep=',', index=False)
    
    df = df.merge(df3, left_on="batteryname_",right_on="batteryname_")
    df.to_csv(f"{folder}\\df_app_data.csv", sep=',', index=False)
    return True



c_fold = fu.get_folder()
create_appdata(c_fold)

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.title("Analysis of Battery Failure Predictions")

# Add all your applications (pages) here
app.add_page("Data Overview", page1.app)
app.add_page("Data Reference Discharges", page2.app)
#app.add_page("Machine Learning", machine_learning.app)
#app.add_page("Data Analysis",data_visualize.app)
#app.add_page("Y-Parameter Optimization",redundant.app)

# The main app
app.run()


