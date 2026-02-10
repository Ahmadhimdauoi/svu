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
        print("✅ تم إرسال الخبر إلى تلغرام بنجاح!")
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    # إضافة headers لتبدو العملية كمتصفح حقيقي
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج الأخبار
        news_items = soup.find_all('div', class_='views-row')
        
        if news_items:
            first_news = news_items[0]
            title_tag = first_news.find('a')
            if title_tag:
                title = title_tag.text.strip()
                link = "https://svuonline.org" + title_tag['href']
                
                msg = f"🔔 <b>خبر جديد من SVU:</b>\n\n{title}\n\n🔗 <a href='{link}'>التفاصيل من هنا</a>"
                send_telegram_msg(msg)
        else:
            print("⚠️ لم يتم العثور على أي أخبار في الصفحة.")
            
    except Exception as e:
        print(f"❌ خطأ أثناء سحب البيانات: {e}")

if __name__ == "__main__":
    scrape_svu()