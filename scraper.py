import requests
from bs4 import BeautifulSoup
import os

DB_FILE = "last_news.txt"

def get_last_sent():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_last_sent(link):
    with open(DB_FILE, "w") as f:
        f.write(link)

def send_telegram_msg(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
        print("✅ تم إرسال الخبر إلى تلغرام بنجاح!")
        return True
    except Exception as e:
        print(f"❌ فشل الإرسال: {e}")
        return False

def scrape_svu():
    url = "https://svuonline.org/ar/node/228"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_items = soup.find_all('div', class_='views-row')
        
        if news_items:
            first_news = news_items[0]
            title_tag = first_news.find('a')
            
            # محاولة العثور على التاريخ
            date_tag = first_news.find('span', class_='date-display-single')
            if not date_tag:
                date_tag = first_news.find('div', class_='views-field-created')
            if not date_tag:
                date_tag = first_news.find(class_='date')
                
            date_str = date_tag.text.strip() if date_tag else "غير متوفر"

            if title_tag:
                title = title_tag.text.strip()
                link = "https://svuonline.org" + title_tag['href']
                
                # التحقق من التكرار
                last_link = get_last_sent()
                if link == last_link:
                    print("😴 لا يوجد أخبار جديدة. تم إرسال هذا الخبر مسبقاً.")
                    return
                
                msg = f"🔔 <b>خبر جديد من SVU:</b>\n\n📅 <b>التاريخ:</b> {date_str}\n\n📰 <b>العنوان:</b> {title}\n\n🔗 <a href='{link}'>التفاصيل من هنا</a>"
                if send_telegram_msg(msg):
                    save_last_sent(link)
        else:
            print("⚠️ لم يتم العثور على أي أخبار في الصفحة.")
            
    except Exception as e:
        print(f"❌ خطأ أثناء سحب البيانات: {e}")

if __name__ == "__main__":
    scrape_svu()