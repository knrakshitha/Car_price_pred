from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        car_age = int(request.form['Year'])
        seats=float(request.form['seats'])
        km_driven=int(request.form['km_driven'])
        km_driven2=np.log(km_driven)
        Owner=request.form['Owner']
        if(Owner=='1'):
            o_4=0
            o_3=0
            o_2=0
            tc=0
        elif(Owner=='2'):
            o_4=0
            o_3=0
            o_2=1
            tc=0
        elif(Owner=='3'):
            o_4=0
            o_3=1
            o_2=0
            tc=0
        elif(Owner=='4 and above'):
            o_4=1
            o_3=0
            o_2=0
            tc=0
        else:
            o_4=0
            o_3=0
            o_2=0
            tc=1
        Fuel_Type_Petrol=request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
                Fuel_Type_LPG=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
            Fuel_Tyoe_LPG=0
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
            Fuel_Type_LPG=1
        car_age=2021-car_age
        Seller_Type_Individual=request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
            Seller_Type_Dealer=0
        else:
            Seller_Type_Individual=0
            Seller_Type_Dealer=1	
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        prediction=model.predict([[km_driven2,seats,car_age,Fuel_Type_Diesel,Fuel_Type_LPG,Fuel_Type_Petrol,Seller_Type_Individual,Seller_Type_Dealer,Transmission_Mannual, o_4, o_2, tc, o_3]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)