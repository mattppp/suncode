#!/usr/bin/env python3

import pandas as pd

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

def add_cols(data_df, source_dict, key):
    data_new = data_df
    columns = data_new.columns.tolist()
    sample_key = data_new.get_value(0, key)
    #if sample_key

    print(sample_key)
    for c in source_dict[sample_key].keys():
        if c not in columns:
            data_new[c] = 0
            columns.append([c])

    for i in range(len(data_new['JobId'])):
        k = data_new.get_value(i, key)
        for c in source_dict[k].keys():
            data_new.set_value(i, c, source_dict[k][c])

    return data_new

data_installed = pd.read_csv('data/PV_installed_customer_details.csv', sep=',', encoding='ISO-8859-1')
data_cancelled = pd.read_csv('data/PV_cancelled_customer_details.csv', sep=',', encoding='ISO-8859-1')

factors = [
    'JobId',
    'EngineeringSoldkWSize',
    'EngineeringSoldAnnualkWh',
    'EnergyConsumption',
#    'Region',
    'State',
#    'Zip',
#    'Latitude',
#    'Longitude',
#    'AHJ',
#    'RoofType',
    'RoofSqFoot',
    'NumMountingPlanes',
    'NumPanels',
#    'Utility',
#    'ProductTypeAlt',
    'PowerwallCount',
    'UtilityCostPerKWh',
    'OldBill',
    'UtilityRatePlanId',
    'UtilityInflationRate',
    'GasRatePlanID',
    'AverageShading',
    'Reroof',
    'MPU',
#    'NumStories',
]

data_installed = data_installed[factors]
data_cancelled = data_installed[factors]
data_installed['Status'] = 1
data_cancelled['Status'] = 0
data_combined = data_installed.append(data_cancelled)

data_sunlight = pd.read_csv('data/Google Sunroof_Yearly_Sunlight_by_State.csv', sep=',', encoding='ISO-8859-1')
data_sunlight = read_as_dict(data_df=data_sunlight, key='State')

#TODO DELETE
#data_combined = data_combined.head(n=len(data_combined))
data_combined = data_combined.head(n=9714)

data_combined = add_cols(data_df=data_combined, source_dict=data_sunlight, key='State')

#print(data_combined.head(n=5))


# for row in range(len(data_combined['JobId'])):
#     
#     state_row = list(data_sunlight['State']).index(state)
#     data_combined['yearly_sunlight_kwh_kw_threshold_avg'][row] = data_sunlight['yearly_sunlight_kwh_kw_threshold_avg'][state_row]

# print(data_combined.head(n=5))

data_out = data_combined.head(n=100).append(data_combined.tail(n=100))
data_out.to_csv('data_combined_truncated.csv', sep=',')
data_combined.to_csv('data_combined.csv',sep=',')
