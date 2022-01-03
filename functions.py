# coding=utf8
import sys
import os
import pandas as pd

def get_folder():
    """
    Holt den Projekt Ordner Namen und meldet ihn zurück,
    unabhängig ob von Notebook oder Python file ausgeführt.
    """
    return os.path.dirname(os.path.abspath(__file__))



def csv_einlesen(p_fold):
    """
    liest alle CSV dateien aus dem angegebenen Ordner aus und fügt diese in ein dataframe zusammen.
    Das entstehende Dataframe wird zurückgemeldet.
    """
    counter = 0
    for file in os.listdir(p_fold):
        if '.csv' in file and counter == 0:
            df = pd.read_csv(f"{p_fold}\\{file}", index_col = 0)
            counter += 1
            print('Einlesen von ', file, ' erfolgreich')
        elif '.csv' in file: 
            tempdf = pd.read_csv(f"{p_fold}\\{file}", index_col = 0)
            counter+= 1
            df = df.append(tempdf, ignore_index=True)
            print('Einlesen von ', file, ' erfolgreich')
    return df


# Where to save the figures
wdir = "."
fig_path = os.path.join(wdir, "images")
os.makedirs(fig_path, exist_ok=True)
data_path = os.path.join(wdir, "data")
os.makedirs(data_path, exist_ok=True)

def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join(fig_path, fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)