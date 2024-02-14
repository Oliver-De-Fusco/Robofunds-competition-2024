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

    # Get the most recent market data - In this case it is using yfinance
    tradable_universe = ("USDGBP=X", "USDEUR=X", "USDAUD=X", "USDCNY=X", "USDJPY=X")
    market_data = yfinance.download(tradable_universe, period="10d").dropna()
    
    # Initialise the portfolio to be traded
    portfolio_1 = portfolio()
    print(market_data[["Adj Close"]])

    # run the function
    trade(portfolio_1, market_data["Adj Close"],None)

    # Display result
    print(portfolio_1.positions)