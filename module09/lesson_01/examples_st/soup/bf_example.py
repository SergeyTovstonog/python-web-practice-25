import requests
from bs4 import BeautifulSoup

# Step 1: Send a GET request to the website
url = "http://quotes.toscrape.com/"
response = requests.get(url)

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.text, 'lxml')  # You can also use 'html.parser'

# Step 3: Find all quote elements
quotes = soup.find_all('div', class_='quote')

# Step 4: Extract and print quotes and authors
for quote in quotes:
    text = quote.find('span', class_='text').get_text()
    author = quote.find('small', class_='author').get_text()
    tags = quote.find_all('a', class_='tag')
    tags_text = [tag.get_text() for tag in tags]

    print(f"{text} - {author} | {', '.join(tags_text)}")

