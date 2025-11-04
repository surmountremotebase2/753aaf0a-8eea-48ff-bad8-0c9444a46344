from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, ADX

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize strategy properties
        self.assets = ["NVDA"]  # Example ticker, replace with assets of your choice

    @property
    def interval(self):
        return "1hour"  # Interval can be adjusted based on trading preferences

    @property
    def data(self):
        return []  # No additional data sources needed for this strategy

    def run(self, data):
        # Initialize allocation dictionary
        allocation_dict = {}
        
        for ticker in self.assets:
            # Ensure that there is enough historical data to compute indicators
            if len(data["ohlc"]) > 13:
                # Calculate the 13-day EMA and ADX for the ticker
                ema13 = EMA(ticker, data["ohlc"], 13)
                adx = ADX(ticker, data["ohlc"], 14)  # 14-day period is standard for ADX
            
                # Get the last closing price and the last ADX value
                last_close = data["ohlc"][-1][ticker]["close"]
                last_ema13 = ema13[-1]
                last_adx = adx[-1]

                # Decision logic for entering or exiting trades
                if last_close > last_ema13 and last_adx > 20:
                    # Enter: Allocate 100% if price closes above 13 EMA and ADX is above 20
                    allocation_dict[ticker] = 1.0
                elif last_close < last_ema13:
                    # Exit: Allocate 0% if price closes below 13 EMA
                    allocation_dict[ticker] = 0
                else:
                    # Hold current allocation if none of the conditions meet
                    # This case avoids making changes to the allocation if not entering/exiting positions
                    # Update this logic based on how you'd prefer to manage current positions
                    allocation_dict[ticker] = 0 # Assuming exit, update as needed
            else:
                # Insufficient data - do not allocate
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)