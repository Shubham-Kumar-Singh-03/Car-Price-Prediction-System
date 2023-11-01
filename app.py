from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import pickle

model = pickle.load(open('CarPriceModel.pkl', 'rb'))

app = Flask(__name__)

car = pd.read_csv("Cleaned.csv")


@app.route('/')
def index():
    companies = sorted(car["company"].unique())
    car_models = sorted(car["name"].unique())
    year = sorted(car["year"].unique())
    fuel_type = sorted(car["fuel_type"].unique())

    companies.insert(0,'Select Company')
    year.insert(0,'Select Year')
    fuel_type.insert(0,'Select Fuel Type')
    return render_template('index.html', companies=companies, car_models=car_models, years=year, fuel_types=fuel_type)

@app.route('/predict', methods=['POST'])
def predict():
    company=request.form.get('company')
    car_model=request.form.get('car_models')
    year=request.form.get('year')
    fuel_type=request.form.get('fuel_type')
    driven=int(request.form.get('kilo_driven'))

    

    prediction=model.predict(pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'],
                              data=np.array([car_model,company,year,driven,fuel_type]).reshape(1, 5)))

    return str(np.round(prediction[0],2))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')