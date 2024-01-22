import pandas as pd
import numpy as np

data = pd.read_csv("NIFTY 50-20-12-2023-to-20-01-2024.csv")
data.columns = data.columns.str.strip()
# Calculate daily returns
data["Daily Returns"] = data["Close"] / data["Close"].shift(1) - 1
print(data["Daily Returns"])
# Drop the first row which contains NaN in 'Daily Returns'
data = data.dropna(subset=['Daily Returns'])
print(data["Daily Returns"])
# Calculate daily volatility
daily_volatility = data['Daily Returns'].std()
print(daily_volatility)

# Calculate annualized volatility (assuming 252 trading days per year)
annualized_volatility = daily_volatility * np.sqrt(252)
print(annualized_volatility)

print("Daily Volatility:", daily_volatility)
print("Annualized Volatility:", annualized_volatility)
