from y2p import yield_to_price
from p2y import price_to_yield
from risk import risk
import datetime as dt

# Testing yield to price and price to yield
def test1():
  stl = dt.datetime(2008, 2, 15)
  mat = dt.datetime(2017, 11, 15)
  cpn = 5.75
  yld = 6.5
  face_val = 100
  freq = 2
  basis = 1

  price, dpdy = yield_to_price(stl, mat, cpn, yld, face_val, freq, basis)
  print(f"Test 1 Output: This yield has a price of {price} and rate of change of {dpdy} w.r.t yield")

  y = price_to_yield(stl, mat, cpn, price, face_val, freq, basis)
  print(y)

# Testing estimations of duration: dp/dy vs estimation using change in yield
def test2():
  stl = dt.datetime(2008, 2, 15)
  mat = dt.datetime(2017, 11, 15)
  cpn = 5.75
  yld = 6.5
  face_val = 100
  freq = 2
  basis = 1

  pv1, dpdy1 = yield_to_price(stl, mat, cpn, yld, face_val, freq, basis)
  pv2, dpdy2 = yield_to_price(stl, mat, cpn, yld + 0.01, face_val, freq, basis)
  print(f"Test 2 Output: This should be close to equal {(pv2 - pv1) *100} and {dpdy1}")

# Testing on bond
def test3():
  stl = dt.datetime(2024, 4, 25)
  mat = dt.datetime(2033, 2, 15)
  cpn = 3.5
  yld = 4.67
  face_val = 100
  freq = 2
  basis = 1

  price, dpdy = yield_to_price(stl, mat, cpn, yld, face_val, freq, basis)
  dpdy_calc, dpdy_autograd, mdur, convexity = risk(stl, mat, cpn, yld, face_val, freq, basis)

  print(f"Test 3 Output: This should be close to equal {dpdy_calc} and {dpdy_autograd}")
  print(f"Based on a yield of {yld}, the price is {price}")
  print(f"And duration and convenxity values are {mdur} and {convexity}, respectively")

def test4():
  stl = dt.datetime(2024, 4, 25)
  mat = dt.datetime(2033, 2, 15)
  cpn = 3.5
  face_val = 100
  freq = 2
  basis = 1

  y = price_to_yield(stl, mat, cpn, 100, face_val, freq, basis)
  print(y)

test3()