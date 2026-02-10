import requests
from bs4 import BeautifulSoup
import os

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"Error: {e}")

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # سحب أول خبر للتجربة
    news_items = soup.find_all('div', class_='views-row')
    if news_items:
        title_tag = news_items[0].find('a')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://svuonline.org" + title_tag['href']
            msg = f"📢 <b>تحديث من الجامعة:</b>\n\n{title}\n\n🔗 <a href='{link}'>التفاصيل</a>"
            send_telegram_msg(msg)

if __name__ == "__main__":
    scrape_svu()
