import json
import time

from datetime import datetime
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src import Helper

# Load the variables from .env into the environment
load_dotenv()

# Air traffic news website 1
URL = "https://www.aircargonews.net/category/region/americas/"

# Define the path to the SQLite database
db_path = "../data/news/air_news.db"
# Define table naming by date of execution
current_date = datetime.now().strftime("%m%d%Y")
air_news_table_name = f"air_news_{current_date}"
helper_obj = Helper(db_path, air_news_table_name)

# Load keywords from JSON file for classification
with open("../json/keywords.json", "r") as file:
    keywords = json.load(file)


def main():
    """ """
    conn = helper_obj.connect_to_db()
    cursor = conn.cursor()
    # Initialize DDBB and create tables
    helper_obj.initialize_tables()

    # Create a browser session
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.implicitly_wait(2)
    browser.get(URL)

    # Click cookies button
    try:
        # Wait for the button to be clickable
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='I Accept']"))
        )
        # Click the button once it is clickable
        browser.find_element(By.XPATH, "//button[text()='I Accept']").click()
    except (NoSuchElementException, TimeoutException):
        print("The cookie acceptance button was not found on the page.")

    # Recent NEWS
    location = "LATAM"
    browser.implicitly_wait(2)
    # List of latest global news
    region_cat = browser.find_elements(By.CLASS_NAME, "category-item")
    region_cat_url = [
        cat.find_element(By.TAG_NAME, "a").get_attribute("href") for cat in region_cat
    ]
    for cat in region_cat_url:
        # cat = region_cat_url[0]
        time.sleep(5)
        browser.get(cat)
        cat_items = browser.find_elements(By.CLASS_NAME, "category-item")
        # pagination = browser.find_element(By.CLASS_NAME, 'aircargo-pagination')
        # [element.get_attribute('href') for element in pagination.find_elements(By.TAG_NAME, "a")][-1]
        cat_items_url = [
            items.find_element(By.TAG_NAME, "a").get_attribute("href")
            for items in cat_items
        ]
        for items_url in cat_items_url:
            time.sleep(5)
            # items_url = cat_items_url[0]
            browser.get(items_url)
            article_title = browser.find_element(
                By.CSS_SELECTOR, "h1[class='blog-post-title']"
            ).text
            # summary = browser.find_element(By.XPATH, "//div[contains(@class, 'field field-name-field-penton-content-summary field-type-text-long field-label-hidden')]").text
            article_text = browser.find_element(
                By.CSS_SELECTOR, "div[class='content-section clearfix']"
            ).text
            article_date = browser.find_element(
                By.CSS_SELECTOR, "h4[class='post-date']"
            ).text.strip()
            date_obj = datetime.strptime(article_date.replace(" ", ""), "%d/%m/%Y")

            premium = False

            if premium:
                helper_obj.summarize_text(article_text)
            else:

                summary = "Get Premium for enabling AI-powered summary!"

            classification = helper_obj.classify_article(article_text, keywords)
            ml_classification = helper_obj.ml_classification(article_text)
            helper_obj.insert_article_data(
                cursor,
                article_title,
                article_text,
                summary,
                classification,
                ml_classification,
                location,
                items_url,
            )
            conn.commit()
    conn.close()
    browser.quit()


if __name__ == "__main__":
    main()
