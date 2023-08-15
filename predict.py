import pandas as pd

def predict():
    # Load the CSV file into a DataFrame
    data = pd.read_csv('stock_data.csv')

    data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    data['Open'] = pd.to_numeric(data['Open'], errors='coerce')
    data['Volume'] = pd.to_numeric(data['Volume'], errors='coerce')

    # Calculate a score for each stock based on some criteria (e.g., price change percentage, volume)
    data['Score'] = ((data['Close'] - data['Open']) / data['Open']) * data['Volume']

    # Group data by stock and calculate the total score for each stock
    grouped = data.groupby('Stock')['Score'].sum().reset_index()

    # Sort stocks based on the total score in descending order
    sorted_stocks = grouped.sort_values(by='Score', ascending=False)

    # Recommend the top stock
    recommended_stock = sorted_stocks.iloc[0]['Stock']

    print("Currently Recommended stock in order", recommended_stock)