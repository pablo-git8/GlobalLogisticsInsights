import json
import time
import openai
import sqlite3

from datetime import datetime
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Load the variables from .env into the environment
load_dotenv()

# Maritime news website 1
URL = "https://www.seatrade-maritime.com/"

# Define the path to the SQLite database
db_path = "../data/news/maritime_news.db"
# Define table naming by date of execution
current_date = datetime.now().strftime("%m%d%Y")
mar_news_table_name = f"mar_news_{current_date}"

# Load keywords from JSON file for classification
with open("../json/keywords.json", "r") as file:
    keywords = json.load(file)


# Establishes a connection to the SQLite database
def connect_to_db(db_path):
    """ """
    return sqlite3.connect(db_path)


# Create a new table for storing only daily articles
def create_daily_news_table(cursor, table_name):
    """ """
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        text TEXT,
                        summary TEXT,
                        classification TEXT,
                        location TEXT,
                        link TEXT
                    );"""
    )


def initialize_tables():
    """ """
    # Establish a connection and create a cursor
    conn = connect_to_db(db_path)
    cursor = conn.cursor()

    # Create tables for today's date with news
    create_daily_news_table(cursor, mar_news_table_name)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def summarize_text(text):
    """ """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"""
Please summarize the key points of the article for a business audience in a concise paragraph, limiting the summary to no more than 350 characters. Then, in a separate paragraph of 500 characters, elaborate on the potential impact of the situation described in the article on maritime logistics, port operations, and supply chain management, specifically focusing on its implications for Latin America. Label this second paragraph 'Impacto en LATAM:' and ensure there is a clear separation between the two sections. Present your response in Spanish and format it as markdown text for clarity:\n\n{text}
                """,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()


def insert_article_data(
    cursor,
    table_name,
    article_title,
    article_text,
    summary,
    classification,
    location,
    link,
):
    """ """
    # Check if an article with the same title already exists
    cursor.execute(f"SELECT id FROM {table_name} WHERE title = ?", (article_title,))
    existing_article = cursor.fetchone()

    if existing_article == None:
        cursor.execute(
            f"""INSERT INTO {table_name} (title, text, summary, classification, location, link)
                        VALUES (?, ?, ?, ?, ?, ?);""",
            (article_title, article_text, summary, classification, location, link),
        )


def classify_article(article_text, keywords):
    """ """
    max_count = 0
    max_category = "Unclassified or Neutral"

    # Convert article text to lower case for comparison
    article_text_lower = article_text.lower()

    # Check for the presence of each keyword in the article
    for category, category_keywords in keywords.items():
        count = sum(keyword in article_text_lower for keyword in category_keywords)
        if count > max_count:
            max_count = count
            max_category = category

    return max_category


def main():
    """ """
    conn = connect_to_db(db_path)
    cursor = conn.cursor()
    # Initialize DDBB and create tables
    initialize_tables()

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
        article_text = browser.find_element(
            By.CSS_SELECTOR, "div[itemprop='articleBody']"
        ).text

        premium = False

        if premium:
            summary = summarize_text(article_text)
        else:

            summary = "Get Premium for enabling AI-powered summary!"

        classification = classify_article(article_text, keywords)
        insert_article_data(
            cursor,
            mar_news_table_name,
            article_title,
            article_text,
            summary,
            classification,
            location,
            article_url,
        )
    conn.commit()
    conn.close()
    browser.quit()
