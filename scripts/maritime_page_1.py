# Imports
import os
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
URL = "https://www.maritimelogisticsprofessional.com"

# Define the path to the SQLite database
db_path = '../data/news/maritime_news.db'
# Define table naming by date of execution
current_date = datetime.now().strftime("%m%d%Y")
mar_news_table_name = f"mar_news_{current_date}"

# Load keywords from JSON file for classification
with open('../json/keywords.json', 'r') as file:
    keywords = json.load(file)


# Establishes a connection to the SQLite database
def connect_to_db(db_path):
    """
    """
    return sqlite3.connect(db_path)


# Create a new table for storing only daily articles
def create_daily_news_table(cursor, table_name):
    """
    """
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        text TEXT,
                        summary TEXT,
                        classification TEXT,
                        location TEXT,
                        link TEXT
                    );""")


def initialize_tables():
    """
    """
    # Establish a connection and create a cursor
    conn = connect_to_db(db_path)
    cursor = conn.cursor()

    # Create tables for today's date with news
    create_daily_news_table(cursor, mar_news_table_name)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def summarize_text(text):
    """
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt= f"""
Please summarize the key points of the article for a business audience in a concise paragraph, limiting the summary to no more than 350 characters. Then, in a separate paragraph of 500 characters, elaborate on the potential impact of the situation described in the article on maritime logistics, port operations, and supply chain management, specifically focusing on its implications for Latin America. Label this second paragraph 'Impacto en LATAM:' and ensure there is a clear separation between the two sections. Present your response in Spanish and format it as markdown text for clarity:\n\n{text}
                """,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()


def insert_article_data(cursor, table_name, article_title, article_text, summary, classification, location, link):
    """
    """
    # Check if an article with the same title already exists
    cursor.execute(f"SELECT id FROM {table_name} WHERE title = ?", (article_title,))
    existing_article = cursor.fetchone()

    if existing_article == None:
        cursor.execute(f"""INSERT INTO {table_name} (title, text, summary, classification, location, link)
                        VALUES (?, ?, ?, ?, ?, ?);""",
                    (article_title, article_text, summary, classification, location, link))

def classify_article(article_text, keywords):
    """
    """
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
    """
    """
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
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Ok']"))
        )
        # Click the button once it is clickable
        browser.find_element(By.XPATH, "//button[text()='Ok']").click()
    except (NoSuchElementException, TimeoutException):
        print("The cookie acceptance button was not found on the page.")

    # GLOBAL NEWS
    location = "Global"

    # List of latest global news
    latest_news = browser.find_elements(By.CLASS_NAME, "snippet-flex")
    # Collect all URLs before navigating
    article_urls = [element.get_attribute('href') for element in latest_news if '/news/' in element.get_attribute('href')]
    # Premium version
    premium = False

    # Establish a connection and create a cursor
    conn = connect_to_db(db_path)
    cursor = conn.cursor()

    # Iterate through global news
    for article in article_urls:
        """
        """
        # Get article
        time.sleep(5)
        browser.get(article)

        # Find the title element and get the text
        title_element = browser.find_element(By.CSS_SELECTOR, "h1[itemprop='name']")
        article_title = title_element.text
        print(article_title)

        # Find the article body element and get all the paragraph texts
        article_body_element = browser.find_element(By.CSS_SELECTOR, "div[property='articleBody']")
        article_paragraphs = article_body_element.find_elements(By.TAG_NAME, "p")

        # Combine the text of all paragraphs to form the body text
        article_text = " ".join(paragraph.text for paragraph in article_paragraphs)

        # AI-powered Summary
        if premium:
            summarize_text(article_text)
        else:
            # Summary not premium
            summary = "Get Premium for enabling AI-powered summary!"
        
        # Article classification
        classification = classify_article(article_text, keywords)

        # Insert the article data into the table
        insert_article_data(cursor, mar_news_table_name, article_title, article_text, summary, classification, location, article)
        conn.commit() # Commit the changes

    # Close connection
    conn.close()
    browser.quit()


if __name__ == '__main__':
    main()
