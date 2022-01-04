"""
Training eines ML Modells zur Prediction
"""
import streamlit as st
import pandas as pd
import numpy as np
import joblib

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

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn import metrics

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

def app():
    st.write("## Training von ML Randomforest")
    c_fold = fu.get_folder()
    folder = c_fold + '\data\Application'
    folder_final = c_fold + '\data\Processed\\final'

    df = pd.read_csv(f"{folder}\\df_feature_importance_data.csv", sep=',')
    st.set_option('deprecation.showPyplotGlobalUse', False)

    train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

    daten = train_set.drop("amperestunden", axis=1)
    daten_labels = train_set["amperestunden"].copy()

    test_daten = train_set.drop("amperestunden", axis=1)
    test_daten_labels = train_set["amperestunden"].copy()
    st.write("=== Train Test Split Performed ===")
    
    if st.button("Start ML Procedures"):
        c_fold = fu.get_folder()
        folder = c_fold + '\data\Application'
        folder_final = c_fold + '\data\Processed\\final'

        df = pd.read_csv(f"{folder}\\df_feature_importance_data.csv", sep=',')
        st.set_option('deprecation.showPyplotGlobalUse', False)

        train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

        daten = train_set.drop("amperestunden", axis=1)
        daten_labels = train_set["amperestunden"].copy()


        test_daten = train_set.drop("amperestunden", axis=1)
        test_daten_labels = train_set["amperestunden"].copy()

        st.write("=== Train Test Split Performed ===")

        num_pipeline = Pipeline([
            ('std_scaler', StandardScaler()), #Warum Standard Scaler? keine Normalverteilung in den Daten
        ])

        num_attribs = list(daten.columns)

        full_pipeline = ColumnTransformer([
                ("num", num_pipeline, num_attribs)
            ])

        daten_tr = full_pipeline.fit_transform(daten)

        st.write("=== Preprocessing Pipeline Executed ===")
        if st.button("Train new Randomforest Model"):
            rfr_pm     = RandomForestRegressor()
            params = {'n_estimators': range(100,1500),
                      'n_jobs':       [-1],
                      'criterion':    ['squared_error','absolute_error'],
                      'max_depth':    range(1,200)
                     }
            k      = 3

            reg_search = RandomizedSearchCV(rfr_pm, params, scoring= 'neg_root_mean_squared_error', cv = k, verbose = 1, n_iter=200)
            reg_search.fit(daten_tr, daten_labels)

            st.write(f"=== Best Parameters found with RandomizedSearchCV: {reg_search.best_params_} ===")

            prepare_and_predict_pipeline = Pipeline([
                ('preparation', full_pipeline),
                ('rfr_reg', reg_search.best_estimator_)
            ])


            joblib.dump(prepare_and_predict_pipeline, f"{folder}\\pickle\\prepare_and_predict_pipeline.pkl")

            st.write("New ML Model trained and saved")

        prepare_and_predict_pipeline_load = joblib.load(f"{folder}\\pickle\\prepare_and_predict_pipeline.pkl")


        st.write(f"=== Predicting with Test Data === ")
        test_daten_pred = prepare_and_predict_pipeline_load.predict(test_daten)
        test_daten_pred_series = pd.Series(test_daten_pred, index=test_daten_labels.index)

        sns.jointplot(x=test_daten_labels,y=test_daten_pred_series, kind='reg')
        st.pyplot()

        st.write("=== Following Performance Metrics for test data on trained model found ===")
        st.write('RMSE:', np.sqrt(metrics.mean_squared_error(test_daten_labels, test_daten_pred_series)))
        st.write('R2:',metrics.r2_score(test_daten_labels, test_daten_pred_series))

        st.write("=== Most Important Features for the ML Model: ===")
        st.write(sorted(zip(prepare_and_predict_pipeline_load['rfr_reg'].feature_importances_, daten.columns), reverse=True))
        
    if st.button("Linear Regression "):
        from sklearn.linear_model import LinearRegression   

        ss = StandardScaler()
        daten_lr = ss.fit_transform(daten) 
        lr = LinearRegression()  
        lr.fit(daten_lr, daten_labels)
        
        coefs = pd.DataFrame(zip(daten.columns, lr.coef_ * np.sqrt(ss.var_) + ss.mean_), columns=["feature","wert"])
        coefs.set_index('feature', inplace=True)
        zeit_coefs = coefs.loc[["time_temp_hoch_vorher","time_laden_leicht_vorher","time_laden_stark_vorher","time_entladen_leicht_vorher","time_entladen_stark_vorher"],["wert"]]
        
        st.write("Wie viele Stunden je Attribut um die Amperestunden um 1 zu reduzieren")
        st.write(zeit_coefs["wert"] / 3600)
        
        zyk_coef = coefs.loc[["zyklus_"],["wert"]]
        st.write("Wie viele vorherige Zyklen müssen durchlaufen werden um die Amperestunde um 1 zu reduzieren")
        st.write(zyk_coef["wert"] )