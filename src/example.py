#######################################################
## ------------------------------------------------- ##
## LIBF Fintech Society - Robofunds Competition 2024 ##
## ------------------------------------------------- ##
#######################################################
##  -----------------------------------------------  ##
##  This is the Example file, this file will not be  ##
##  tested and all code should be in __main__.py     ##
##  This file is to show how to use the trading api. ##
##  -----------------------------------------------  ##
#######################################################

from trading_api import *
import datetime
from dateutil.relativedelta import relativedelta
import yfinance
import pandas as pd

def trade(account, market_data, recursive_data=None):
    """This is the function that is going to be tested and needs to output the trades to be made"""

    msft_asset = asset("MSFT",110, "buy",10)
    msft_call = optionContract(msft_asset, "call", 120, account.date + relativedelta(months=+3), 0.2, account.risk_Free)
    order = (msft_call)

    return order, recursive_data


if __name__ == "__main__":
    # This if statement is required, all code to run and test the function must be located under here
    # It is also good practice to move the code below into it's own function but its not necessary

    # Initialise the portfolio and variables for trade function
    portfolio_1 = portfolio(1000)
    recursive_data = None
    market_data = [None] * 3

    # send trade history into function
    for index, day in enumerate(market_data):
        orders, recursive_data = trade(portfolio_1, market_data[:index], recursive_data)

        portfolio_1.process_Orders(orders)
        portfolio.date += relativedelta(months=1)

    print(portfolio_1.open_Positions)
