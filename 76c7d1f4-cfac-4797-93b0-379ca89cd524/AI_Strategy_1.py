from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, ADX

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the tickers of interest
        self.tickers = ["SPY"]  # Example with SPY, add more as needed

    @property
    def assets(self):
        # List of assets (tickers) this strategy will evaluate
        return self.tickers

    @property
    def interval(self):
        # Data interval to use for indicators and analysis
        return "1day"

    @property
    def data(self):
        # List of additional data sources needed, empty if only OHLCV is used
        return []

    def run(self, data):
        # Initialize the allocation dictionary with 0 allocation for each ticker
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Iterate through each ticker and apply the strategy
        for ticker in self.tickers:
            # Check if there's enough data to perform the analysis
            if len(data["ohlcv"]) > 13:
                # Calculate 13-day EMA and ADX for the ticker
                ema_13 = EMA(ticker, data["ohlcv"], length=13)
                adx_value = ADX(ticker, data["ohlcv"], length=14)  # Default ADX period is 14

                # Get the most recent closing price
                last_close = data["ohlcv"][-1][ticker]["close"]

                # Check if the current conditions meet the buying criteria
                if last_close > ema_13[-1] and adx_value[-1] > 20:
                    allocation_dict[ticker] = 1  # Allocate fully (e.g., buy 10 stocks) to this ticker
                # Implement the exit strategy
                elif last_close < ema_13[-1]:
                    allocation_dict[ticker] = 0  # Deallocate (e.g., sell the previously bought stocks)

        # Return the allocation dict as a TargetAllocation object
        return TargetAllocation(allocation_dict)