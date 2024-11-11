from flask import Flask, render_template, request, redirect, flash
import pickle
import numpy as np
import os

# Ensure the correct file path and name
filename = 'first-innings-score-model.pkl'
# Alternatively, use an absolute path if the file is in a different directory
# filename = '/path/to/your/file/first-innings-score-model.pkl'

# Check if the file exists
if not os.path.exists(filename):
    raise FileNotFoundError(f"Model file {filename} not found. Ensure the file is in the correct directory.")

with open(filename, 'rb') as file:
    regressor = pickle.load(file)

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        temp_array = list()
        batting_team = request.form['batting-team']
            
        if batting_team == 'Chennai Super Kings':
            temp_array += [1, 0, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Delhi Daredevils':
            temp_array += [0, 1, 0, 0, 0, 0, 0, 0]
        elif batting_team == 'Kings XI Punjab':
            temp_array += [0, 0, 1, 0, 0, 0, 0, 0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array += [0, 0, 0, 1, 0, 0, 0, 0]
        elif batting_team == 'Mumbai Indians':
            temp_array += [0, 0, 0, 0, 1, 0, 0, 0]
        elif batting_team == 'Rajasthan Royals':
            temp_array += [0, 0, 0, 0, 0, 1, 0, 0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array += [0, 0, 0, 0, 0, 0, 1, 0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array += [0, 0, 0, 0, 0, 0, 0, 1]
        
        bowling_team = request.form['bowling-team']

        if batting_team == bowling_team:
            flash("Same Team Not allowed")
            return redirect('/')

        if bowling_team == 'Chennai Super Kings':
            temp_array += [1, 0, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array += [0, 1, 0, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array += [0, 0, 1, 0, 0, 0, 0, 0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array += [0, 0, 0, 1, 0, 0, 0, 0]
        elif bowling_team == 'Mumbai Indians':
            temp_array += [0, 0, 0, 0, 1, 0, 0, 0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array += [0, 0, 0, 0, 0, 1, 0, 0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array += [0, 0, 0, 0, 0, 0, 1, 0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array += [0, 0, 0, 0, 0, 0, 0, 1]
        
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])

        temp_array += [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5]

        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])

        return render_template('result.html', lower_limit=my_prediction-10, upper_limit=my_prediction+10)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
