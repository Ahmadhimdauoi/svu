import requests
from bs4 import BeautifulSoup
import os

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = "6086820567" # تم استخراجه من صورتك
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # جلب آخر الأخبار
    news_items = soup.find_all('div', class_='views-row')
    
    if news_items:
        first_news = news_items[0]
        title_tag = first_news.find('a')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://svuonline.org" + title_tag['href']
            msg = f"📢 <b>خبر جديد من الجامعة:</b>\n\n{title}\n\n🔗 <a href='{link}'>التفاصيل هنا</a>"
            send_telegram_msg(msg)
            print("تم إرسال الخبر!")

if __name__ == "__main__":
    scrape_svu()
