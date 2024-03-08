# **AI-Powered Supply Chain News Aggregator and Analyzer**

![python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-F9AB00?style=for-the-badge&logo=HuggingFace&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=OpenAI&logoColor=white)
![markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![terminal](https://img.shields.io/badge/windows%20terminal-4D4D4D?style=for-the-badge&logo=windows%20terminal&logoColor=white)

<p align="center">
	<img src="https://raw.githubusercontent.com/pablo-git8/GlobalLogisticsInsights/main/images/14c0ecef-68ef-4ce8-8bfe-bd63176ea5ef.png" alt="200" width="300"/>
</p>

## **Overview**

This Streamlit application is an AI-powered reporting tool designed to transform the responsiveness and strategic decision-making capabilities of supply chain managers. By using NLP and AI integration, it provides predictive insights into maritime/air logistics and supply chain disruptions through real-time global news aggregation.

## **Features**

### Real-Time News Aggregation

The application aggregates news from three sources in the air and maritime transport sectors:

- [Air Cargo News](https://www.aircargonews.net/)
- [Maritime Logistics Professional](https://www.maritimelogisticsprofessional.com)
- [Seatrade Maritime](https://www.seatrade-maritime.com/)

### Automated News Scraping

We have developed daily scripts that scrape these websites to gather the most relevant news of the day. This ensures our users always have access to the latest information:

- `scripts/maritime_page_1.py`
- `scripts/maritime_page_1_latam.py`
- `scripts/air_page_1.py`
- `scripts/air_page_1_latam.py`
- `scripts/air_page_2.py`
- `scripts/air_page_2_latam.py`

### Modular Codebase

The `scripts/src.py` file includes helper functions that facilitate modularization of the application. It covers functionalities such as:

- Connecting to an SQLite database
- Database initialization
- Text summarization, translation to spanish and business context via the OpenAI API
- Simple news text classification by mapping words to a JSON file
- Advanced news text classification using a Hugging Face BERT model fine-tuned for news classification

### Interactive User Interface

The Streamlit app provides a user-friendly interface where users can:

- Select the type of transport: '🚢 Maritime' or '✈️ Air'
- Choose the geographical focus: '🌐 Global', '🌎 South America'
- Choose the topic of news articles: 'Regulation', 'Issues', 'Supply Chain', etc.
- Decide the number of news articles to display, ranging from 1 to 10

### Hugging Face Model Integration

Utilizing the [Hugging Face BERT model](https://huggingface.co/spaces/manideepvemula/supply-chain/tree/main/riskclassification_finetuned_xlnet_model_ld), the application categorizes news and provides 3 recommendations based on the day's classifications ('Risks', 'Opportunities' and 'General').

### Comprehensive Display

For each news article, the application main page displays:

- The title
- The text content
- A link to the full article

### Premium Features

The premium layer of the application offers:

- Summaries of news articles translated into Spanish
- Concise key point summaries for a business audience limited to 350 characters
- In-depth analysis of the article's impact on maritime logistics, port operations, and supply chain management, with a specific focus on Latin America labeled `Impacto en LATAM`, limited to 500 characters

## Technical Details

### Frontend Development

The frontend of the application is built using Streamlit coupled with custom CSS for styling.

### Notebook Documentation

The included Jupyter notebooks document all development tests, especially focusing on web scraping logic and utilization of the BERT model:

- `notebooks/maritime_scrapping_1.ipynb`
- `notebooks/bert_model.ipynb`

## Getting Started

To run the application on your local machine:

1. Clone the repository:
   ```sh
   git clone https://github.com/pablo-git8/GlobalLogisticsInsights.git
   ```

2. Navigate to the cloned directory and install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Start the Streamlit server:
   ```sh
   python -m streamlit run news_app/app.py
   ```

## Contribution

We welcome contributions from the community.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Contact

If you have any questions or comments about the application, please open an issue in this repository.