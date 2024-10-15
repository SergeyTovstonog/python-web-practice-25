import time
from playwright.sync_api import sync_playwright

# Credentials (replace with actual values)
username = "admin"
password = "admin"  # This is the demo credentials for the site


def login_and_scrape(playwright):
    # Launch the browser
    browser = playwright.chromium.launch(headless=False)  # Set headless=True for headless mode
    page = browser.new_page()

    # Go to the login page
    page.goto("http://quotes.toscrape.com/login")

    # Fill out the login form
    page.fill('input[name="username"]', username)  # Find username input field
    page.fill('input[name="password"]', password)  # Find password input field

    # Click the login button
    page.click('input.btn.btn-primary')

    # Wait for the next page to load after login
    page.wait_for_load_state('networkidle')  # Wait for the page to fully load

    print("Login successful! Page title:", page.title())

    # Go to the main quotes page
    page.goto("http://quotes.toscrape.com/")

    all_quotes = []

    # Scrape quotes and tags across multiple pages
    while True:
        # Find all quote elements on the page
        quotes = page.query_selector_all('div.quote')
        for quote in quotes:
            text = quote.query_selector('span.text').inner_text()
            author = quote.query_selector('small.author').inner_text()
            tags = [tag.inner_text() for tag in quote.query_selector_all('a.tag')]
            all_quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })

        # Check for the next page button
        next_button = page.query_selector('li.next > a')
        if next_button:
            next_button.click()
            page.wait_for_load_state('networkidle')  # Wait for the next page to load
            time.sleep(2)
        else:
            break

    # Close the browser
    browser.close()

    # Print scraped quotes
    for quote in all_quotes:
        print(f"{quote['text']} - {quote['author']} | Tags: {', '.join(quote['tags'])}")


with sync_playwright() as playwright:
    login_and_scrape(playwright)
