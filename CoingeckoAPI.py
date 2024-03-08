import requests
import time

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'YOUR_API_KEY'

# Your custom coin ID
your_coin_id = 'your-coin-id'

# List of coins to fetch prices for
coins = ['dogecoin', 'dogwifcoin', 'pepe', 'shiba-inu', 'mog-coin', 'meme', 'bonk', 'floki', 'myro', 'maga', 'bitcoin', 'ethereum', 'chainlink', 'binancecoin', 'solana','ripple','cardano','avalanche-2','tether','uniswap',
         'bitcoin-cash','near','aptos','optimism','bittensor','render-token','injective-protocol','kaspa','arbitrum','celestia','fetch-ai']

coin_data = {}


def fetch_prices(coins):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(coins)}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        for coin_id, info in data.items():
            if 'usd' in info:
                price = info['usd']
                market_cap = info.get('usd_market_cap', 'N/A')
                change_24h = info.get('usd_24h_change', 'N/A')
                coin_data[coin_id] = {
                    'price': price,
                    'market_cap': market_cap,
                    'change_24h': change_24h
                }
    except requests.RequestException as e:
        print("Error fetching prices:", e)


def print_prices():
    for coin_id, info in coin_data.items():
        price = info['price']
        market_cap = info['market_cap']
        change_24h = info['change_24h']

        market_cap_formatted = "${:,.0f}".format(market_cap) if market_cap != 'N/A' else 'N/A'
        change_24h_formatted = "{:.2f}%".format(change_24h) if change_24h != 'N/A' else 'N/A'
        formatted_price = "{:.10f}".format(price)

        print(f"Coin ID: {coin_id}")
        print(f"Price: {formatted_price}")
        print(f"Market Cap: {market_cap_formatted}")
        print(f"24h Change: {change_24h_formatted}")
        print("\n")


while True:
    fetch_prices(coins)
    print_prices()
    # Introduce a delay of 65 seconds before making the next request
    time.sleep(65)


