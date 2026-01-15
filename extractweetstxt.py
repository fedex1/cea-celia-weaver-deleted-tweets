import re
import json

def convert_to_amp_tweet(json_input):
    # Parse the input (handles both dict and string)
    data = json_input if isinstance(json_input, dict) else json.loads(json_input)

    handle = data.get("handle", "Unknown")
    raw_content = data.get("content", "")
    date = data.get("date", "")

    # 1. Clean up the content
    # Removes the "Follow/Unfollow/Blocked" header noise from archived tweets
    clean_content = re.sub(r'^.*?More\s+\*\s+', '', raw_content, flags=re.DOTALL)
    # Remove markdown-style links/images for a cleaner text display
    clean_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean_content)
    clean_content = re.sub(r'!\[.*?\]\([^\)]+\)', '🔥', clean_content) # Replacing emoji images with unicode

    amp_html = f"""
    <!doctype html>
    <html ⚡>
    <head>
      <meta charset="utf-8">
      <link rel="canonical" href="self.html">
      <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
      <style amp-custom>
        .tweet-card {{
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          border: 1px solid #e1e8ed;
          border-radius: 12px;
          padding: 16px;
          max-width: 500px;
          margin: 20px auto;
          background: #fff;
        }}
        .tweet-header {{ display: flex; align-items: center; margin-bottom: 10px; }}
        .handle {{ font-weight: bold; color: #14171a; }}
        .content {{ font-size: 16px; line-height: 1.4; color: #1c2022; white-space: pre-wrap; }}
        .date {{ font-size: 14px; color: #657786; margin-top: 10px; }}
      </style>
      <script async src="https://cdn.ampproject.org/v0.js"></script>
    </head>
    <body>
      <div class="tweet-card">
        <div class="tweet-header">
          <span class="handle">{handle}</span>
        </div>
        <div class="content">{clean_content.strip()}</div>
        <div class="date">{date}</div>
      </div>
    </body>
    </html>
    """
    return amp_html

def extract_ceaweaver_tweets(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex patterns for different tweet formats found in the text
    # 1. Text-based format (e.g., "5:01 AM - 10 Jun 2021")
    # 2. JSON-like format (e.g., "created_at":"Sun Nov 28 04:09:10 +0000 2021")
    
    tweets = []

    # Extracting from text blocks
    # Looking for blocks starting with @ceaweaver and ending with a date/time stamp
    text_blocks = re.findall(r'@\*\*ceaweaver\*\*\].*?\n\n(.*?)\n\n(\d{1,2}:\d{2} [APM]{2} - \d{1,2} [A-Za-z]{3} \d{4})', content, re.DOTALL)
    for text, date in text_blocks:
        tweet={
            'handle': '@ceaweaver',
            'date': date,
            'content': text.strip().replace('\n', ' ')
        }
        # print(json.dumps(tweet))
        # print()
        print(convert_to_amp_tweet(tweet))

        # tweets.append(tweet)

#   # Extracting from JSON-like strings
#   json_tweets = re.findall(r'{"created_at":"(.*?)".*?"text":"(.*?)".*?"screen_name":"ceaweaver"', content)
#   for date, text in json_tweets:
#       # Clean up escaped unicode if present
#       clean_text = text.encode().decode('unicode_escape')
#       tweets.append({
#           'handle': '@ceaweaver',
#           'date': date,
#           'content': clean_text.strip()
#       })

#   # Extracting from German/International legacy format (e.g., "19:17 - 8. Feb. 2021")
#   intl_blocks = re.findall(r'@\*\*ceaweaver\*\*\].*?\n\n(.*?)\n\n(\d{1,2}:\d{2} - \d{1,2}\. [A-Za-z]+\.? \d{4})', content, re.DOTALL)
#   for text, date in intl_blocks:
#       if "retweeted" not in text.lower(): # Simple check to avoid duplicates from retweets
#           tweets.append({
#               'handle': '@ceaweaver',
#               'date': date,
#               'content': text.strip().replace('\n', ' ')
#           })

    return tweets

# Usage
file_name = 'ceaweaver-deleted-twitter.txt'
extracted_tweets = extract_ceaweaver_tweets(file_name)

print(f"Found {len(extracted_tweets)} tweets:\n")
for t in extracted_tweets:
    print(f"DATE: {t['date']}")
    print(f"TWEET: {t['content']}")
    print("-" * 30)
