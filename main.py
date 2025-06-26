import os
from dotenv import load_dotenv
from format_email import format_html_email, format_plain_text_email
from services import get_weather_data, get_news_headlines, get_stocks_data, get_daily_quote, get_calendar_events, send_email
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Main function to gather all data and send the daily digest email
def send_daily_digest():
    # Gather all data
    if os.getenv("INCLUDE_WEATHER") == "True":
        weather = get_weather_data()
    else:
        weather = None
    
    if os.getenv("INCLUDE_NEWS") == "True":
        news = get_news_headlines()
    else:
        news = None
    
    if os.getenv("INCLUDE_STOCKS") == "True":
        stocks = get_stocks_data()
    else:
        stocks = None
    
    if os.getenv("INCLUDE_QUOTE") == "True":
        quote = get_daily_quote()
    else:
        quote = None
    
    if os.getenv("INCLUDE_CALENDAR") == "True":
        calendar = get_calendar_events()
    else:
        calendar = None

    html_content = format_html_email(weather, news, stocks, quote, calendar)
    plain_content = format_plain_text_email(weather, news, stocks, quote, calendar)
    
    # Send email
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"Daily Digest - {current_date}"
    send_email(subject, plain_content, html_content)

send_daily_digest()