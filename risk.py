from autograd import grad # type: ignore
from y2p import yield_to_price

def risk(settlement, maturity, coupon, yld, par_val, freq, basis):
  def g(x):
    price, dpdy = yield_to_price(settlement, maturity, coupon, x, par_val, freq, basis)
    return price
  d_price, dpdy_calc = yield_to_price(settlement, maturity, coupon, yld, par_val, freq, basis)
  dg = grad(g)
  ddg = grad(dg)
  dpdy_autograd = dg(yld)
  mdur = -dpdy_calc/d_price
  convexity = ddg(yld)/d_price
  return dpdy_calc, dpdy_autograd, mdur, convexity
