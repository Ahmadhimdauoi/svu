import requests
from bs4 import BeautifulSoup
import os

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # البحث عن عناصر الأخبار (تعديل الـ selectors بناءً على هيكلية الموقع)
    news_items = soup.find_all('div', class_='views-row')
    
    # ملف بسيط لتخزين آخر خبر تم إرساله لمنع التكرار
    last_news_file = "last_news.txt"
    last_sent = ""
    if os.path.exists(last_news_file):
        with open(last_news_file, "r") as f:
            last_sent = f.read().strip()

    new_messages = []
    
    for item in news_items[:5]: # فحص آخر 5 أخبار فقط
        title_tag = item.find('a')
        if title_tag:
            title = title_tag.text.strip()
            link = "https://svuonline.org" + title_tag['href']
            
            if link == last_sent:
                break
                
            new_messages.append(f"<b>خبر جديد من SVU:</b>\n\n{title}\n\n<a href='{link}'>رابط الخبر</a>")
            
    if new_messages:
        # إرسال الأخبار من الأقدم للأحدث
        for msg in reversed(new_messages):
            send_telegram_msg(msg)
        
        # تحديث آخر خبر تم إرساله
        with open(last_news_file, "w") as f:
            latest_link = "https://svuonline.org" + news_items[0].find('a')['href']
            f.write(latest_link)

if __name__ == "__main__":
    scrape_svu()
