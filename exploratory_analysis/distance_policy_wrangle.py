'''
Christi Liongson, Hana Passen, Charmaine Runes, Damini Sharma

Module to clean and wrangle the data from datasets on prison COVID-19 related
social distancing measures into a series of dummy variables at the state level.
'''

import numpy as np
import pandas as pd
import re

POLICIES_KEYWORDS = {"no_volunteers": ["volunteer"],
                     "limiting_movement": ["transfer", "travel", "tour"],
                     "screening" : ["screening", "temperature"],
                     "healthcare_support": ["co-pay"]}

FINAL_FEATURES = ["state", "effective_date", "no_visits", "lawyer_access",
                  "phone_access", "video_access", "no_volunteers", 
                  "limiting_movement", "screening", "healthcare_support"]


def import_clean_data(filepath):
    '''
    Imports a csv file and transforms the column names to snake case,
    transforms any columns related to time to datetime type

    Inputs: 
        - filepath: (str) the string with the filepath for the csv

    Returns: 
        - df: (pandas df) a dataframe with datetime fields and snake_case column
               names
    '''
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.strip("?")
    df.columns = df.columns.str.replace(" ", "_")

    for col in df.columns: 
        if 'date' in col:
            df[col] = pd.to_datetime(df[col])
        if 'time' in col: 
            df[col] = pd.to_datetime(df[col])

    return df


def transform_easy_cols(df, features, new_cols):
    '''
    Takes any columns designed as dummy columns with X values for yes and empty
    cells for no, and creates new dummy columns with 1 and 0

    Inputs:
        - df: (pandas df) the dataframe containing the data
        - features: (lst) list of columns in the data that are set up as dummies
        - new_cols: (lst) list of names for the new dummy columns, in the same
                      order as the columns in features

    Returns: 
        - df: (pandas df) the same dataframe, updated
    '''
    for idx, feature in enumerate(features): 
        new_name = new_cols[idx]
        df[new_name] = df[feature]
        df[new_name].fillna('0', inplace=True)
        df.loc[df[new_name].str.contains('exploring', flags=re.IGNORECASE, 
                                         regex=True), new_name] = '0'
        df.loc[df[new_name].str.contains('X', flags=re.IGNORECASE, regex=True), 
               new_name] = '1'
        df[new_name] = df[new_name].astype(int)

    return df


def encode_policies_str(df, feature, new_dummies=POLICIES_KEYWORDS):
    '''
    Takes summaries of policies and pulls out dummy variables for the social
    distancing policies implemented by each state

    Inputs: 
        - df: (pandas df) the dataframe containing the data
        - feature: (str) column name in the data containing policy summary
                    information
        - new_dummies: (dict) dictionary with key:value pairs of the form
                              newdummycolname:keywords to flag a 1 in that 
                              column, uses the POLICIES_KEYWORDS constant

    Returns: 
        - df: (pandas df) the same dataframe, updated  
    '''
    df[feature].fillna("0", inplace=True)

    for new_dummy in POLICIES_KEYWORDS:
        df[new_dummy] = "0"
        for keyword in POLICIES_KEYWORDS[new_dummy]:
            df.loc[df[feature].str.contains(keyword, flags=re.IGNORECASE, 
                                              regex=True), new_dummy] = '1'
        df[new_dummy] = df[new_dummy].astype(int)

    return df


def select_columns(df, features=FINAL_FEATURES):
    '''
    Returns a dataframe only with cleaned dummy variables and date of policy
    implementation

    Inputs: 
        - df: (pandas df) the dataframe containing the data
        - features: (lst) list of columns that we will then use in our model; 
                     defaults to FINAL_FEATURES constant

    Returns:
        - small_df: (pandas df) the dataframe containing dummy variables and the
                     date of distancing policy implementation by state
    '''
    small_df = df.copy()

    small_df = small_df[features]

    return small_df
    