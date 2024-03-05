# cd to the app project
# python -m streamlit run app.py

import streamlit as st

######## CSS ########

# Read the contents of the CSS file
with open('./css/styles.css', 'r') as f:
    css_to_include = f.read()

# Include the contents of the CSS file in the Streamlit app
st.markdown(f'<style>{css_to_include}</style>', unsafe_allow_html=True)


######## APP PRESENTATION ########

# App title
st.title('Maritime & Air News Gatherer')

with st.container():
    col1, col2, col3 = st.columns([2, 4, 2])
    # Display an image with a specified width, maintaining aspect ratio
    with col2:
        st.image('https://raw.githubusercontent.com/pablo-git8/GlobalLogisticsInsights/main/images/mar_air_transport.png', width=300)


######## URGET NEWS SECTION (5 NEWS) ########
        
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:0.1px black">', unsafe_allow_html=True)
# App section
#st.subheader('🚨 Urgent Issues in Maritime / Air Transport 🚨')
st.markdown('<p class="centered-subheader">🚨 Urgent Issues in Maritime / Air Transport 🚨</p>', unsafe_allow_html=True)
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:1px solid #D4FFB2">', unsafe_allow_html=True)

# TODO - Get 5 news tagged as issues, regulations, etc.

# Container of news 1
with st.container():
    # Assign custom CSS class to the container
    col1, col2 = st.columns([6, 6])
    with col1:
        # Header for the news title
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        # Use an expander for displaying the news content
        with st.expander("Read More"):
            st.markdown('<div class="quote">Display regulation news...</div>', unsafe_allow_html=True)
    with col2:
        # Summary of the news title
        st.markdown('<div class="caption-code">Get Premium for enabling AI-powered summary!</div>', unsafe_allow_html=True)

# Container of news 2
with st.container():
    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown('<div class="quote">Display regulation news...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="caption-code">Get Premium for enabling AI-powered summary!</div>', unsafe_allow_html=True)

# Container of news 3
with st.container():
    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown('<div class="quote">Display regulation news...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="caption-code">Get Premium for enabling AI-powered summary!</div>', unsafe_allow_html=True)

# Container of news 4
with st.container():
    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown('<div class="quote">Display regulation news...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="caption-code">Get Premium for enabling AI-powered summary!</div>', unsafe_allow_html=True)

# Container of news 5
with st.container():
    col1, col2 = st.columns([6, 6])
    with col1:
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        with st.expander("Read More"):
            st.markdown('<div class="quote">Display regulation news...</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="caption-code">Get Premium for enabling AI-powered summary!</div>', unsafe_allow_html=True)


######## CHOOSE NEWS SECTION ########
        
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:0.1px black">', unsafe_allow_html=True)
# App section
st.subheader('Choose News of Interest')
# Insert custom HTML to create a horizontal line separator
st.markdown('<hr style="border:0.5px solid #D4FFB2">', unsafe_allow_html=True)

# Drop-down menu for choosing news transport
news_option = st.selectbox(
    'Choose transport:',
    ('🚢 Maritime News', '✈️ Air News'))

# Drop-down menu for choosing news category
news_cat = st.selectbox(
    'Choose category:',
    ('🌐 Global', '🌎 South America'))

# Button to trigger the display of the text
if st.button('Display News!'):

    # Maritime news
    if news_option == 'Maritime News':
        # Global maritime news
        if news_cat == 'Global':
            # Container of news
            with st.container():
                # Header for the news title
                st.subheader('Global Maritime News Title')
                # Use an expander for displaying the news content
                with st.expander("View Global Maritime News"):
                    st.write('Displaying Global Maritime News...')
                # Summary of the news title
                st.caption('Global Maritime News Title Summary')

        # South America maritime news
        if news_cat == 'South America':
            st.write('South America Maritime News Title')
            st.write('Displaying South America Maritime News...')
            st.write('South America Maritime News Title Summary')

    # Air news
    elif news_option == 'Air News':
        if news_cat == 'Global':
            st.write('Global Air News Title')
            st.write('Displaying Global Air News...')
            st.write('Air Maritime News Title Summary')
        if news_cat == 'South America':
            st.write('South America Air News Title')
            st.write('Displaying South America Air News...')
            st.write('South America Air News Title Summary')


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
    col1, col2 = st.columns([6, 6])
    with col1:
        # Header for the news title
        st.markdown('<p class="subheader-font">Tensions in the Red Sea</p>', unsafe_allow_html=True)
        # Use an expander for displaying the news content
        with st.expander("Read More"):
            st.markdown(f'<div class="quote">{text_example}</div>', unsafe_allow_html=True)
    with col2:
        # Summary of the news title
        st.markdown(f'<div class="quote-test">🤖 AI-Powered Summary:</div>', unsafe_allow_html=True)
        st.write(f'')
        st.write(f'{summary_example}')
