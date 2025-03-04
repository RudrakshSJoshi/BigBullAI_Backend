import random
from Tools.params import fetch_signal_risk
def risk_switcher(tkn_val):
    # 0 = sell, 1 = hold, 2 = buy
    buy, risk = fetch_signal_risk(tkn_val)
    if buy == 1:
        return 2
    else:
        return 0