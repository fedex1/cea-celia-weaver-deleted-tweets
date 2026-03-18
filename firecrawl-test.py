import os
import sys
import requests
import json

url = "https://api.firecrawl.dev/v2/search"

payload = {
  "query": "site:x.com paladino after:2026-02-26",
  "sources": [
    "web"
  ],
  "categories": [],
  "limit": 10,
  "scrapeOptions": {
    "onlyMainContent": False,
    "maxAge": 172800000,
    "parsers": [
      "pdf"
    ],
    "formats": []
  }
}

headers = {
    "Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

# print(response.json())
json.dump(response.json(),sys.stdout)
