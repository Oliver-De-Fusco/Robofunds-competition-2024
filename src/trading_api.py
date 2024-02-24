#####################################################
## ----------------------------------------------- ##
## LIBF Fintech Society Robofunds Competition 2024 ##
## ----------------------------------------------- ##
#####################################################

import datetime
import numpy
from collections import defaultdict
from dataclasses import dataclass 

WHITELIST = ("MSFT")

class portfolio:
    date = datetime.datetime.now()

    def __init__(self, balance) -> None:
        self.positions = defaultdict(lambda :{"position" : 0, "contracts" : defaultdict(int)})
        self.balance = balance
        self.trade_history = []

    def buy(self, order, quantity):
        if isinstance(order, optionContract):
            # Add option contract to open position
            order.side = "buy"
            if order in self.positions[order.asset]["contracts"]:
                self.positions[order.asset]["contracts"][order] += quantity
            else:
                self.positions[order.asset]["contracts"][order] += quantity


        else:
            # Buy asset immediately
            self.positions[order.asset]["position"] += quantity
            self.trade_history.append(order)
        
        self.balance -= order.cost * quantity

    def sell(self, order, quantity):
        if isinstance(order, optionContract):
            # Add option contract to open position
            order.side = "sell"
            self.positions[order.asset]["contracts"][order] -= quantity


        else:
            # Sell asset immediately
            self.positions[order.asset]["position"] -= quantity
            self.trade_history.append(order)
        
        self.balance += order.cost * quantity

    def execute_option_contract(self, contract, spot):
        """Executes a given contract"""
        if not isinstance(contract, optionContract):
            raise TypeError("Contract must be option class.")

        if contract.expiry != portfolio.date:
            # European options cannot be excerised early.
            self.positions[contract.asset.buy]["contracts"].remove(
                contract)
            return False

        revenue = contract.value(spot)

        if contract.side == "sell":
            proft *= -1

        self.positions[contract.asset.buy]["contracts"].remove(contract)
        self.positions[contract.asset.buy]["balance"] += revenue
        self.trade_history.append(contract)

        return revenue


@dataclass(frozen=True, eq=True)
class asset:
    asset: str
    cost: float


class optionContract:
    def __init__(self, asset, strike, cost, expiry, type)  -> None:
        """
        Using option contracts allow for hedging and strategies to be implemented.

        Costs are in USD
        """
        self.asset = asset
        self.strike = strike
        self.cost = cost
        self.side = None

        if isinstance(expiry, datetime.datetime):
            self.expiry = expiry
        else:
            raise TypeError("Expiry must be a datetime object.")

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
