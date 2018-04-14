#!/usr/bin/env python3

import pandas as pd
import numpy as np

def read_as_dict(data_df, key):
    keys = data_df[key]
    columns = data_df.columns.tolist()
    d = {}

    for i in range(len(keys)):
        d[keys[i]] = {}
        for c in columns:
            if c != key:
                d[keys[i]][c] = data_df[c][i]

    return d

def add_cols(data_df, source_dict, key, new_columns):
    data_new = data_df
    columns = data_new.columns.tolist()

    sample_key = data_new.get_value(0, key)
    if not isinstance(sample_key, str):
        sample_key = sample_key[0]

    for c in new_columns:
        data_new[c] = np.nan
        columns.append([c])

    for i in range(len(data_new['JobId'])):

        if i % 5000 == 0:
            print(i)

        k = data_new.get_value(i, key)
        if not isinstance(k, str) and not isinstance(k, float) and not isinstance(k, int):
            k = k[0]

        try:
            if key == 'Zip':
                k = int(k)
            for c in source_dict[k].keys():
                data_new.set_value(i, c, source_dict[k][c])
        except:
            continue

    return data_new

data_installed = pd.read_csv('data/PV_installed_customer_details.csv', sep=',', encoding='ISO-8859-1', low_memory=False)
data_cancelled = pd.read_csv('data/PV_cancelled_customer_details.csv', sep=',', encoding='ISO-8859-1', low_memory=False)

factors = [
    'JobId',
    'EngineeringSoldkWSize',
    'EngineeringSoldAnnualkWh',
    'EnergyConsumption',
    'Region',
    'State',
    'Zip',
#    'Latitude',
#    'Longitude',
    'AHJ',
    'RoofType',
    'RoofSqFoot',
    'NumMountingPlanes',
    'NumPanels',
    'Utility',
    'ProductTypeAlt',
    'PowerwallCount',
    'UtilityCostPerKWh',
    'OldBill',
    'UtilityRatePlanId',
    'UtilityInflationRate',
    'GasRatePlanID',
    'AverageShading',
#    'Reroof',
#    'MPU',
    'NumStories',
]

data_installed = data_installed[factors]
data_cancelled = data_installed[factors]
data_installed['Status'] = 1
data_cancelled['Status'] = 0
data_combined = data_installed.append(data_cancelled)

#TODO DELETE
#data_combined = data_combined.head(n=len(data_combined))
data_sample = data_combined.head(n=10000).append(data_combined.tail(n=10000), ignore_index=True)


data_sunlight = pd.read_csv('data/Google Sunroof_Yearly_Sunlight_by_State.csv', sep=',', encoding='ISO-8859-1', low_memory=False)
data_sunlight = read_as_dict(data_df=data_sunlight, key='State')
data_sample = add_cols(data_df=data_sample, source_dict=data_sunlight, key='State', new_columns=[
    'yearly_sunlight_kwh_kw_threshold_avg',
    'yearly_sunlight_kwh_n',
    'yearly_sunlight_kwh_s',
    'yearly_sunlight_kwh_e',
    'yearly_sunlight_kwh_w',
    'yearly_sunlight_kwh_f',
    'yearly_sunlight_kwh_median',
    'yearly_sunlight_kwh_total',
])

data_insolation = pd.read_csv('data/Insolation_by_Zip.csv', sep=',', encoding='ISO-8859-1', low_memory=False)
data_insolation = read_as_dict(data_df=data_insolation, key='Zip')
data_sample = add_cols(data_df=data_sample, source_dict=data_insolation, key='Zip', new_columns=[
    'Insolation',
])

# data_census = pd.read_csv('data/CensusZIP.csv', sep=',', encoding='ISO-8859-1', low_memory=False)
# data_census = read_as_dict(data_df=data_census, key='Zip')
# data_sample = add_cols(data_df=data_sample, source_dict=data_census, key='Zip', new_columns=[
#     'Avg.Age',
#     'Median.Income',
# ])


print(data_sample.head(n=5))


# Printing
data_sample = data_combined.head(n=10000).append(data_combined.tail(n=10000))
data_sample.to_csv('data_v2_sample.csv', sep=',')
data_combined.to_csv('data_v2_full.csv',sep=',')
