from bs4 import BeautifulSoup

with open("page_source.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
news_items = soup.find_all('div', class_='views-row')

if news_items:
    for i, item in enumerate(news_items[:3]):
        print(f"--- Item {i} ---")
        print(item.prettify()[:1000]) # Print first 1000 chars of each item
else:
    print("No news items found.")
