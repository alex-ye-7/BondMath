from y2p import yield_to_price

def price_to_yield(settlement, maturity, coupon, price, par_val, freq, basis):
  x1 = 0.01
  x2 = 10
  # error function, how close the yield to price prediciton is to the real price
  f1 = yield_to_price(settlement, maturity, coupon, x1, par_val, freq, basis)[0] - price
  while abs(f1) > 1e-6:
    f1 = yield_to_price(settlement, maturity, coupon, x1, par_val, freq, basis)[0] - price
    f2 = yield_to_price(settlement, maturity, coupon, x2, par_val, freq, basis)[0] - price
    temp = x1
    x1 = x1 - (x1 - x2) * f1 / (f1 - f2) # update x1
    x2 = temp
  return x1
