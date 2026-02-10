import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://svuonline.org/ar/node/228"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    response = requests.get(url, headers=headers, timeout=20, verify=False)
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Successfully saved page source.")
except Exception as e:
    print(f"Error: {e}")