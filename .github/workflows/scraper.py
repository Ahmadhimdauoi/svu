import requests
from bs4 import BeautifulSoup
import os

# الدالة المسؤولة عن إرسال الرسالة لتلغرام
def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        print("Sent successfully to Telegram")
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج الأخبار من هيكلية الموقع
        news_items = soup.find_all('div', class_='views-row')
        
        if news_items:
            # نأخذ أول خبر كمثال للتجربة
            first_news = news_items[0]
            title_tag = first_news.find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = "https://svuonline.org" + title_tag['href']
                
                msg = f"📢 <b>تحديث جديد من SVU:</b>\n\n{title}\n\n🔗 <a href='{link}'>رابط التفاصيل</a>"
                send_telegram_msg(msg)
        else:
            print("No news items found.")
            
    except Exception as e:
        print(f"Scraping error: {e}")

if __name__ == "__main__":
    scrape_svu()
