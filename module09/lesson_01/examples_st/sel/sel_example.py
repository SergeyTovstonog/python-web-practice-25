from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Set up the WebDriver (Ensure chromedriver is in PATH)
# service = Service('path/to/chromedriver')  # Replace with actual path or omit if in PATH
# driver = webdriver.Chrome(service=service)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'))

try:
    # Step 2: Navigate to the website
    driver.get("http://quotes.toscrape.com/js/")  # Assume this is a dynamic version

    # Step 3: Wait for the page to load
    time.sleep(3)  # Simple wait; for better handling, use WebDriverWait

    # Step 4: Find all quote elements
    quotes = driver.find_elements(By.CLASS_NAME, 'quote')

    # Step 5: Extract and print quotes and authors
    for quote in quotes:
        text = quote.find_element(By.CLASS_NAME, 'text').text
        author = quote.find_element(By.CLASS_NAME, 'author').text
        print(f"{text} - {author}")

finally:
    # Step 6: Close the browser
    driver.quit()
