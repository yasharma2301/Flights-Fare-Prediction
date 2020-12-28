from flask import Flask, render_template, request, redirect
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
model = pickle.load(open("flight_fare_predictions.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictFare', methods = ["GET", "POST"])
def predict():
    if request.method == 'POST':
        d = {}
        detpartureDate = pd.to_datetime(request.form["departure_date"],format="%Y-%m-%dT%H:%M")
        Journey_Day = int(detpartureDate.day)
        Journey_Month = int(detpartureDate.month)

        departureTime = request.form["departure_time"].split(':')
        Dep_Hour = int(departureTime[0])
        Dep_Minute = int(departureTime[1])

        arriavalTime = request.form["arrival_time"].split(':')
        Arrival_Hour = int(arriavalTime[0])
        Arrival_Minute = int(arriavalTime[1])

        Duration_Hours = abs(Arrival_Hour-Dep_Hour)
        Duration_Minutes = abs(Arrival_Minute-Dep_Minute)
        Total_Stops = int(request.form["stops"])

        airline_dict = {
            'Jet_Airways' : 0,
            'IndiGo' : 0,
            'Air_India' : 0,
            'Multiple_carriers' : 0,
            'SpiceJet' : 0,
            'Vistara' : 0,
            'GoAir' : 0,
            'Multiple_carriers_Premium_economy' : 0,
            'Jet_Airways_Business' : 0,
            'Vistara_Premium_economy' : 0,
            'Trujet' : 0 
        }
        airline_dict[str(request.form["airline"])] = 1
        
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Kolkata'):
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0

        elif (Source == 'Mumbai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0

        elif (Source == 'Chennai'):
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1

        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
        
        Source = request.form["Destination"]
        if (Source == 'Cochin'):
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        
        elif (Source == 'Delhi'):
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'New_Delhi'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0

        elif (Source == 'Hyderabad'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0

        elif (Source == 'Kolkata'):
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1

        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        prediction=model.predict([[
            Total_Stops,
            Journey_Day,
            Journey_Month,
            Dep_Hour,
            Dep_Minute,
            Arrival_Hour,
            Arrival_Minute,
            Duration_Hours,
            Duration_Minutes,

            airline_dict['Air_India'],
            airline_dict['GoAir'],
            airline_dict['IndiGo'],
            airline_dict['Jet_Airways'],
            airline_dict['Jet_Airways_Business'],
            airline_dict['Multiple_carriers'],
            airline_dict['Multiple_carriers_Premium_economy'],
            airline_dict['SpiceJet'],
            airline_dict['Trujet'],
            airline_dict['Vistara'],
            airline_dict['Vistara_Premium_economy'],

            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,

            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        flight_fare =  str(round(prediction[0],2))
        return render_template('index.html',fare="Predicted flight price: ₹ {}".format(flight_fare))

if __name__ == "__main__":
    app.debug = True
    app.run()
