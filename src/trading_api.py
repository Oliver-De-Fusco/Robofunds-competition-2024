#######################################################
## ------------------------------------------------- ##
## LIBF Fintech Society - Robofunds Competition 2024 ##
## ------------------------------------------------- ##
#######################################################

import datetime
from dateutil.relativedelta import relativedelta
import numpy
import scipy.stats as stats
import math
from collections import defaultdict
from dataclasses import dataclass


class portfolio:
    date = datetime.datetime.now()
    risk_Free = 0.05

    def __init__(self, balance) -> None:
        # Keeps track of the amount of shares of an asset currently owned
        self.positions = defaultdict(int)
        # open positions is a list of tuples: [(contract, price per contract)]
        self.open_Positions = []
        # Balance in USD
        self.balance = balance

    def process_Orders(self, *orders):
        for order in orders:
            if isinstance(order, optionContract):
                # Process option contracts
                delta_time = (order.expiry - portfolio.date).days / 255
                price = black_scholes(order, delta_time)
                self.open_Positions.append((order, price))
                balance_Change = order.underlying_Asset.quantity * price

            elif isinstance(order, asset):
                # Process standard buy/sell
                self.positions[order.asset] += order.underlying_Asset.quantity
                balance_Change = order.quantity * price

            if order.underlying_Asset.side == "buy":
                self.balance += balance_Change
            elif order.underlying_Asset.side == "sell":
                self.balance -= balance_Change

    def execute_option_contract(self, contract_Tuple, current_spot):
        """Executes a given contract

        All contracts are settled directly to USD
        """
        contract, price = contract_Tuple

        if not isinstance(contract, optionContract):
            raise TypeError("Option contract not provided")

        if contract.expiry != portfolio.date:
            # All contracts are european and can only be executed on expiry date
            return None

        if contract.type == "call":
            moneyness = max(current_spot - contract.strike, 0) - price
        elif contract.type == "put":
            moneyness = max(contract.strike - current_spot, 0) - price

        if contract.side == "buy":
            balance += moneyness * contract.quantity
        elif contract.side == "sell":
            balance -= moneyness * contract.quantity

        self.open_Positions.remove(contract_Tuple)


# Dataclasses require fields to be filled and be read-only
@dataclass(frozen=True)
class asset:
    asset: str
    spot_Price: float
    side: str
    quantity: int


@dataclass(frozen=True)
class optionContract:

    underlying_Asset: asset
    type: str
    strike: float
    expiry: datetime.datetime
    volatility: float
    # Percentage in decimal form 5% -> 0.05
    risk_Free_Rate: float


def black_scholes(contract_Order, time_to_expiry):
    """Calculates black_scholes equation for options"""

    d_1 = (math.log(contract_Order.underlying_Asset.spot_Price/contract_Order.strike) + (contract_Order.risk_Free_Rate + (contract_Order.volatility)/2)*time_to_expiry)/(math.sqrt(contract_Order.volatility*time_to_expiry))
    d_2 = d_1 - math.sqrt(contract_Order.volatility*time_to_expiry)

    if contract_Order.type == "call":
        expected_value = contract_Order.underlying_Asset.spot_Price * stats.norm.cdf(d_1, 0, 1)
        value_of_not_exercising = contract_Order.strike * math.exp(-contract_Order.risk_Free_Rate * time_to_expiry) * stats.norm.cdf(d_2, 0, 1)
        return expected_value - value_of_not_exercising
    
    elif contract_Order.type == "put":
        expected_value = contract_Order.underlying_Asset.spot_Price * stats.norm.cdf(-d_1, 0, 1)
        value_of_not_exercising = contract_Order.strike * math.exp(-contract_Order.risk_Free_Rate * time_to_expiry) * stats.norm.cdf(-d_2, 0, 1)
        return value_of_not_exercising - expected_value

