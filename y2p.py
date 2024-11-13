from dateutil.relativedelta import relativedelta # type: ignore
import datetime as dt

def yield_to_price(settlement, maturity, coupon, yld, par_val, freq, basis):
  dates = []
  d = maturity
  step = 12/freq

  while d > settlement:
    dates.append(d)
    d = d + relativedelta(months=-step)
  dates.append(d) # add the settlement or pre-settlement date
  dates.sort()
  #print(dates)

  cpn_per_period = coupon/100/freq # adjusted for each period
  yld_per_period = yld/100/freq # adjusted for each period

  dpdy = 0
  ddf = 0
  n = 365 # to only be used for first period
  sum = 0
  weighted_time = 0
  lcd = dates[0]

  for i in range(len(dates)):
    if dates[i] <= settlement:
      lcd = dates[i]
      continue
    ncd = dates[i]

    if basis == 1: # Act/Act Convention

      if lcd > settlement: # a normal period
        weighted_period = 1
      else: # for the first smaller period
        weighted_period = (ncd - settlement).days/((ncd - lcd).days)

      weighted_time += weighted_period

      cf = cpn_per_period

      if ncd == maturity:
        cf += par_val/100

      df = pow(1+yld_per_period, -weighted_time)
      ddf = - weighted_time * (1 + yld_per_period)**(-weighted_time-1) * (1/freq) # Hand calcualted derivative df/dt
      pv = df * cf
      sum += pv
      dpdy += cf * ddf
      lcd = ncd # Remember last coupoun date

  # adjust for accured interest
  accured_percent = ((settlement - dates[0]).days/(dates[1] - dates[0]).days)
  actual_accured = accured_percent * cpn_per_period

  dirty_price = 100 * (sum - actual_accured) # par_value

  return (dirty_price, dpdy)