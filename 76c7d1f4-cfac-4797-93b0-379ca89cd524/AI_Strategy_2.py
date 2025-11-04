from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, ADX

class NVDAEMAStrategy(Strategy):
    def __init__(self):
        # Define the assets and data interval for the strategy
        self.tickers = ["NVDA"]
        self.data_list = []  # Placeholder for any additional data requirements

    @property
    def interval(self):
        return "1day"  # Using daily data for EMA and ADX calculation

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize allocation dict to define our target asset allocations
        allocation_dict = {}
        
        # Check if we have enough data to compute the indicators
        if "ohlcv" in data and len(data["ohlcv"]) > 13:
            # Retrieve NVDA's price data
            nvda_data = data["ohlcv"]
            
            # Calculate the 13-period EMA for NVDA
            nvda_ema = EMA("NVDA", nvda_data, 13)
            
            # Calculate the ADX based on a typical 14-day period to gauge trend strength
            nvda_adx = ADX("NVDA", nvda_data, 14)
            
            # We need at least 1 element in nvda_ema and nvda_adx to proceed
            if nvda_ema and nvda_adx:
                # Check the latest close price against the 13-period EMA and ADX value
                latest_close = nvda_data[-1]["NVDA"]["close"]
                if latest_close > nvda_ema[-1] and nvda_adx[-1] > 20:
                    # If the conditions are met, allocate 100% of the portfolio to NVDA stocks
                    # This implies buying 10 stocks of NVDA, assuming 100% of the portfolio can accommodate that
                    allocation_dict["NVDA"] = 1  # Replace 1 with the proportion of portfolio value you wish to allocate
                elif latest_close < nvda_ema[-1]:
                    # If the closing price is below the 13-day EMA, exit the position
                    allocation_dict["NVDA"] = 0  # Set allocation to 0 to indicate selling off the position
            else:
                # If there's insufficient data to calculate either indicator, do not allocate to NVDA
                allocation_dict["NVDA"] = 0
        else:
            # Initialize NVDA allocation to 0 if there's not enough data
            allocation_dict["NVDA"] = 0
        
        # Return the TargetAllocation based on the allocation dict
        return TargetAllocation(allocation_dict)

# Note: This strategy assumes that buying 10 stocks of NVDA equates to allocating 100% of the portfolio to NVDA.
# Adjust the allocation percentage based on your portfolio value and the current price of NVDA stocks.