import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = 'stock_data.csv'
df = pd.read_csv(csv_file)

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Pivot the data to create separate columns for each stock's 'Close' values
pivot_df = df.pivot(index='Date', columns='Stock', values='Close')

# Calculate the percentage change for each stock's 'Close' values
returns_df = pivot_df.pct_change()

# Calculate the cumulative returns for each stock
cumulative_returns = (1 + returns_df).cumprod()

# Calculate the final returns for each stock
final_returns = cumulative_returns.iloc[-1, :]

# Sort the stocks by final returns in descending order
best_performing = final_returns.sort_values(ascending=False)

# Plotting the data
plt.figure(figsize=(10, 4))
cumulative_returns.plot(ax=plt.gca())
plt.title('Cumulative Returns for Stocks')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.tight_layout()

# Show the plot
plt.show()

# Print the best performing stock
print("Best Performing Stock:", best_performing.index[0])
