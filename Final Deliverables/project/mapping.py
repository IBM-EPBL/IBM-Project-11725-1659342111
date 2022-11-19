import pandas as pd
import os
from os.path import normpath as norm
import json

json_dict = {}
df1 = pd.read_csv(norm(os.getcwd()+"/project/before.csv"))
df2 = pd.read_csv(norm(os.getcwd()+"/project/after.csv"))
df1_col = df1.columns
df2_col = df2.columns

company_dict = {}
for company in df1['company'].unique():
    unique_company = (df1.loc[df1['company'] == company].iloc[0]).to_frame().T
    idx = int(pd.to_numeric(unique_company['Unnamed: 0']))
    try:unique_df2_company = (df2.loc[df2['Unnamed: 0']==idx].iloc[0]).to_frame().T
    except:continue
    num_array = unique_df2_company[['company_BMW', 'company_Chevrolet', 'company_Ford', 'company_Honda', 'company_Hyundai',
                                    'company_Mahindra', 'company_Maruti', 'company_Mercedes-Benz', 'company_Nissan', 
                                    'company_Renault', 'company_Skoda', 'company_Tata', 'company_Toyota', 'company_Volkswagen', 
                                    'company_others']].values
    company_dict[company]=list(map(int,num_array[0]))
json_dict['company']=company_dict

fuel_dict = {}
for fuel in df1['fuel_type'].unique():
    unique_fuel = (df1.loc[df1['fuel_type'] == fuel].iloc[0]).to_frame().T
    idx = int(pd.to_numeric(unique_fuel['Unnamed: 0']))
    try:unique_df2_fuel = (df2.loc[df2['Unnamed: 0']==idx].iloc[0]).to_frame().T
    except:continue
    num_array = unique_df2_fuel[['fuel_type_Diesel', 'fuel_type_Electric', 'fuel_type_LPG','fuel_type_Petrol']].values
    fuel_dict[fuel]=list(map(int,num_array[0]))
json_dict['fuel_type']=fuel_dict

seller_dict = {}
for seller in df1['seller_type'].unique():
    unique_seller = (df1.loc[df1['seller_type'] == seller].iloc[0]).to_frame().T
    idx = int(pd.to_numeric(unique_seller['Unnamed: 0']))
    try:unique_df2_seller = (df2.loc[df2['Unnamed: 0']==idx].iloc[0]).to_frame().T
    except:continue
    num_array = unique_df2_seller[['seller_type_Individual', 'seller_type_Trustmark Dealer']].values
    seller_dict[seller]=list(map(int,num_array[0]))
json_dict['seller_type']=seller_dict

transmission_dict = {}
for transmission in df1['transmission_type'].unique():
    unique_transmission = (df1.loc[df1['transmission_type'] == transmission].iloc[0]).to_frame().T
    idx = int(pd.to_numeric(unique_transmission['Unnamed: 0']))
    try:unique_df2_transmission = (df2.loc[df2['Unnamed: 0']==idx].iloc[0]).to_frame().T
    except:continue
    num_array = unique_df2_transmission[['transmission_type_Manual']].values
    transmission_dict[transmission]=list(map(int,num_array[0]))
json_dict['transmission_type']=transmission_dict

with open('Mapping_details.json', 'w', encoding ='utf8') as json_file:
    json.dump(json_dict, json_file)
