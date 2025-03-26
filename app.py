from flask import Flask, render_template, request, jsonify
from y2p import yield_to_price
from p2y import price_to_yield
from risk import risk
import datetime as dt

app = Flask(__name__)

def convertCouponFreq(cpnString):
    cpn = 0
    if cpnString == 'annual':
        cpn = 1
    elif cpnString == 'semiannual':
        cpn = 2
    elif cpnString == 'quarterly':
        cpn = 4
    elif cpnString == 'monthly':
        cpn = 12
    else:
        cpn = 2
    return cpn  

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# API endpoint to update price from yield
@app.route('/update_price', methods=['POST'])
def update_price():
    data = request.get_json()
    yld_val = float(data['input'])

    face_val = float(data['face'])
    stl = dt.datetime.strptime(data['settlement'], "%Y-%m-%d")
    mat = dt.datetime.strptime(data['maturity'], "%Y-%m-%d")
    cpn = float(data['coupon'])
    freq = convertCouponFreq(data['freq'])
    # basis = convertDCC(data['dcc'])
    basis = 1

    price, dpdy = yield_to_price(stl, mat, cpn, yld_val, face_val, freq, basis)
    return jsonify({"price" : price, "dpdy" : dpdy})

# API endpoint to update yield from price
@app.route('/update_yield', methods=['POST'])
def update_yield():
    data = request.get_json()
    price_val = float(data['input'])
    
    face_val = float(data['face'])
    stl = dt.datetime.strptime(data['settlement'], "%Y-%m-%d")
    mat = dt.datetime.strptime(data['maturity'], "%Y-%m-%d")
    cpn = float(data['coupon'])
    freq = convertCouponFreq(data['freq'])
    # basis = convertDCC(data['dcc'])
    basis = 1

    y = price_to_yield(stl, mat, cpn, price_val, face_val, freq, basis)
    return jsonify({"yield" : y})

# API endpoint to update risk metrics
@app.route('/update_risk', methods=['POST'])
def update_risk():
    data = request.get_json()
    yld = float(data['yield'])
    face_val = float(data['face'])
    stl = dt.datetime.strptime(data['settlement'], "%Y-%m-%d")
    mat = dt.datetime.strptime(data['maturity'], "%Y-%m-%d")
    cpn = float(data['coupon'])
    freq = convertCouponFreq(data['freq'])
    basis = 1     # basis = convertDCC(data['dcc'])

    dpdy_calc, dpdy_autograd, mdur, convexity = risk(stl, mat, cpn, yld, face_val, freq, basis)
    return jsonify({
        "dpdy_calc" : dpdy_calc,    
        "dpdy_autograd" : dpdy_autograd,
        "mdur" : mdur,
        "convexity" : convexity
    })