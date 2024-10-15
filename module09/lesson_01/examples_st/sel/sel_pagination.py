from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_quotes(driver):
    quotes_data = []

    # Find all quote elements on the page
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')
    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, 'text').text
        author = quote.find_element(By.CLASS_NAME, 'author').text
        tags_elements = quote.find_elements(By.CLASS_NAME, 'tag')
        tags = [tag.text for tag in tags_elements]
        quotes_data.append({
            'text': text,
            'author': author,
            'tags': tags
        })

    return quotes_data

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("http://quotes.toscrape.com")
    all_quotes = []

    while True:
        # Scrape the current page
        print(f"Scraping {driver.current_url}...")
        quotes = scrape_quotes(driver)
        all_quotes.extend(quotes)

        try:
            # Look for the "Next" button and click it
            next_button = driver.find_element(By.CLASS_NAME, 'next')
            next_button.find_element(By.TAG_NAME, 'a').click()
            time.sleep(2)  # Pause for a bit to ensure the next page loads
        except Exception as e:
            print("No more pages to scrape.")
            break

    driver.quit()

    # Display the scraped quotes
    for quote in all_quotes:
        print(f"{quote['text']} - {quote['author']} | Tags: {', '.join(quote['tags'])}")

if __name__ == "__main__":
    main()
