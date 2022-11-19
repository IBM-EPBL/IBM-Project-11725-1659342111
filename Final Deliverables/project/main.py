from flask import Flask, render_template, request
import requests
import json
import os
from os.path import normpath as norm
import pandas as pd
from babel.numbers import format_currency
# import pickle
# model = pickle.load(open(norm(os.getcwd()+'/reg_model.pkl'),'rb'))

api = json.load(open('apikey.json'))
API_KEY = api['apikey']
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', 
                               data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)

@app.route('/')
def home():
    with open(norm(os.getcwd()+'/Mapping_details.json'), 'r') as f:
        data = json.load(f)
    car_company = list(data['company'].keys())
    return render_template('main.html', car_company=sorted(car_company[:-1])+[car_company[-1]],
                                        seller_type = sorted(list(data['seller_type'].keys())),
                                        fuel_types = sorted(list(data['fuel_type'].keys())),
                                        transmission_type = sorted(list(data['transmission_type'].keys())),)

@app.route('/main', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            with open(norm(os.getcwd()+'/Mapping_details.json'), 'r') as f:
                data = json.load(f)
            company = data['company'][request.form.get('company')]
            fuel_type = data['fuel_type'][request.form.get('fuel_type')]
            seller_type = data['seller_type'][request.form.get('seller_type')]
            transmission_type = data['transmission_type'][request.form.get('transmission_type')]
            test_dict = {
                'year' : int(request.form.get('year')),
                'km_driven' : int(request.form.get('km_driven')),
                'mileage' : float(request.form.get('mileage')),
                'engine' : float(request.form.get('engine')),
                'max_power': float(request.form.get('max_power')),
                'seats' : int(request.form.get('seats')),
                'seller_type_Individual': seller_type[0],
                'seller_type_Trustmark Dealer': seller_type[1],
                'fuel_type_Diesel': fuel_type[0],
                'fuel_type_Electric': fuel_type[1],
                'fuel_type_LPG': fuel_type[2],
                'fuel_type_Petrol': fuel_type[3],
                'transmission_type_Manual': transmission_type[0],
                'company_BMW': company[0],
                'company_Chevrolet': company[1], 
                'company_Ford': company[2], 
                'company_Honda': company[3], 
                'company_Hyundai': company[4],
                'company_Mahindra': company[5], 
                'company_Maruti': company[6], 
                'company_Mercedes-Benz': company[7],
                'company_Nissan': company[8], 
                'company_Renault': company[9], 
                'company_Skoda': company[10], 
                'company_Tata': company[11],
                'company_Toyota': company[12], 
                'company_Volkswagen': company[13], 
                'company_others': company[14],
            }
            array_of_input_fields = list(test_dict.keys())
            array_of_values_to_be_scored = list(test_dict.values())
            payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored]}]}
            response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2c6a0497-ed41-4976-857e-a9ce6ef2fa18/predictions?version=2022-11-18', 
                                             json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
            
            try:
                prediction = response_scoring.json()
                price = format_currency(int(prediction['predictions'][0]['values'][0][0]),'INR',locale='en_IN')
                # output = model.predict(pd.DataFrame(test_dict,index=[0]))
                # output = format_currency(output[0],'INR', locale='en_IN')
                car_name = request.form.get('car_name')
                car_year = int(request.form.get('year'))
            except Exception as e:
                price = None
                print("Error while predicting output ", e)
            return render_template('output.html', 
                                    prediction = price, car_name =request.form.get('company')+" "+car_name,
                                    car_year=car_year )
        except Exception as e:
            print(e)
            return "Error while receiving data...."
    else: 
        print(" in else POST")
        return render_template('/')


if __name__ == '__main__':
    app.run(debug=True)

# setx FLASK_APP "main.py"
# flask run