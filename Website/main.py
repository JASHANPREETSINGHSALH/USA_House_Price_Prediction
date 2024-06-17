# flask, scikit-learn, pandas, joblib
import pandas as pd
from flask import Flask, render_template, request
from joblib import load
import numpy as np


app = Flask(__name__)

# Load the cleaned dataset
data = pd.read_csv('Cleaned_data.csv')

model = load('model.joblib')


@app.route('/')
def index():
    # Get unique locations from the dataset
    locations = sorted(data['state'].unique())
    return render_template('index.html', locations=locations)


@app.route('/predict', methods=['POST'])
def predict():
    # Get input parameters from the form submission
    location = request.form.get('location')
    beds = float(request.form.get('beds'))
    bath = float(request.form.get('bath'))
    sqft = float(request.form.get('total_sqft'))
    state_mapping = {
        'Connecticut': 0,
        'Delaware': 1,
        'Maine': 2,
        'Massachusetts': 3,
        'New Hampshire': 4,
        'New Jersey': 5,
        'New York': 6,
        'Pennsylvania': 7,
        'Puerto Rico': 8,
        'Rhode Island': 9,
        'Vermont': 10,
        'Virgin Islands': 11
    }
    state_id = state_mapping[location]
    input_data=[[beds,bath,sqft,state_id]]
    prediction = model.predict(input_data)
    predictions_str = np.round(prediction[0]).astype(str)
    return predictions_str


if __name__ == "__main__":
    app.run(debug=True)
