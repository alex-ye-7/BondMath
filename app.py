from flask import Flask, render_template, request, jsonify
from y2p import yield_to_price
from p2y import price_to_yield
from risk import risk
import datetime as dt

app = Flask(__name__)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to update price from yield
@app.route('/update_price', methods=['POST'])
def update_price():
    data = request.get_json()
    yld_val = float(data['input'])

    stl = dt.datetime(2008, 2, 15)
    mat = dt.datetime(2017, 11, 15)
    cpn = 5.75
    face_val = 100
    freq = 2
    basis = 1

    price, dpdy = yield_to_price(stl, mat, cpn, yld_val, face_val, freq, basis)
    return jsonify({"price" : price, "dpdy" : dpdy})

# API endpoint to update yield from price
@app.route('/update_yield', methods=['POST'])
def update_yield():
    data = request.get_json()
    price_val = float(data['input'])
    
    stl = dt.datetime(2008, 2, 15)
    mat = dt.datetime(2017, 11, 15)
    cpn = 5.75
    face_val = 100
    freq = 2
    basis = 1

    y = price_to_yield(stl, mat, cpn, price_val, face_val, freq, basis)
    return jsonify({"yield" : y})
