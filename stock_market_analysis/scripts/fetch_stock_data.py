import requests
import pandas as pd
import os

def fetch_stock_data(stock_symbol, api_key):
    # API URL for fetching stock data
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_symbol}&interval=5min&apikey={api_key}&datatype=json"
    
    # Sending the request to the API
    response = requests.get(url)
    data = response.json()

    # Check for errors in the response
    if 'Time Series (5min)' not in data:
        print("Error fetching data:", data.get("Note", "Unknown error occurred."))
        return None

    # Convert the time series data to a DataFrame
    df = pd.DataFrame.from_dict(data['Time Series (5min)'], orient='index')
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)

    # Add a 20-period simple moving average
    df['SMA_20'] = df['close'].rolling(window=20).mean()

    return df

if __name__ == "__main__":


    api_key = '983MEP2LEGIWSQLM'
    stock_symbol = input("Enter the stock symbol (e.g., AAPL, TSLA, MSFT): ")

    # Fetching data
    stock_data = fetch_stock_data(stock_symbol, api_key)

    if stock_data is not None:
        # Define the output path using os.path
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'{stock_symbol}_data.csv')
        
        # Save to CSV
        stock_data.to_csv(output_path)
        print(f"Data saved to {output_path}")
