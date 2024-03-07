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

# Maritime news website 1
URL = "https://www.seatrade-maritime.com/"

# Define the path to the SQLite database
db_path = "data/news/maritime_air_news.db"
# Define table naming by date of execution
current_date = datetime.now().strftime("%m%d%Y")
mar_news_table_name = f"mar_news_{current_date}"


helper_obj = Helper(db_path, mar_news_table_name)
# Load keywords from JSON file for classification
with open("json/keywords.json", "r") as file:
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
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept All']"))
        )
        # Click the button once it is clickable
        browser.find_element(By.XPATH, "//button[text()='Accept All']").click()
    except (NoSuchElementException, TimeoutException):
        print("The cookie acceptance button was not found on the page.")

    # Recent NEWS
    location = "Global"
    browser.implicitly_wait(2)
    # List of latest global news
    recent_news = browser.find_element(
        By.XPATH, "//a[contains(@href, '/recent')]"
    ).get_attribute("href")
    browser.get(recent_news)
    latest_news = browser.find_element(By.CLASS_NAME, "view-content").find_elements(
        By.TAG_NAME, "article"
    )
    article_url = [
        news.find_element(By.TAG_NAME, "a").get_attribute("href")
        for news in latest_news
    ]
    # pagination = browser.find_element(By.XPATH, "//li[contains(@class, 'pager__item')]").find_element(By.TAG_NAME, "a").get_attribute('href')
    for url in article_url:
        # url = article_url[1]
        time.sleep(5)
        browser.get(url)
        article_title = browser.find_element(
            By.CSS_SELECTOR, "h1[itemprop='headline']"
        ).text
        # summary = browser.find_element(By.XPATH, "//div[contains(@class, 'field field-name-field-penton-content-summary field-type-text-long field-label-hidden')]").text
        article_date = (
            browser.find_element(By.CSS_SELECTOR, "p[class='author-and-date']")
            .text.split("|")[-1]
            .strip()
        )
        date_obj = datetime.strptime(article_date, "%b %d, %Y")
        article_text = browser.find_element(
            By.CSS_SELECTOR, "div[itemprop='articleBody']"
        ).text

        premium = False

        if premium:
            summary = helper_obj.summarize_text(article_text)
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
            article_url,
            date_obj
        )
        conn.commit()
    conn.close()
    browser.quit()


if __name__ == "__main__":
    main()
