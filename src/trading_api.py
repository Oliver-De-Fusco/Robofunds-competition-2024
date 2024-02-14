#####################################################
## ----------------------------------------------- ##
## LIBF Fintech Society Robofunds Competition 2024 ##
## ----------------------------------------------- ##
#####################################################

import datetime
import numpy

WHITELIST = ("GBP", "USD", "EUR", "AUD", "CNY", "JPY")


class portfolio:
    date = datetime.datetime.now()

    def __init__(self) -> None:
        self.positions = {currency: {"balance": 0, "contracts": []}
                          for currency in WHITELIST}
        self.trade_history = []

    def buy(self, order):
        if isinstance(order, option):
            # Add to open positions
            order.side = "buy"
            self.positions[order.underlying.buy]["contracts"].append(order)
            self.positions["USD"]["balance"] -= order.cost * order.quantity

        elif isinstance(order, currency_pair):
            # Adjust balances accordingly
            if order.rate is not None:

                self.positions[order.buy]["balance"] += round(
                    (1 / order.rate) * order.quantity, 4)
                self.positions[order.sell]["balance"] -= round(
                    order.quantity, 4)
                self.trade_history.append(order)
            else:
                raise TypeError("rate not found")

    def sell(self, order):
        if isinstance(order, option):
            order.side = "sell"
            self.positions[order.underlying.sell]["contracts"].append(order)
            self.positions["USD"]["balance"] += order.cost * order.quantity

        elif isinstance(order, currency_pair):
            # Adjust balances accordingly
            self.positions[order.sell]["balance"] += round(order.quantity, 4)
            self.positions[order.buy]["balance"] -= round(
                (1 / order.rate) * order.quantity, 4)

            self.trade_history.append(order)

    def execute_option_contract(self, contract, spot):
        """Executes a given contract"""
        if not isinstance(contract, option):
            raise TypeError("Contract must be option class.")

        if contract.expiry < portfolio.date:
            # contract has expired and cannot be excersied.
            self.positions[contract.underlying.buy]["contracts"].remove(
                contract)
            return False

        revenue = contract.value(spot)

        if contract.side == "sell":
            proft *= -1

        self.positions[contract.underlying.buy]["contracts"].remove(contract)
        self.positions[contract.underlying.buy]["balance"] += revenue
        self.trade_history.append(contract)

        return revenue


class currency_pair:
    def __init__(self, buy, sell, quantity, rate=None) -> None:
        """Currency pair is used to establish the underlying trade.

        Consider it like a form that requires specific information.

        rate in terms of sell/buy=X

        quantity is in terms of currency being sold.
        """
        if buy in WHITELIST and sell in WHITELIST:
            if buy != sell:
                self.buy = buy
                self.sell = sell
            else:
                raise Exception("Buy and sell cannot be the same currency.")
        else:
            raise Exception("Invalid Currency.")

        if isinstance(rate, (numpy.float64, float)):
            self.rate = rate
        else:
            raise TypeError("Rate must be float or numpy.float64")

        if isinstance(quantity, int):
            self.quantity = quantity
        else:
            raise TypeError("Quantity must be int.")


class option:
    def __init__(self, underlying, strike, cost, expiry, type) -> None:
        """
        Using option contracts allow for hedging and strategies to be implemented.

        Costs are in USD
        """

        if isinstance(underlying, currency_pair):
            self.underlying = underlying
        else:
            raise TypeError("Underlying must be a currency pair class.")

        self.strike = strike
        self.quantity = underlying.quantity
        self.cost = cost
        self.side = None

        if isinstance(expiry, datetime.datetime):
            self.expiry = expiry
        else:
            raise TypeError("Expiry must be a datetime.")

        if type.lower() in ["call", "put"]:
            self.type = type.lower()
        else:
            raise ValueError("Incorrect option type.")

    def value(self, spot):
        """Value when executed at given spot price"""

        if self.type == "call":
            revenue = max(spot - self.strike, 0) * self.quantity
        else:
            # put
            revenue = max(self.strike - spot, 0) * self.quantity

        return revenue

    def __repr__(self) -> str:
        return f"option({self.underlying.buy}/{self.underlying.sell}, strike={self.strike}, cost={self.cost}, 'expiry':{self.expiry}, {self.type}, {self.quantity})"
