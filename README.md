# Crypto News Scrapers

## Features

- Seamlessly extracts the latest news articles from renowned cryptocurrency platforms such as [The Block](https://www.theblockcrypto.com/) and [CoinDesk](https://www.coindesk.com/)
- Enhances the news output by identifying the specific cryptocurrency token mentioned in each article's title. This enables the scraper to provide additional insights into the highlighted token, including its current price, 24-hour price change, market cap, and sentiment analysis (bullish, bearish, or neutral).
- Operates continuously, ensuring timely updates every 60-65 seconds. This consistent refresh rate guarantees users have access to the most recent news and market data, empowering them to make informed decisions in the dynamic cryptocurrency market.

![outputGithub](https://github.com/Cyreexcs/TheBlock-CoinDesk-Scrapers/assets/70235827/f397f223-bee7-48bd-83a6-ae66a5d2e54c)

## Usage

1. **Clone the repository to your local machine:**

   ```bash
   git clone https://github.com/Cyreexcs/TheBlock-CoinDesk-Scrapers.git

Configuration
You can modify the frequency of scraping (default: every 60 seconds) by adjusting the interval but note that the free Coingecko API only allows for 1 call every 60 seconds.

## Dependencies

- [Requests](https://pypi.org/project/requests/): A library for making HTTP requests.
- [TextBlob](https://pypi.org/project/textblob/): A library for processing textual data, including sentiment analysis.
- [Beautiful Soup](https://pypi.org/project/beautifulsoup4/): A library for parsing HTML and XML documents.
- [CoinGecko API](https://www.coingecko.com/api): Used to Fetch Data.
