# DailyDigestBot

A Python automated script that sends you a personalized daily digest email containing weather updates, news headlines, stock information, daily quotes, and your Google Calendar events.

## Overview

DailyDigestBot gathers data from multiple APIs and sends you a nicely formatted daily email summary. You can customize when to receive the email via your crontab and which services to include in the digest via environment variables.

---

## Features

- **Weather:** Current weather and forecast from Visual Crossing Weather API  
- **News:** Latest headlines from GNews API  
- **Stocks:** Real-time stock info from Finnhub API  
- **Quote:** Daily quotes from ZenQuotes 
- **Calendar:** Events from your Google Calendar  

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/krishmajumdar12/DailyDigestBot.git
cd DailyDigestBot
```

### 2. Create and Activate a Python Virtual Environment (Optional but Recommended)

Using a virtual environment helps isolate your project's dependencies and avoid conflicts with other Python projects on your system. While this step is optional, it is highly recommended.

To create and activate a virtual environment, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

After activating your virtual environment (or if you prefer to install packages globally), install the required dependencies by running:

```bash
pip install -e .
```

### 4. Create Your `.env` File

The `.env` file stores your configuration variables and API keys. It allows the bot to access the necessary services securely.

In the root of your project, create a file named `.env` and add the following content:

```env
# Which services to include in your daily digest (True/False)
INCLUDE_WEATHER=True
INCLUDE_NEWS=True
INCLUDE_STOCKS=True
INCLUDE_QUOTE=True
INCLUDE_CALENDAR=True

# SendGrid Email API settings
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=your_verified_sendgrid_email@example.com
TO_EMAIL=your_recipient_email@example.com

# Visual Crossing Weather API
WEATHER_API_KEY=your_visualcrossing_api_key_here
CITY=your_city

# GNews API
GNEWS_API_KEY=your_gnews_api_key_here
NUM_HEADLINES=5 # Optional

# Finnhub Stock API
FINNHUB_API_KEY=your_finnhub_api_key_here
STOCK_SYMBOLS="NVDA,AAPL,GOOG,TSLA,AMZN"

# Google Calendar API
GOOGLE_CREDENTIALS_FILE=credentials.json
```

Note: You can comment out API key lines for services you opt out of by setting their corresponding `INCLUDE_` variable to `False`, as the API keys won’t be needed in that case.

### How to Get API Keys for Each Service

- **SendGrid:**  
  Sign up at [https://sendgrid.com/](https://sendgrid.com/), create an API key in the dashboard, and verify your sender email address.

- **Visual Crossing Weather:**  
  Create a free account at [https://www.visualcrossing.com/weather-api](https://www.visualcrossing.com/weather-api) and obtain your API key from your account settings.

- **GNews:**  
  Register at [https://gnews.io/](https://gnews.io/) to get a free API key that allows you to fetch news headlines.

- **Finnhub:**  
  Sign up for a free account at [https://finnhub.io/](https://finnhub.io/) and generate your stock data API key.

- **Google Calendar:**  
  Follow the official Google Developers guide to create OAuth credentials and download your `credentials.json` file:  
  [Google Calendar API Quickstart](https://developers.google.com/calendar/api/quickstart/python)

---

Remember to keep your API keys private and **never** commit them to public repositories.

### 5. (Optional) Automate with Cron to Send Daily Emails

If you want the bot to send your daily digest automatically every day at 7:00 AM PST, you can add it to your system’s crontab (Linux/macOS):

1. Open your crontab editor:

```bash
crontab -e
```

2. Add the following lines (update paths as needed):

```bash
CRON_TZ=America/Los_Angeles
0 7 * * * cd /path/to/DailyDigestBot && /path/to/venv/bin/python main.py
```

Replace /path/to/DailyDigestBot with your actual project directory path.

Replace /path/to/venv/bin/python with your Python interpreter path inside the virtual environment (or system Python if not using venv).

Output and errors will be logged to cron.log for troubleshooting.

To adjust the cron job time and timezone, change the 0 7 * * * part to your desired minute/hour (cron uses 24-hour military time format for scheduling) and update CRON_TZ=America/Los_Angeles to your preferred timezone.

## Important Notes

- **Spam Folder:** The first few emails you send may end up in your recipient’s spam or junk folder. Mark them as “Not Spam” to improve deliverability over time.  
- **API Keys:** Keep your API keys and credentials private and **never** commit them to a public repository. Use the `.env` file and add it to `.gitignore`.  
- **SendGrid `FROM_EMAIL`:** The sender email must be verified in your own SendGrid account for emails to be sent successfully.  

---

## License

This project is for **personal use only** and is **not currently open source**.

---

## Contributing

Contributions and pull requests are not accepted at this time.

---

## Contact

For questions or feedback, please contact krishmajumdar12@gmail.com.

---

Thank you for using DailyDigestBot!  
Happy coding and stay informed every day! 🚀
