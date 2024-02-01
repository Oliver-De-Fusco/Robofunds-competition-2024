import datetime

class portfolio:
    def __init__(self, start_balance) -> None:
        self.balance = start_balance
        self.positions = [""]
        self.trade_history = []
    
    
    def buy(self, asset, type):
        self.


    def sell(self):
        pass



class asset:
    def __init__(self, asset, price) -> None:
        self.asset = asset
        self.price = price


class option:
    def __init__(self, strike, cost, expiry, type, side) -> None:

        self.strike = strike
        self.cost = cost

        if isinstance(expiry, datetime.datetime):
            self.expiry = expiry
        else: raise TypeError("Inappropriate argument type.")

        if type.lower() in ["call", "put"]:
            self.type = type.lower()
        else: raise ValueError("Incorrect option type.")

        if side.lower() in ["buy", "sell"]:
            self.side = side.lower()
        else: raise ValueError("Incorrect buy/sell side.")