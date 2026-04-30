import os
import sys
import requests
import json

# query = "https://x.com/MicahLasher"
query = "site:x.com paladino after:2026-02-26"
if len(sys.argv) > 1:
    # print(f"argv {sys.argv}") 
    query = sys.argv[1]
# sys.exit(1)
url = "https://api.firecrawl.dev/v2/search"

payload = {
  "query": query,
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
