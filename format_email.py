from datetime import datetime
from services import get_weather_icon

def format_html_email(weather, news, stocks, quote, calendar):
    # Format all data into HTML email
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="light dark">
        <title>Daily Digest</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            :root {{
                --bg-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                --bg-secondary: rgba(255, 255, 255, 0.95);
                --bg-section: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0.6) 100%);
                --bg-item: rgba(255,255,255,0.4);
                --bg-item-hover: rgba(255,255,255,0.6);
                --bg-detail: rgba(255,255,255,0.6);
                --text-primary: #1a1a1a;
                --text-secondary: #64748b;
                --text-muted: #475569;
                --text-dark: #1e293b;
                --border-color: rgba(255,255,255,0.2);
                --border-section: rgba(255,255,255,0.3);
                --border-item: rgba(255,255,255,0.4);
                --border-subtle: rgba(226,232,240,0.6);
                --shadow-light: rgba(0,0,0,0.08);
                --shadow-medium: rgba(0,0,0,0.15);
                --quote-accent: rgba(102,126,234,0.3);
                --error-bg: rgba(220, 38, 38, 0.05);
                --error-border: rgba(220, 38, 38, 0.1);
            }}
            
            @media (prefers-color-scheme: dark) {{
                :root {{
                    --bg-primary: linear-gradient(135deg, #4c63d2 0%, #5a4fcf 100%);
                    --bg-secondary: rgba(20, 24, 35, 0.95);
                    --bg-section: linear-gradient(135deg, rgba(30,35,50,0.9) 0%, rgba(40,45,65,0.8) 100%);
                    --bg-item: rgba(45,52,70,0.6);
                    --bg-item-hover: rgba(55,62,85,0.8);
                    --bg-detail: rgba(60,67,90,0.7);
                    --text-primary: #f8fafc;
                    --text-secondary: #94a3b8;
                    --text-muted: #cbd5e1;
                    --text-dark: #e2e8f0;
                    --border-color: rgba(255,255,255,0.1);
                    --border-section: rgba(255,255,255,0.15);
                    --border-item: rgba(255,255,255,0.2);
                    --border-subtle: rgba(71,85,105,0.4);
                    --shadow-light: rgba(0,0,0,0.25);
                    --shadow-medium: rgba(0,0,0,0.4);
                    --quote-accent: rgba(102,126,234,0.5);
                    --error-bg: rgba(220, 38, 38, 0.15);
                    --error-border: rgba(220, 38, 38, 0.3);
                }}
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                line-height: 1.6;
                color: var(--text-primary);
                max-width: 680px;
                margin: 0 auto;
                background: var(--bg-primary);
                padding: 40px 20px;
                min-height: 100vh;
            }}
            .container {{
                background: var(--bg-secondary);
                backdrop-filter: blur(20px);
                padding: 40px;
                border-radius: 24px;
                box-shadow: 0 20px 40px var(--shadow-medium), 0 0 0 1px var(--border-color);
                border: 1px solid var(--border-color);
            }}
            .header {{
                text-align: center;
                margin-bottom: 40px;
                position: relative;
                overflow: hidden;
            }}
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
                opacity: 0.1;
                border-radius: 16px;
                animation: gradient-shift 6s ease-in-out infinite;
            }}
            @keyframes gradient-shift {{
                0%, 100% {{ transform: translateX(-100%); }}
                50% {{ transform: translateX(100%); }}
            }}
            .header h1 {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 0;
                font-size: 32px;
                font-weight: 700;
                letter-spacing: -0.5px;
                position: relative;
                z-index: 1;
            }}
            .date {{
                color: var(--text-secondary);
                font-size: 16px;
                font-weight: 500;
                margin-top: 8px;
                position: relative;
                z-index: 1;
            }}
            .section {{
                margin-bottom: 32px;
                padding: 28px;
                border-radius: 20px;
                background: var(--bg-section);
                backdrop-filter: blur(10px);
                border: 1px solid var(--border-section);
                box-shadow: 0 8px 32px var(--shadow-light);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }}
            .section::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 2px;
                background: linear-gradient(90deg, transparent, rgba(102,126,234,0.6), transparent);
                transition: left 0.5s ease;
            }}
            .section:hover {{
                transform: translateY(-2px);
                box-shadow: 0 12px 48px rgba(0,0,0,0.12);
            }}
            .section:hover::before {{
                left: 100%;
            }}
            .section-title {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 20px;
                font-weight: 600;
                margin: 0 0 20px 0;
                display: flex;
                align-items: center;
                letter-spacing: -0.3px;
            }}
            .section-title .emoji {{
                font-size: 28px;
                margin-right: 12px;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
            }}
            .weather-temp {{
                font-size: 48px;
                font-weight: 700;
                background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 16px 0;
                text-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            .weather-details {{
                display: flex;
                gap: 24px;
                margin: 16px 0;
                flex-wrap: wrap;
            }}
            .weather-detail {{
                background: var(--bg-detail);
                padding: 12px 16px;
                border-radius: 12px;
                font-weight: 500;
                color: var(--text-muted);
                border: 1px solid var(--border-item);
            }}
            .weather-summary {{
                margin-top: 16px;
                color: var(--text-secondary);
                font-weight: 500;
            }}
            .stock-item {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 16px 0;
                border-bottom: 1px solid var(--border-subtle);
                transition: all 0.2s ease;
                gap: 20px;
            }}
            .stock-item:last-child {{
                border-bottom: none;
            }}
            .stock-symbol {{
                font-weight: 600;
                font-size: 16px;
                color: var(--text-dark);
            }}
            .stock-price {{
                font-weight: 600;
                font-size: 15px;
                display: flex;
                align-items: center;
                gap: 6px;
                margin-left: 20px;
            }}
            .stock-positive {{
                color: #059669;
                background: rgba(5, 150, 105, 0.15);
                padding: 6px 12px;
                border-radius: 8px;
            }}
            .stock-negative {{
                color: #dc2626;
                background: rgba(220, 38, 38, 0.15);
                padding: 6px 12px;
                border-radius: 8px;
            }}
            @media (prefers-color-scheme: dark) {{
                .stock-positive {{
                    color: #10b981;
                    background: rgba(16, 185, 129, 0.2);
                }}
                .stock-negative {{
                    color: #f87171;
                    background: rgba(248, 113, 113, 0.2);
                }}
            }}
            .news-item {{
                margin-bottom: 20px;
                padding: 20px;
                background: var(--bg-item);
                border-radius: 16px;
                border: 1px solid var(--border-section);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                display: flex;
                gap: 20px;
                align-items: flex-start;
            }}

            .news-image {{
                width: 120px;
                height: 80px;
                object-fit: cover;
                border-radius: 4px;
                flex-shrink: 0;
                margin-right: 20px;
            }}

            .news-content {{
                flex: 1;
            }}

            .news-item::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                transform: scaleY(0);
                transition: transform 0.3s ease;
            }}
            .news-item:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px var(--shadow-light);
                background: var(--bg-item-hover);
            }}
            .news-item:hover::before {{
                transform: scaleY(1);
            }}
            .news-title {{
                font-weight: 600;
                color: var(--text-dark);
                text-decoration: none;
                display: block;
                font-size: 16px;
                line-height: 1.5;
                transition: color 0.2s ease;
            }}
            .news-title:hover {{
                color: #667eea;
            }}
            .event-item {{
                display: flex;
                align-items: center;
                margin-bottom: 16px;
                padding: 16px;
                background: var(--bg-item);
                border-radius: 14px;
                border: 1px solid var(--border-item);
                transition: all 0.2s ease;
                position: relative;
            }}
            .event-item::before {{
                content: '';
                position: absolute;
                left: 0;
                top: 50%;
                transform: translateY(-50%);
                width: 4px;
                height: 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 2px;
            }}
            .event-item:hover {{
                transform: translateX(4px);
                background: var(--bg-item-hover);
                box-shadow: 0 4px 20px var(--shadow-light);
            }}
            .event-time {{
                font-weight: 600;
                color: #667eea;
                margin-right: 20px;
                min-width: 90px;
                font-size: 14px;
                margin-left: 16px;
            }}
            .event-title {{
                color: var(--text-dark);
                font-weight: 500;
            }}
            .quote-section {{
                text-align: center;
                padding: 32px;
                background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
                border-radius: 20px;
                position: relative;
            }}
            @media (prefers-color-scheme: dark) {{
                .quote-section {{
                    background: linear-gradient(135deg, rgba(102,126,234,0.15) 0%, rgba(118,75,162,0.15) 100%);
                }}
            }}
            .quote-text {{
                font-style: italic;
                font-size: 18px;
                color: var(--text-muted);
                margin-bottom: 16px;
                line-height: 1.7;
                font-weight: 400;
                position: relative;
            }}
            .quote-text::before,
            .quote-text::after {{
                content: '"';
                font-size: 48px;
                color: var(--quote-accent);
                position: absolute;
                font-family: serif;
            }}
            .quote-text::before {{
                top: -10px;
                left: -16px;
            }}
            .quote-text::after {{
                bottom: -30px;
                right: -16px;
            }}
            .quote-author {{
                font-weight: 600;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 16px;
            }}
            .error {{
                color: #dc2626;
                font-style: italic;
                padding: 16px;
                background: var(--error-bg);
                border-radius: 12px;
                border: 1px solid var(--error-border);
            }}
            @media (prefers-color-scheme: dark) {{
                .error {{
                    color: #f87171;
                }}
            }}
            .no-events {{
                color: var(--text-secondary);
                font-style: italic;
            }}
            @media (max-width: 600px) {{
                body {{ padding: 20px 16px; }}
                .container {{ padding: 24px; }}
                .section {{ padding: 20px; }}
                .weather-details {{ flex-direction: column; gap: 12px; }}
                .stock-item {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
                .event-item {{ flex-direction: column; align-items: flex-start; }}
                .event-time {{ margin-left: 0; margin-bottom: 4px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Daily Digest</h1>
                <div class="date">{current_date}</div>
            </div>
    """
    
    # Weather Section
    if weather and "error" not in weather:
        weather_emoji = get_weather_icon(weather.get("icon", ""), weather.get("conditions", ""))
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span class="emoji">{weather_emoji}</span>
                    Weather in {weather['city']}
                </div>
                <div class="weather-temp">{weather['temp']}°F</div>
                <div class="weather-details">
                    <div class="weather-detail">Low: {weather['tempmin']}°F</div>
                    <div class="weather-detail">High: {weather['tempmax']}°F</div>
                    <div class="weather-detail">{weather['conditions']}</div>
                </div>
                <div class="weather-summary">{weather['summary']}</div>
            </div>
        """
    elif weather and "error" in weather:
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span class="emoji">🌤️</span>
                    Weather
                </div>
                <div class="error">{weather['error']}</div>
            </div>
        """
    
    # Calendar Section
    if calendar and calendar["events"]:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📅</span>
                    Today's Events
                </div>
        """
        for event in calendar["events"]:
            html += f"""
                <div class="event-item">
                    <div class="event-time">{event['time']}</div>
                    <div class="event-title">{event['title']}</div>
                </div>
            """
        html += "</div>"
    elif calendar:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📅</span>
                    Today's Events
                </div>
                <div class="no-events">No events scheduled for today.</div>
            </div>
        """
    
    # Stocks Section
    if stocks and stocks["stocks"]:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📈</span>
                    Stock Prices
                </div>
        """
        for stock in stocks["stocks"]:
            if "error" not in stock:
                arrow = "⬆️" if stock["change"] > 0 else "⬇️" if stock["change"] < 0 else "⏸"
                price_class = "stock-positive" if stock["change"] > 0 else "stock-negative" if stock["change"] < 0 else ""
                html += f"""
                    <div class="stock-item">
                        <div class="stock-symbol">{stock['symbol']}</div>
                        <div class="stock-price {price_class}">
                            ${stock['price']:.2f} <span style="margin-left: 4px;">{arrow} {stock['percent_change']:.2f}%</span>
                        </div>
                    </div>
                """
            else:
                html += f"""
                    <div class="stock-item">
                        <div class="stock-symbol">{stock['symbol']}</div>
                        <div class="error">{stock['error']}</div>
                    </div>
                """
        html += "</div>"
    
    # News Section
    if news and news["articles"]:
        html += """
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📰</span>
                    Top News Headlines
                </div>
        """
        for article in news["articles"]:
            # Handle image with fallback
            image_html = ""
            # print(f"Image URL: {article.get('image')}")
            if article.get('image') and article['image'].strip():
                image_html = f'''<div class="news-image-container">
                                    <img src="{article["image"]}" 
                                        alt="Article image" 
                                        class="news-image" 
                                        loading="lazy"
                                        onerror="this.style.display='none'; this.parentElement.innerHTML='<div class=&quot;image-placeholder&quot;>📰</div>'">
                                </div>'''
            
            html += f"""
                <div class="news-item">
                    {image_html}
                    <div class="news-content">
                        <a href="{article['url']}" class="news-title" target="_blank">
                            {article['title']}
                        </a>
                    </div>
                </div>
            """
        html += "</div>"
    elif news:
        error_msg = news.get("error", "No news articles found.")
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span class="emoji">📰</span>
                    Top News Headlines
                </div>
                <div class="error">{error_msg}</div>
            </div>
        """
    
    # Quote Section
    if quote and "error" not in quote:
        html += f"""
            <div class="section quote-section">
                <div class="section-title">
                    <span class="emoji">💭</span>
                    Quote of the Day
                </div>
                <div class="quote-text">{quote['quote']}</div>
                <div class="quote-author">– {quote['author']}</div>
            </div>
        """
    elif quote and "error" in  quote:
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span class="emoji">💭</span>
                    Quote of the Day
                </div>
                <div class="error">{quote['error']}</div>
            </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    
    return html

def format_plain_text_email(weather, news, stocks, quote, calendar):
    #Format all data into plain text email as fallback
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    
    content = f"""
                    📧 DAILY DIGEST - {current_date}
                    {'='*50}

                    """
    
    # Weather
    if weather and "error" not in weather:
        weather_emoji = get_weather_icon(weather.get("icon", ""), weather.get("conditions", ""))
        content += f"""
                    {weather_emoji} WEATHER IN {weather['city'].upper()}
                    Current: {weather['temp']}°F
                    Low: {weather['tempmin']}°F | High: {weather['tempmax']}°F
                    Conditions: {weather['conditions']}
                    {weather['summary']}

                    """
    elif weather and "error" in weather:
        content += f"""
                    🌤️ WEATHER
                    {weather['error']}

                    """
    
    # Calendar
    content += "📅 TODAY'S EVENTS\n"
    if calendar and calendar["events"]:
        for event in calendar["events"]:
            content += f"- {event['time']}: {event['title']}\n"
    elif calendar:
        content += "No events scheduled for today.\n"
    content += "\n"
    
    # Stocks
    content += "📈 STOCK PRICES\n"
    if stocks and stocks["stocks"]:
        for stock in stocks["stocks"]:
            if "error" not in stock:
                arrow = "⬆️" if stock["change"] > 0 else "⬇️" if stock["change"] < 0 else "⏸"
                content += f"{stock['symbol']}: ${stock['price']:.2f} {arrow} ({stock['percent_change']:.2f}%)\n"
            else:
                content += f"{stock['symbol']}: {stock['error']}\n"
    content += "\n"
    
    # News
    content += "📰 TOP NEWS HEADLINES\n"
    if news and news["articles"]:
        for article in news["articles"]:
            content += f"- {article['title']}\n  ({article['url']})\n"
    elif news:
        error_msg = news.get("error", "No news articles found.")
        content += f"{error_msg}\n"
    content += "\n"
    
    # Quote
    content += "💭 QUOTE OF THE DAY\n"
    if quote and "error" not in quote:
        content += f'"{quote["quote"]}"\n– {quote["author"]}\n'
    elif quote and "error" in  quote:
        content += f"{quote['error']}\n"
    
    return content