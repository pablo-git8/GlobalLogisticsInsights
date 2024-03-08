# cd to the app project
# python -m streamlit run app.py

import sqlite3
import random
import streamlit as st

from datetime import datetime


######## CSS ########

# Read the contents of the CSS file
with open('./css/styles.css', 'r') as f:
    css_to_include = f.read()

# Include the contents of the CSS file in the Streamlit app
st.markdown(f'<style>{css_to_include}</style>', unsafe_allow_html=True)


######## APP INITIALIZATION ########

# App title
st.title('Maritime & Air News Gatherer')

# App Image
with st.container():
    col1, col2, col3 = st.columns([2, 4, 2])
    # Display an image with a specified width, maintaining aspect ratio
    with col2:
        st.image('https://raw.githubusercontent.com/pablo-git8/GlobalLogisticsInsights/main/images/14c0ecef-68ef-4ce8-8bfe-bd63176ea5ef.png', width=320)

# Initialize session state variable if it doesn't exist
if 'show_text' not in st.session_state:
    st.session_state.show_text = True 

# Define a callback to hide the text
def hide_text():
    st.session_state.show_text = False

# Define the path to the SQLite database
db_path = '../data/news/maritime_air_news.db'

# Define table naming by date of execution
current_date = datetime.now().strftime("%m%d%Y")
#current_date = '03082024' # For testing purposes - cron jobs needed to keep the app updated

# Function to get news from the database based on the selected category
def get_news_data(option, classification, num_news):
    """
    """
    conn = sqlite3.connect(db_path)  # Update with your SQLite DB path
    cur = conn.cursor()

    # Determine the table name based on the option
    table_suffix = "air" if option == '✈️ Air News' else "mar"
    table_name = f"{table_suffix}_news_{current_date}"

    # Count the total news in the category
    cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE classification = ?", (classification,))
    count = cur.fetchone()[0]

    # Maximum number of news to select
    limit = num_news if count >= num_news else count

    # Then, fetch the limited number of news articles
    cur.execute(f"""
        SELECT title, text, summary, link
        FROM {table_name}
        WHERE classification = ? 
        LIMIT ?
    """, (classification, limit))

    # Get data
    data = cur.fetchall()
    conn.close()

    return data

def get_news_data_ml(option, ml_classification):
    """
    Fetches news data from the database based on BERT classification. 
    If no data is found for the classification, a random news entry is returned.
    """
    conn = sqlite3.connect(db_path)  # Update with your SQLite DB path
    cur = conn.cursor()

    # Determine the table name based on the option
    table_suffix = "air" if option == 1 else "mar"
    table_name = f"{table_suffix}_news_{current_date}"

    # Count the total news in the ml_classification
    cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE ml_classification = ?", (ml_classification,))
    count = cur.fetchone()[0]

    if count > 0:
        # If there is at least one row with the ml_classification, fetch one entry
        cur.execute(f"""
            SELECT title, text, summary, link
            FROM {table_name}
            WHERE ml_classification = ? 
            ORDER BY RANDOM() 
            LIMIT 1
        """, (ml_classification,))
    else:
        # If no rows have the ml_classification, select a random row from the table
        cur.execute(f"""
            SELECT title, text, summary, link
            FROM {table_name}
            ORDER BY RANDOM() 
            LIMIT 1
        """)

    # Get data
    data = cur.fetchone()
    conn.close()

    return data


######## CHOOSE NEWS SECTION (SIDEBAR) ########
        
# Sidebar Title
st.sidebar.title('News of Interest')

# Drop-down menu for choosing news transport
news_option = st.sidebar.radio(
    'Transport:',
    ('🚢 Maritime News', '✈️ Air News'))

# Drop-down menu for choosing news location
news_loc = st.sidebar.radio(
    'Location:',
    ('🌐 Global', '🌎 South America'))

# Drop-down menu for choosing news categories
news_cat = st.sidebar.selectbox(
    'Category:',
    ('Unclassified or Neutral', 'Regulations', 'Issues', 'Global Trade', 'Port Operations',
     'Shipping Market', 'Supply Chain', 'Customs', 'Regulations'))

# Select number of news to display
num_news = st.sidebar.slider('Number of News:', min_value=1, max_value=10, value=1)


######## NEWS OF INTEREST ########

# App section
st.markdown('<p class="centered-subheader">Selected News</p>', unsafe_allow_html=True)
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:1px solid red">', unsafe_allow_html=True)

# Display the text if the corresponding state is True
if st.session_state.show_text:
    st.markdown("<h4 style='margin-bottom:0px; color: #FFFFCC;'>👈 Select your news of interest...</h4>", unsafe_allow_html=True)


#### BUTTON DISPLAY NEWS! ####

# Button to trigger the display of the text
if st.sidebar.button('Display News!', on_click=hide_text):
    news_items = get_news_data(news_option, news_cat, num_news)
    if len(news_items) == 0:
        # Display a message if no news items were found
        st.markdown('<p class="notification">No news found today!</p>', unsafe_allow_html=True)
    else:
        for news_title, news_content, summary, link in news_items:
            # Container of news
            with st.container():
                col1, col2 = st.columns([7, 5])
                with col1:
                    # Make the news title a clickable link
                    st.markdown(f'<p class="subheader-font"><a href="{link}" target="_blank">{news_title}</a></p>', unsafe_allow_html=True)
                    with st.expander("Read More"):
                        st.markdown(f'<div class="quote">{news_content[:1300]}...</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="caption-code">🤖 {summary}</div>', unsafe_allow_html=True)


######## AI RECOMMENDED NEWS (3) ########

# App section
st.markdown('<p class="centered-subheader">AI Recommended News</p>', unsafe_allow_html=True)
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:1px solid red">', unsafe_allow_html=True)

# Container of Risk news
with st.container():
    # Risks
    random_option = random.choice([1, 2])
    news_title, news_content, summary, link = get_news_data_ml(random_option, ml_classification = 'risk')
    st.markdown('<p class="subheader-cat">Risks</p>', unsafe_allow_html=True)
    # Assign custom CSS class to the container
    col1, col2 = st.columns([7, 5])
    with col1:
        # Header for the news title
        st.markdown(f'<p class="subheader-font"><a href="{link}" target="_blank">{news_title}</a></p>', unsafe_allow_html=True)
        # Use an expander for displaying the news content
        with st.expander("Read More"):
            st.markdown(f'<div class="quote">{news_content[:1300]}...</div>', unsafe_allow_html=True)
    with col2:
        # Summary of the news title
        st.markdown(f'<div class="caption-code">🤖 {summary}</div>', unsafe_allow_html=True)

# Container of Opportunities News
with st.container():
    # Oportunities
    random_option = random.choice([1, 2])
    news_title, news_content, summary, link  = get_news_data_ml(random_option, ml_classification = 'opportunities')
    st.markdown('<p class="subheader-cat">Oportunities</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([7, 5])
    with col1:
        st.markdown(f'<p class="subheader-font"><a href="{link}" target="_blank">{news_title}</a></p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown(f'<div class="quote">{news_content[:1300]}...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="caption-code">🤖 {summary}</div>', unsafe_allow_html=True)

# Container of General news
with st.container():
    # General
    random_option = random.choice([1, 2])
    news_title, news_content, summary, link  = get_news_data_ml(random_option, ml_classification = 'neither')
    st.markdown('<p class="subheader-cat">General</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([7, 5])
    with col1:
        st.markdown(f'<p class="subheader-font"><a href="{link}" target="_blank">{news_title}</a></p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown(f'<div class="quote">{news_content[:1300]}...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="caption-code">🤖 {summary}</div>', unsafe_allow_html=True)


######## PREMIUM EXAMPLE SECTION #########

# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:0.1px black">', unsafe_allow_html=True)
# App section
st.markdown('<p class="subheader-premium">🔓 PREMIUM Example</p>', unsafe_allow_html=True)
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:0.5px solid #D4FFB2">', unsafe_allow_html=True)

text_example = \
    """
    The Red Sea has turned from one of the world's most important trade routes into a danger zone.
    Tensions in the region have been escalating since November, when Yemen-based Houthis started launching drone and missile attacks against ships transiting the Red Sea. The Shiite military group's attacks, meant to pressure Israel to stop its bombardment of Gaza, are leading to sustained delays and disruption in trade, along with surging shipping costs.
    An increasing number of companies that transport vital raw materials and fuels have suspended operations in the area. They are rerouting their ships an additional 3,500 nautical miles around the Cape of Good Hope in South Africa — the route the Suez Canal was built to circumvent in 1869.
    The Suez Canal is one of the most important trade routes in the world, accounting for around 10 percent of seaborne trade globally.
    Volume of goods that pass through the Suez Canal, as a share of global seaborne trade  between 2018 and 2023. Data extracted on Feb. 7, 2024.
    Shipping costs for routes transiting through the Suez Canal have also increased massively as a result of the violence in the region.
    The fastest alternative to transiting through the Red Sea is circumnavigating Africa through the Cape of Good Hope. A journey from Rotterdam to Singapore, which would take around 26 days through Suez, would be 10 to 14 days longer.
    """

summary_example = \
    """
    Los conflictos en el Mar Rojo han disparado costos y demoras en comercio, afectando rutas críticas como el Canal de Suez, esencial para el comercio internacional.
    
    **Impacto en LATAM:**

    La inestabilidad en el Mar Rojo podría repercutir en LATAM al incrementar los tiempos y costos de transporte marítimo, afectando negativamente las importaciones y exportaciones. Esta situación desafiaría las operaciones portuarias y la gestión eficiente de la cadena de suministro en la región, exigiendo a las empresas adoptar medidas para mitigar los retrasos y los aumentos en los costos de envío.
    """

# Container of news
with st.container():
    # Assign custom CSS class to the container
    col1, col2 = st.columns([7, 5])
    with col1:
        # Linl to project
        link_project = 'https://github.com/pablo-git8/GlobalLogisticsInsights'
        # Header for the news title
        st.markdown(f'<p class="subheader-font"><a href="{link_project}" target="_blank">Tensions in the Red Sea</a></p>', unsafe_allow_html=True)
        # Use an expander for displaying the news content
        with st.expander("Read More"):
            st.markdown(f'<div class="quote">{text_example}</div>', unsafe_allow_html=True)
    with col2:
        # Summary of the news title
        st.markdown(f'<div class="quote-test">🤖 AI-Powered Summary:</div>', unsafe_allow_html=True)
        st.write(f'')
        st.write(f'{summary_example}')

# Add a copyright notice at the bottom of the page
st.markdown("""
    <hr style="border:0.5px dash #f0f0f5;">
    <p style="text-align: center; color: grey;">
        &copy; 2024 Pablo-git8. All rights reserved.
    </p>
    """, unsafe_allow_html=True)