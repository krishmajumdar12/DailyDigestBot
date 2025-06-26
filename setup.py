from setuptools import setup

setup(
    name="DailyDigestBot",
    version="1.0.0",
    description="A Python bot that sends daily digest emails with weather, news, stocks, quotes, and calendar events.",
    author="Krish Majumdar",
    py_modules=["main", "services", "format_email"],
    install_requires=[
        "requests",
        "python-dotenv",
        "sendgrid",
        "google-api-python-client",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "pytz",
        "certifi",
    ],
    python_requires=">=3.8",
)
