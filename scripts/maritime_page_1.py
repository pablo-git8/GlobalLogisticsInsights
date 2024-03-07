# Imports
import json

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
from ml_classification import ml_classification


# Load the variables from .env into the environment
load_dotenv()

# Maritime news website 1
URL = "https://www.maritimelogisticsprofessional.com"

# Path to the SQLite database
db_path = '../data/news/maritime_air_news.db'
# Table naming by date of execution and type of news
current_date = datetime.now().strftime("%m%d%Y")
mar_news_table_name = f"mar_news_{current_date}"

helper_obj = Helper(db_path, mar_news_table_name)

# Load keywords from JSON file for classification
with open("../json/keywords.json", "r") as file:
    keywords = json.load(file)


def main():
    """ """
    # Initialize DDBB and create tables
    helper_obj.initialize_tables()

    # Create a browser session
    browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    browser.get(URL)

    # Define a wait variable with a timeout of 10 seconds
    wait = WebDriverWait(browser, 10)

    # Cookies button
    try:
        # Wait for the button to be clickable and click it
        cookie_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Ok']"))
        )
        cookie_button.click()

    except TimeoutException:
        print("The cookie acceptance button was not found on the page.")

    # GLOBAL NEWS
    location = "Global"

    # Get latest news urls
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "snippet-flex")))
        latest_news = browser.find_elements(By.CLASS_NAME, "snippet-flex")
        article_urls = [
            element.get_attribute("href")
            for element in latest_news
            if "/news/" in element.get_attribute("href")
        ]

    except TimeoutException:
        print("Latest news elements were not found on the page.")
        article_urls = []

    # Premium version
    premium = False

    # Connect to DDBB
    conn = helper_obj.connect_to_db()
    cursor = conn.cursor()

    print(f"\nGetting {location} news...")

    # Iterate through global news
    for article in article_urls:
        """ """
        article = article_urls[0]
        try:
            # Get article
            browser.get(article)

            # Find the title element and get the text
            title_element = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
            )
            article_title = title_element.text
            print(article_title)

            # Find the article body element and get all the paragraph texts
            article_body_element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[property='articleBody']")
                )
            )
            article_paragraphs = article_body_element.find_elements(By.TAG_NAME, "p")

            # Combine the text of all paragraphs to form the body text
            article_text = " ".join(paragraph.text for paragraph in article_paragraphs)

            # AI-powered Summary
            if premium:
                helper_obj.summarize_text(article_text)
            else:
                summary = "Get Premium for enabling AI-powered summary!"

            # Article classification
            classification = helper_obj.classify_article(article_text, keywords)

            # Insert the article data into the table
            helper_obj.insert_article_data(
                cursor,
                article_title,
                article_text,
                summary,
                classification,
                location,
                article,
            )
            conn.commit()

        except (NoSuchElementException, TimeoutException) as e:
            print(
                f"An error occurred while processing the article: {article}. Error: {e}"
            )

    conn.close()
    browser.quit()


if __name__ == "__main__":
    main()
