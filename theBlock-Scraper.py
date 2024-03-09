import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import pytz



def scrape_latest_articles():
    try:
        url = 'https://www.theblock.co/latest'

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all elements representing articles
            articles = soup.find_all('article', class_='articleCard')

            latest_articles = []
            for article in articles[:5]:
                # Extract the pubDate
                pub_date_elem = article.find('div', class_='pubDate')
                pub_date_str = pub_date_elem.get_text(strip=True) if pub_date_elem else 'Unknown'

                est = pytz.timezone('US/Eastern')
                utc = pytz.utc
                est_time = datetime.strptime(pub_date_str, "%B %d, %Y, %I:%M%p EST")
                est_time = est.localize(est_time)
                utc_time = est_time.astimezone(utc)

                title_elem = article.find('span', attrs={'ga-on': 'click', 'ga-event-category': 'Article',
                                                         'ga-event-action': 'Click'})
                title = title_elem.text.strip() if title_elem else 'Unknown'

                latest_articles.append({'pubDate': utc_time.strftime("%B %d, %Y, %I:%M%p UTC"), 'title': title})

            return latest_articles
        else:
            print(f'Failed to retrieve the webpage. Status Code: {response.status_code}')
            return []
    except Exception as e:
        print(f'An error occurred: {e}')
        return []


def print_latest_articles_with_updates():
    old_articles = scrape_latest_articles()
    print("Initial Articles:")
    for index, article in enumerate(old_articles, start=1):
        pub_date = article['pubDate']
        title = article['title']
        print(f"{index}. Article-Title: {title}, Pub Date: {pub_date}")

    while True:
        new_articles = scrape_latest_articles()
        if new_articles != old_articles:
            print("\nNew articles detected!")
            for index, article in enumerate(new_articles, start=1):
                pub_date = article['pubDate']
                title = article['title']
                print(f"{index}. Article-Title: {title}, Pub Date: {pub_date}")
            old_articles = new_articles
        else:
            print("\nNo new articles found. Continuing...")
        time.sleep(120)

print_latest_articles_with_updates()
