import requests
from bs4 import BeautifulSoup
import time
from textblob import TextBlob


def parse_time(time_str):
    try:
        return time_str.split(' at ')[1].strip()
    except IndexError:
        print(f"Error: Unable to parse time string: {time_str}")
        return None


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


# Function to fetch prices of cryptocurrencies
def fetch_prices(coins):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={",".join(coins)}&vs_currencies=usd&include_24hr_change=true&include_market_cap=true'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4XX and 5XX status codes
        data = response.json()
        return data
    except requests.RequestException as e:
        print("Error fetching prices:", e)
        return None


# Function to analyze sentiment of news articles
def analyze_sentiment(text):
    # Use TextBlob for sentiment analysis
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Bullish"
    elif sentiment_score < 0:
        return "Bearish"
    else:
        return "Neutral"


# Initialize the latest articles dictionary
latest_articles = {}


# Function to merge and print the latest articles
def merge_and_print(last_output):
    coins = ['dogecoin', 'dogwifcoin', 'pepe', 'shiba-inu', 'mog-coin', 'meme', 'bonk', 'floki', 'myro', 'maga',
             'bitcoin', 'ethereum', 'chainlink', 'binancecoin', 'solana', 'ripple', 'cardano', 'avalanche-2', 'tether',
             'uniswap',
             'bitcoin-cash', 'aptos', 'optimism', 'bittensor', 'render-token', 'injective-protocol', 'kaspa',
             'arbitrum', 'celestia', 'fetch-ai']

    # Scrape the latest articles
    new_articles = scrape_latest_articles()

    # Check if new articles are found
    if new_articles:
        # Check if new articles are different from the last output
        if new_articles != last_output:
            prices_data = fetch_prices(coins)

            if prices_data:
                updated = False
                for index, article_info in new_articles.items():
                    title = article_info['title']
                    coin_name = None
                    for coin_id, price_info in prices_data.items():
                        if coin_id.lower() in title.lower():
                            coin_name = coin_id
                            price = '{:,.2f}'.format(price_info['usd'])
                            market_cap = '{:,.2f}'.format(price_info.get('usd_market_cap', 0))
                            change_24h = "{:.2f}%".format(price_info.get('usd_24h_change', 0))
                            sentiment = analyze_sentiment(title)
                            print(f"News Article: {title}")
                            print(f"Time: {article_info['post_time']} ")
                            print(f"Coin Name: {coin_name}")
                            print(f"Price: ${price}")
                            print(f"Market Cap: ${market_cap} | 24H change: {change_24h} | Sentiment {sentiment}")
                            print()  # Print an empty line for separation
                            updated = True
                            break  # Exit the loop after finding the first coin match

                if not updated:
                    print("Failed to retrieve cryptocurrency prices.")
            else:
                print("Failed to fetch cryptocurrency prices.")

            return new_articles  # Return the updated container
        else:
            print("No new articles found.")
            return last_output  # Return the unchanged container
    else:
        print("No new articles found.")
        return last_output  # Return the unchanged container


# Initially print the latest articles
latest_articles = merge_and_print(None)

# Start listening for updates
while True:
    time.sleep(62)
    latest_articles = merge_and_print(latest_articles)

