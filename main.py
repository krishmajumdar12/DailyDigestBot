from format_email import format_html_email, format_plain_text_email
from services import get_weather_data, get_news_headlines, get_stocks_data, get_daily_quote, get_calendar_events, send_email
from datetime import datetime

# Main function to gather all data and send the daily digest email
def send_daily_digest():
    # Gather all data
    weather = get_weather_data()
    news = get_news_headlines()
    stocks = get_stocks_data()
    quote = get_daily_quote()
    calendar = get_calendar_events()
    html_content = format_html_email(weather, news, stocks, quote, calendar)
    plain_content = format_plain_text_email(weather, news, stocks, quote, calendar)
    
    # Send email
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    subject = f"Daily Digest - {current_date}"
    send_email(subject, plain_content, html_content)

send_daily_digest()