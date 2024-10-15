import requests
from bs4 import BeautifulSoup

def scrape_quotes(page_url):
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {page_url}")
        return []

    soup = BeautifulSoup(response.text, 'lxml')
    quotes_data = []

    quotes = soup.find_all('div', class_='quote')
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    # Check for the next page link
    next_button = soup.find('li', class_='next')
    next_page_url = None
    if next_button:
        next_page_url = next_button.find('a')['href']
        next_page_url = f"http://quotes.toscrape.com{next_page_url}"

    return quotes_data, next_page_url

def main():
    base_url = "http://quotes.toscrape.com"
    current_url = base_url
    all_quotes = []

    while current_url:
        print(f"Scraping {current_url}...")
        quotes, next_page_url = scrape_quotes(current_url)
        all_quotes.extend(quotes)
        current_url = next_page_url  # Move to the next page

    # Display the scraped quotes
    for quote in all_quotes:
        print(f"{quote['text']} - {quote['author']} | Tags: {', '.join(quote['tags'])}")

if __name__ == "__main__":
    main()
