from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset
from surmount.technical_indicators import EMA, ADX

class EMA_ADX_Strategy(Strategy):
    def __init__(self, tickers):
        self.tickers = tickers
        # You may include additional data sources if needed
        self.data_list = [Asset(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # 1‑hour timeframe
        return "1hour"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {ticker: 0.0 for ticker in self.tickers}

        for ticker in self.tickers:
            ohlcv = data[("ohlcv", ticker)]
            if ohlcv is None or len(ohlcv) < 50:
                continue

            # Extract close, high, low series
            closes = [row["close"] for row in ohlcv]
            
            # Compute indicators
            ema13_series = EMA(ticker, ohlcv, length=13)
            adx_series  = ADX(ticker, ohlcv, length=14)

            # Use the most recent values
            current_close = closes[-1]
            current_ema13  = ema13_series[-1] if ema13_series else None
            current_adx   = adx_series[-1] if adx_series else None

            if current_ema13 is None or current_adx is None:
                continue

            # Strategy logic
            if current_close > current_ema13 and current_adx > 20:
                # Enter long: allocate full weight to this ticker
                allocation_dict[ticker] = 1.0
                log(f"{ticker} • Enter long at {current_close:.2f} (EMA13={current_ema13:.2f}, ADX={current_adx:.2f})")
            elif current_close < current_ema13:
                # Exit / avoid long: set allocation to zero
                allocation_dict[ticker] = 0.0
                log(f"{ticker} • Exit/No position at {current_close:.2f} (below EMA13={current_ema13:.2f})")
            else:
                # Maintain current, or flat
                allocation_dict[ticker] = 0.0

        return TargetAllocation(allocation_dict)