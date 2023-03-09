from datetime import datetime as dt
from datetime import date
from pandas.core.frame import DataFrame
from discord.ext import tasks

from trade.speculbot import SpeculBot
from utils.embedlogger import EmbedLogger
from hook.discordparser import *


class Macd(SpeculBot):
    def __init__(self, logger=EmbedLogger()):
        super.__init__(logger)

    @tasks.loop(seconds = 10) # repeat after every 1800 seconds
    async def loop(self):
        if self.is_market_open():
            """TODO Run algorithm -> return Decision object"""
            pass

    def algorithm(self, tickers: list, history, stop_loss: list):
        prices = []

        # Add the closing prices to the prices list and make sure we 
        # start at greater than 2 dollars to reduce outlier calculations.
        for ticker, sl in zip(tickers, stop_loss):
            for price in history['Close'][ticker.name]:
                prices.append(price)

            prices_df = DataFrame(prices)  # Make a dataframe from the prices list

            # Calculate exponential weighted moving averages:
            day12 = prices_df.ewm(span=12).mean()
            day26 = prices_df.ewm(span=26).mean()
            macd = day12 - day26

            signal = macd.ewm(span=9).mean()

            current_state = -1
            last_state = ticker.states[-1]

            # Information sur la deniere analyse, soit buy ou sell
            compar = macd.iloc[-1][0] - signal.iloc[-1][0]
            if compar > 0:
                current_state = 1
            elif compar <= 0:
                current_state = 0

            closing_yesterday = prices_df.iloc[-2][0]
            closing_today = prices_df.iloc[-1][0]

            if current_state == 1:
                ratio = (closing_today - closing_yesterday)/closing_yesterday
                if ratio < sl:
                    ticker.add_state(0)

                    # Pour empêcher plusieurs SELL signal en rafale
                    if ticker.states[-2] == ticker.states[-1]:
                        ticker.result = -1
                    continue

            if current_state == 1 and last_state <= 0:
                ticker.add_state(1)
                continue
            elif current_state == 0 and last_state == 1:
                ticker.add_state(0)
                continue
            elif current_state == 0 and last_state == -1:
                ticker.add_state(0)
                continue
            elif current_state == last_state:
                ticker.result = -1
                continue

if __name__ == "__main__":
    # Logger being passed to all functions
    logger = EmbedLogger(name="MACD", verbose=True)
    bot = SpeculBot(logger)