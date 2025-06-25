import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking
from dotenv import load_dotenv
import certifi
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

load_dotenv()
os.environ['SSL_CERT_FILE'] = certifi.where()
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Use SendGrid API to send daily digest email
def send_email(subject, content):
    message = Mail(
        from_email = os.getenv("FROM_EMAIL"),
        to_emails = os.getenv("TO_EMAIL"),
        subject = subject,
        plain_text_content = content
    )
    # Disable SendGrid click tracking
    tracking_settings = TrackingSettings()
    tracking_settings.click_tracking = ClickTracking(enable=False, enable_text=False)
    message.tracking_settings = tracking_settings

    try:
        sendgrid = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sendgrid.send(message)
        print(f"Email sent! Status: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Use VisualCrossing API to get daily weather info
def get_weather_data():
    key = os.getenv("WEATHER_API_KEY")
    city = os.getenv("CITY")
    city_url = city.replace(" ", "%20")
    request_url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{city_url}/today?unitGroup=us&key={key}&include=current&contentType=json"
    )

    try:
        res = requests.get(request_url)
        data = res.json()
        current = data.get("currentConditions", {})
        temp = current.get("temp")
        today = data['days'][0]
        summary = today['description']
        tempmax = today['tempmax']
        tempmin = today['tempmin']
        conditions = today['conditions']
        return f"Current weather in {city}: {temp}°F, with a low of {tempmin}°F and a high of {tempmax}°F. {conditions}. {summary}"
    
    except Exception as e:
        return f"Error retrieving weather data: {e}"
    
# Using GNews API to get daily news headlines
def get_news_headlines():
    key = os.getenv("GNEWS_API_KEY")
    topic = os.getenv("NEWS_TOPIC", "") # Optionally adjust topic
    max_headlines = int(os.getenv("NUM_HEADLINES", 3)) # Optionally adjust how many headlines appear

    
    request_url = (
        f"https://gnews.io/api/v4/top-headlines?"
        f"token={key}&lang=en&max={max_headlines}"
    )
    if topic:
        request_url += f"&topic={topic}"

    try:
        res = requests.get(request_url)
        articles = res.json().get("articles", [])

        if not articles:
            return "No news articles found."

        result = "Top News Headlines:\n"
        for article in articles:
            title = article["title"]
            link = article["url"]
            result += f"- {title}\n  ({link})\n"
        return result
    
    except Exception as e:
        return f"Error retrieving news: {e}"
 
# Using Finnhub API to get daily stock info
def get_stocks_data():
    key = os.getenv("FINNHUB_API_KEY")
    stocks = os.getenv("STOCK_SYMBOLS", "DOW").split(",")
    result = "Stock Prices:\n"

    for stock in stocks:
        try:
            request_url = f"https://finnhub.io/api/v1/quote?symbol={stock.strip()}&token={key}"
            res = requests.get(request_url)
            data = res.json()
            current = data.get("c") # current price
            change = data.get("d") # price change
            pct = data.get("dp") # percent change

            if current:
                arrow = "🔺" if change > 0 else "🔻" if change < 0 else "⏸"
                result += f"{stock.strip()}: ${current:.2f} {arrow} ({pct:.2f}%)\n"
            else:
                result += f"{stock.strip()}: Data not available\n"

        except Exception as e:
            result += f"{stock.strip()}: Error retrieving data: {e}\n"

    return result

# Use ZenQuotes API for daily quote
def get_daily_quote():
    try:
        res = requests.get("https://zenquotes.io/api/today")
        data = res.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return f"Quote of the Day:\n\"{quote}\"\n– {author}"
    except Exception as e:
        return f"Error retrieving key: {e}"

# Using Google Calendar API to get daily events
def get_calendar_events():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh()
        else:
            credentials_file = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    service = build('calendar', 'v3', credentials=credentials)
    pacific = pytz.timezone("America/Los_Angeles")
    now = datetime.now(pacific).isoformat()
    end_of_day = (datetime.now(pacific) + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    ).isoformat()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        timeMax=end_of_day,
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        return "No events today."

    result = "Today’s Events:\n"
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.fromisoformat(start).strftime("%I:%M %p")
        result += f"- {start_time}: {event['summary']}\n"

    return result

# Testing
if __name__ == "__main__":
    send_email("Daily Digest", get_calendar_events())
