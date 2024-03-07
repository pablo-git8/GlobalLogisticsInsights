import time
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

# Load the variables from .env into the environment
load_dotenv()

# Maritime news website 1
URL = "https://www.maritimelogisticsprofessional.com"

# Path to the SQLite database
db_path = "data/news/maritime_air_news.db"
# Table naming by date of execution and type of news
current_date = datetime.now().strftime("%m%d%Y")
mar_news_table_name = f"mar_news_{current_date}"

helper_obj = Helper(db_path, mar_news_table_name)

# Load keywords from JSON file for classification
with open("json/keywords.json", "r") as file:
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

    # LATAM NEWS
    location = "LATAM"
    print(f"\nGetting {location} news...")

    # Connect to DDBB
    conn = helper_obj.connect_to_db()
    cursor = conn.cursor()
    premium = False
    # Go back to main page
    browser.get(URL)

    # Filter for LATAM
    filter_news = "/south-america"
    try:
        # Category links to find LATAM
        cat_links = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cat-link"))
        )

        latam_link = None
        for cat_link_div in cat_links:
            a_element = cat_link_div.find_element(By.TAG_NAME, "a")
            href = a_element.get_attribute("href")
            if href.endswith(filter_news):
                latam_link = href
                break  # Exit the loop once we find the LATAM link

        # Check if the LATAM link was found before proceeding
        if latam_link:
            # Navigate to the LATAM link
            browser.get(latam_link)
            # Get snippets
            snippets = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".snippet"))
            )
            
            snippet_url = [snippet.get_attribute("href") for snippet in snippets]

            # Process each snippet
            for news_link in snippet_url:
                # news_link = snippet_url[0]
                try:
                    time.sleep(5)
                    browser.get(news_link)
    
                    # Find the title element and get the text
                    title_element = wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1[itemprop='name']"))
                    )
                    news_title = title_element.text
                    print(news_title)
        
                    # Find the article body element and get all the paragraph texts
                    article_body_element = wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div[property='articleBody']")
                        )
                    )
                    article_paragraphs = article_body_element.find_elements(By.TAG_NAME, "p")
        
                    # Combine the text of all paragraphs to form the body text
                    news_text = " ".join(paragraph.text for paragraph in article_paragraphs)
                    article_date = browser.find_element(
                        By.CSS_SELECTOR, "span[class='date']"
                    ).text
                    date_object = datetime.strptime(article_date, '%B %d, %Y')
            
            
            
# =============================================================================
#                     news_link = snippet.get_attribute("href")
#                     news_title = snippet.find_element(By.TAG_NAME, "h2").text
#                     news_text = snippet.find_element(By.TAG_NAME, "p").text
# =============================================================================

                    # AI-powered Summary
                    if premium:
                        helper_obj.summarize_text(news_text)
                    else:
                        summary = "Get Premium for enabling AI-powered summary!"

                    # Article classification
                    classification = helper_obj.classify_article(news_text, keywords)
                    # Machine learning classification
                    ml_classification = helper_obj.ml_classification(news_text)

                    # Insert the article data into the table
                    helper_obj.insert_article_data(
                        cursor,
                        news_title,
                        news_text,
                        summary,
                        classification,
                        ml_classification,
                        location,
                        news_link,
                        date_object
                    )
                    print(news_title)
                    conn.commit()

                except NoSuchElementException:
                    print("An element was not found while processing a snippet.")
        else:
            print("LATAM link was not found")

    except TimeoutException:
        print("Failed to load the necessary elements for LATAM news scraping.")

    # Close connection and quit the browser
    conn.close()
    browser.quit()


if __name__ == "__main__":
    main()
