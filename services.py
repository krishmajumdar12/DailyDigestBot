import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, TrackingSettings, ClickTracking, Content
from dotenv import load_dotenv
import certifi
import requests
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pytz

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))
os.environ['SSL_CERT_FILE'] = certifi.where()
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Use SendGrid API to send daily digest email
def send_email(subject, plain_content, html_content=None):
    message = Mail(
        from_email=os.getenv("FROM_EMAIL"),
        to_emails=os.getenv("TO_EMAIL"),
        subject=subject
    )
    
    if html_content:
        message.add_content(Content("text/plain", plain_content))
        message.add_content(Content("text/html", html_content))
    else:
        message.add_content(Content("text/plain", plain_content))
    
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
    key = os.getenv("WEATHER_API_KEY", "")
    city = os.getenv("CITY", "")
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
        icon = current.get("icon", "")
        
        # Return structured data for better formatting
        return {
            "city": city,
            "temp": temp,
            "tempmin": tempmin,
            "tempmax": tempmax,
            "conditions": conditions,
            "summary": summary,
            "icon": icon
        }
    
    except Exception as e:
        return {"error": f"Error retrieving weather data: {e}"}
    
# Using GNews API to get daily news headlines with images
def get_news_headlines():
    key = os.getenv("GNEWS_API_KEY", "")
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
        articles_data = res.json().get("articles", [])

        if not articles_data:
            return {"articles": [], "error": "No news articles found."}

        articles = []
        for article in articles_data:
            processed_article = {
                "title": article.get("title", ""),
                "url": article.get("url", ""),
                "image": article.get("image", ""),
                "description": article.get("description", ""),
                "source": article.get("source", {}).get("name", "Unknown Source"),
                "publishedAt": article.get("publishedAt", "")
            }
            articles.append(processed_article)

        return {"articles": articles}
    
    except Exception as e:
        return {"articles": [], "error": f"Error retrieving news: {e}"}
 
# Using Finnhub API to get daily stock info with company logos
def get_stocks_data():
    key = os.getenv("FINNHUB_API_KEY", "")
    stocks = os.getenv("STOCK_SYMBOLS", "NVDA").split(",")
    stock_data = []

    for stock in stocks:
        try:
            # Get stock quote data
            quote_url = f"https://finnhub.io/api/v1/quote?symbol={stock.strip()}&token={key}"
            quote_res = requests.get(quote_url)
            quote_data = quote_res.json()
            
            current = quote_data.get("c") # current price
            change = quote_data.get("d") # price change
            pct = quote_data.get("dp") # percent change

            # Get company profile for logo
            profile_url = f"https://finnhub.io/api/v1/stock/profile2?symbol={stock.strip()}&token={key}"
            profile_res = requests.get(profile_url)
            profile_data = profile_res.json()
            
            logo_url = profile_data.get("logo", "")

            if current:
                stock_data.append({
                    "symbol": stock.strip(),
                    "price": current,
                    "change": change,
                    "percent_change": pct,
                    "logo": logo_url
                })
            else:
                stock_data.append({
                    "symbol": stock.strip(),
                    "logo": logo_url,
                    "error": "Price data not available"
                })

        except Exception as e:
            stock_data.append({
                "symbol": stock.strip(),
                "company_name": stock.strip(),
                "logo": "",
                "error": f"Error retrieving data: {e}"
            })

    return {"stocks": stock_data}

# Use ZenQuotes API for daily quote
def get_daily_quote():
    try:
        res = requests.get("https://zenquotes.io/api/today")
        data = res.json()
        quote = data[0]["q"]
        author = data[0]["a"]
        return {
            "quote": quote,
            "author": author
        }
    except Exception as e:
        return {"error": f"Error retrieving quote: {e}"}

# Using Google Calendar API to get daily events
def get_calendar_events():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
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
    
    formatted_events = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start_time = datetime.fromisoformat(start).strftime("%I:%M %p")
        formatted_events.append({
            "time": start_time,
            "title": event['summary']
        })

    return {"events": formatted_events}

def get_weather_icon(icon, conditions):
    # Get weather icon based on icon or conditions
    weather_icons = {
        "clear-day": "☀️",
        "clear-night": "🌙",
        "rain": "🌧️",
        "snow": "❄️",
        "sleet": "🌨️",
        "wind": "💨",
        "fog": "🌫️",
        "cloudy": "☁️",
        "partly-cloudy-day": "⛅",
        "partly-cloudy-night": "☁️"
    }
    
    # Try icon first, then fallback to conditions
    if icon in weather_icons:
        return weather_icons[icon]
    
    conditions_lower = conditions.lower()
    if "clear" in conditions_lower:
        return "☀️"
    elif "rain" in conditions_lower:
        return "🌧️"
    elif "snow" in conditions_lower:
        return "❄️"
    elif "cloud" in conditions_lower:
        return "☁️"
    elif "fog" in conditions_lower:
        return "🌫️"
    else:
        return "🌤️"

# Helper function to validate image URLs
def is_valid_image_url(url):
    # Check if URL is valid and likely an image
    if not url:
        return False
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        return False
    
    # Check for common image extensions
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')
    url_lower = url.lower()
    
    # Either has image extension or is from known image hosting services
    has_image_extension = any(url_lower.endswith(ext) for ext in image_extensions)
    is_image_service = any(service in url_lower for service in ['imgur', 'cloudinary', 'amazonaws', 'googleusercontent'])
    
    return has_image_extension or is_image_service