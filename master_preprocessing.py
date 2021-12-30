import pandas as pd
import numpy as np

import os
import sys
import logging

import functions as fu
from feature_engineering import *

def stark_leicht(type_, current_mean, relativeTime_amax):
    entladen_stark = 0
    entladen_leicht = 0
    laden_stark = 0
    laden_leicht = 0
    pause = 0
    
    
    if type_ == 'D': #discharge
        if current_mean >= 3:
            entladen_stark = relativeTime_amax
        else:
            entladen_leicht = relativeTime_amax
    if type_ == 'C': #charge
        if current_mean <= -3:
            laden_stark = relativeTime_amax
        else:
            laden_leicht = relativeTime_amax
    if type_ == 'R':
        pause = relativeTime_amax
    return entladen_stark, entladen_leicht, laden_stark, laden_leicht, pause

    

def temp_hoch(temperature_amax, relativeTime_amax):
    temp_hoch = 0
    if temperature_amax >= 30:
        return relativeTime_amax
    else:
        return 0
        
if _name__ == "__main__":
    # Pfade setzen
    c_fold = fu.get_folder()
    p_fold = c_fold + '\data\Prepared'
    folder = c_fold + '\data\Processed\Zyklus'
    folder_final = c_fold + '\data\Processed\\final'


    # Initialize Logging
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler(
                                filename='datalogger.log',
                                mode='a',
                                encoding='utf-8'),
                            logging.StreamHandler(sys.stdout)])


    for file in os.listdir(p_fold):
        if ".csv" in file:
    # file = "prepared_RW1.csv" #für tests nur eins
            logging.info(f"<<< Started processing file: {file} >>>")
            new_filename = file.replace("prepared","processed")

            df = pd.read_csv(f"{p_fold}\\{file}", index_col = 0,
                                     #nrows= 100000
                                    )
            logging.info(f"<<< Size of Dataframe: {df.shape} >>>")

            #Auf Ebene Batterie + Zyklus gruppieren mit benötigten Aggregationen
            df_pv = pd.pivot_table(
               df,
               index=['batteryname','zyklus','comment','type'],
               aggfunc={'time': np.min, 'relativeTime':  np.max, 'voltage': [np.min, np.max, np.mean], 'current': [np.min, np.max, np.mean], 'temperature': [np.min, np.max, np.mean]}
            ).reset_index()

            df_pv.columns = ['_'.join(col) for col in list(df_pv.columns)]



            df_pv['time_entladen_stark'],df_pv['time_entladen_leicht'],df_pv['time_laden_stark'],df_pv['time_laden_leicht'],df_pv['time_pause']  = zip(*df_pv.apply(lambda x: stark_leicht(x['type_'],x['current_mean'],x['relativeTime_amax']),axis=1))

            df_pv['time_entladen_stark_vorher'] = df_pv.time_entladen_stark.cumsum()
            df_pv['time_entladen_leicht_vorher'] = df_pv.time_entladen_leicht.cumsum()
            df_pv['time_laden_stark_vorher'] = df_pv.time_laden_stark.cumsum()
            df_pv['time_laden_stark_vorher'] = df_pv.time_laden_leicht.cumsum()
            df_pv['time_pause_vorher'] = df_pv.time_pause.cumsum()


            df_pv['time_temp_hoch'] = df_pv.apply(lambda x: temp_hoch(x['temperature_amax'],x['relativeTime_amax']),axis=1)

            df_pv['time_temp_hoch_vorher'] = df_pv.time_temp_hoch.cumsum()

            df_pv['amperestunden'] = (df_pv['current_mean']*df_pv['relativeTime_amax'])/3600
            #mapply(trapz,refDisSteps$relativeTime,refDisSteps$current)/3600

            df_pv_filtered = df_pv[df_pv['comment_'] == 'reference discharge']


            logging.info(f"<<< Start saving dataframe with shape {df_pv_filtered.shape} >>>")
            df_pv.to_csv(f"{folder}\\{new_filename}", sep=',', index=False)
            logging.info(f"<<< Saved processed file in directory {folder}\\{new_filename} >>>")


    d = []

    df_full = pd.DataFrame(d, columns=df_pv_filtered.columns)

    for file in os.listdir(folder):
        if ".csv" in file:
            df = pd.read_csv(f"{folder}\\{file}")
            df_full = df_full.append(df)
    df_full = df_full.reset_index()


    var_auswahl = [
        "batteryname_",
        "amperestunden",
        "zyklus_",
        "comment_",
        "type_",
        "temperature_amax",
        "temperature_amin",
        "temperature_mean",
        "time_amin",
        "time_entladen_stark_vorher",
        "time_entladen_leicht_vorher",
        "time_laden_stark_vorher",
        "time_pause_vorher",
        "time_temp_hoch",
        "time_temp_hoch_vorher"
    ]

    df_final = df_full[var_auswahl]
    df_final.to_csv(f"{folder_final}\\df_fertige_features.csv", sep=',', index=False)
    df_final