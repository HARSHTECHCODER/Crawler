import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

# Constants
ARCHIVE_URL = "https://pastebin.com/archive"
RAW_URL_FORMAT = "https://pastebin.com/raw/{}"
KEYWORDS = ["crypto", "bitcoin", "ethereum", "blockchain", "t.me"]
OUTPUT_FILE = "keyword_matches.jsonl"

# Function to extract paste IDs from the archive page
def get_paste_ids():
    response = requests.get(ARCHIVE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    paste_links = soup.select("table.maintable a")
    paste_ids = [link['href'].replace("/", "") for link in paste_links[:30]]
    return paste_ids

# Function to fetch raw content of a paste
def fetch_paste_content(paste_id):
    url = RAW_URL_FORMAT.format(paste_id)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
    return None

# Function to detect keywords in paste content
def detect_keywords(content):
    found = [kw for kw in KEYWORDS if kw.lower() in content.lower()]
    return found

# Function to store result in JSONL file
def store_result(paste_id, keywords_found):
    data = {
        "source": "pastebin",
        "context": f"Found crypto-related content in Pastebin paste ID {paste_id}",
        "paste_id": paste_id,
        "url": RAW_URL_FORMAT.format(paste_id),
        "discovered_at": datetime.utcnow().isoformat() + "Z",
        "keywords_found": keywords_found,
        "status": "pending"
    }
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")

# Main crawling logic
def main():
    paste_ids = get_paste_ids()
    for paste_id in paste_ids:
        print(f"Checking paste ID: {paste_id}")
        content = fetch_paste_content(paste_id)
        if content:
            keywords_found = detect_keywords(content)
            if keywords_found:
                print(f"-> Keywords found: {keywords_found}")
                store_result(paste_id, keywords_found)
            else:
                print("-> No keywords found.")
        else:
            print("-> Failed to fetch content.")
        time.sleep(1)  # Delay to avoid rate limiting

if __name__ == "__main__":
    main()
