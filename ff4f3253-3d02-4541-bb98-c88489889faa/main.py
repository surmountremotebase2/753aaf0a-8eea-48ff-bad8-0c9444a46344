import pandas as pd
import ta

# === Load historical data ===
# Make sure your CSV has columns: Date, Open, High, Low, Close, Volume
data = pd.read_csv("AAPL_1h.csv", parse_dates=["Date"], index_col="Date")

# === Calculate indicators ===
data['EMA13'] = ta.trend.EMAIndicator(close=data['Close'], window=13).ema_indicator()
adx_indicator = ta.trend.ADXIndicator(high=data['High'], low=data['Low'], close=data['Close'], window=14)
data['ADX'] = adx_indicator.adx()

# === Strategy parameters ===
adx_threshold = 20

# === Generate signals ===
data['Long'] = (data['Close'] > data['EMA13']) & (data['ADX'] > adx_threshold)
data['Exit'] = data['Close'] < data['EMA13']

# === Backtesting ===
position = 0
entry_price = 0
returns = []

for i in range(len(data)):
    if position == 0:
        if data['Long'].iloc[i]:
            position = 1
            entry_price = data['Close'].iloc[i]
    elif position == 1:
        if data['Exit'].iloc[i]:
            exit_price = data['Close'].iloc[i]
            returns.append(exit_price - entry_price)
            position = 0

# Close any open position at the end
if position == 1:
    returns.append(data['Close'].iloc[-1] - entry_price)

# === Results ===
total_profit = sum(returns)
num_trades = len(returns)
avg_profit = total_profit / num_trades if num_trades > 0 else 0

print(f"Number of trades: {num_trades}")
print(f"Total Profit: {total_profit:.2f}")
print(f"Average Profit per Trade: {avg_profit:.2f}")