#####################################################
## ----------------------------------------------- ##
## LIBF Fintech Society Robofunds Competition 2024 ##
## ----------------------------------------------- ##
#####################################################

from trading_api import *
import datetime
import yfinance
import pandas as pd

def trade(account, market_data, recursive_data=None):

    currency_to_trade = "USD", "GBP"
    # Get current spot price for USD and GBP
    current_spot_price = market_data["USDGBP=X"].tail(1).values[0]
    # Create spot purchase order to purchase USD using GBP
    order = currency_pair(currency_to_trade[0], currency_to_trade[1], rate=current_spot_price, quantity=1000)
    # Purchase order
    account.buy(order)
    # Return data
    return order, recursive_data


if __name__ == "__main__":
    # This if statement is required, all code to run the function must be located under here

    
    # Initialise the portfolio to be traded
    portfolio_1 = portfolio(1000)
    # print(portfolio_1.positions["MSFT"])
    # print(portfolio_1.positions["MSFT"]["position"])
    # print(portfolio_1.positions["MSFT"]["contracts"])

    msft_call = optionContract("MSFT", 400, 3, datetime.datetime.now(),"call")

    portfolio_1.buy(msft_call, 400)
    portfolio_1.buy(msft_call,200)

    print(portfolio_1.positions["MSFT"]["contracts"])
    # print(portfolio_1.positions)c

    """apple = asset("AAPL",122)

    portfolio_1.buy(apple, 500)
    print(portfolio_1.positions)
    portfolio_1.sell(apple, 500)
    print(portfolio_1.positions)
"""