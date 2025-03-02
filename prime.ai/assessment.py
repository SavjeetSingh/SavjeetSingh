import requests
import pandas as pd
import openpyxl
import time

# CoinMarketCap API key (Replace with your own API key)
API_KEY = "fd59d133-6d6e-44d7-8bd9-de572edc502b"

# CoinMarketCap API URL
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Request Headers
HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY
}

# API Parameters
PARAMS = {
    "start": "1",         # Start from rank 1
    "limit": "50",        # Get top 50 cryptocurrencies
    "convert": "USD"      # Convert prices to USD
}

# Function to fetch live cryptocurrency data
def fetch_crypto_data():
    response = requests.get(API_URL, headers=HEADERS, params=PARAMS)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print("Failed to fetch data from CoinMarketCap API")
        return None

# Function to process and analyze data
def analyze_crypto_data(data):
    # Extract relevant fields
    crypto_list = []
    
    for coin in data:
        crypto_list.append({
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Current Price (USD)": coin["quote"]["USD"]["price"],
            "Market Cap (USD)": coin["quote"]["USD"]["market_cap"],
            "24h Volume (USD)": coin["quote"]["USD"]["volume_24h"],
            "24h Change (%)": coin["quote"]["USD"]["percent_change_24h"]
        })
    
    # Convert to DataFrame
    df = pd.DataFrame(crypto_list)

    # Top 5 cryptocurrencies by Market Cap
    top_5 = df.nlargest(5, "Market Cap (USD)")

    # Average price of the top 50 cryptocurrencies
    avg_price = df["Current Price (USD)"].mean()

    # Highest & lowest 24-hour percentage price change
    max_change = df["24h Change (%)"].max()
    min_change = df["24h Change (%)"].min()

    return df, top_5, avg_price, max_change, min_change

# Function to update Excel file
def update_excel(df):
    file_path = "Live_Crypto_Data.xlsx"

    with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, sheet_name="Live Prices", index=False)

# Run the script continuously every 5 minutes
while True:
    print("Fetching and updating data from CoinMarketCap API...")

    # Fetch data
    crypto_data = fetch_crypto_data()
    
    if crypto_data:
        # Analyze data
        df, top_5, avg_price, max_change, min_change = analyze_crypto_data(crypto_data)

        # Update Excel sheet
        update_excel(df)

        print("Updated Excel file successfully.")
    
    # Wait for 5 minutes before next update
    time.sleep(300)
