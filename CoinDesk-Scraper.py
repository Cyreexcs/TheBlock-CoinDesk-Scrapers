import requests
from bs4 import BeautifulSoup
import time
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




def parse_time(time_str):
    try:
        # Attempt to parse the time string
        return time_str.split(' at ')[1].strip()
    except IndexError:
        print(f"Error: Unable to parse time string: {time_str}")
        return None

# Function to scrape the latest articles and return their titles and post times in a dictionary
def scrape_latest_articles():
    # URL of the CoinDesk website
    url = 'https://www.coindesk.com/'

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all elements representing articles
        articles = soup.find_all('div', class_='static-cardstyles__StaticCardWrapper-sc-1kiw3u-0 iiwocm') + \
                   soup.find_all('div', class_='side-cover-cardstyles__SideCoverCardData-sc-1nd3s5z-2 gnuOAQ')

        # Dictionary to store the titles and post times of the last 5 articles
        latest_articles_dict = {}

        # Extract the titles and post times of the last 5 articles
        for index, article in enumerate(articles[:7], start=1):
            title_elem = article.find('h2', class_='typography__StyledTypography-sc-owin6q-0 dtjHgI')
            title = title_elem.text.strip() if title_elem else 'Unknown'
            time_elem = article.find('span', class_='typography__StyledTypography-sc-owin6q-0 iOUkmj')
            time_str = time_elem.text.strip() if time_elem else 'Unknown'
            post_time = parse_time(time_str)
            latest_articles_dict[index] = {'title': title, 'post_time': post_time}

        return latest_articles_dict
    else:
        print('Failed to retrieve the webpage.')
        return {}

def print_latest_articles_with_updates():
    old_articles = scrape_latest_articles()
    print("Initial Articles:")
    for index, article_info in old_articles.items():
        title = article_info['title']
        post_time = article_info['post_time']
        print(f"{index}. {title}, Post Time: {post_time}")
    while True:
        time.sleep(120)  # Wait for 1 second before checking for new articles
        new_articles = scrape_latest_articles()
        if new_articles != old_articles:
            print("New article(s) detected!")
            for index, article_info in new_articles.items():
                if index not in old_articles:
                    title = article_info['title']
                    post_time = article_info['post_time']
                    print(f"{index}. {title}, Post Time: {post_time}")
            old_articles = new_articles
        else:
            print("No new articles found. Continuing...")

# Start printing the latest articles with updates
print_latest_articles_with_updates()
