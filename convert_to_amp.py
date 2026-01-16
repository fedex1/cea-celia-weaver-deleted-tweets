import json
import os
import re
invalid_chars_pattern = r'[%&<>:"/\\|?*\n\r#]'


def create_amp_html(tweet_text, created_at, author_name, author_handle, tweet_id):
    """Generates a valid AMP HTML string for a tweet."""
    amp_template = f"""<!doctype html>
<html amp lang="en">
  <head>
    <meta charset="utf-8">
    <script async src="https://cdn.ampproject.org/v0.js"></script>
    <title>Tweet by {author_name}</title>
    <link rel="canonical" href="https://example.com/tweets/{tweet_id}.html">
    <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
    <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
    <style amp-custom>
      body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; line-height: 1.5; background-color: #f7f9f9; }}
      .tweet-card {{ background: white; border: 1px solid #e1e8ed; padding: 20px; border-radius: 12px; max-width: 500px; margin: auto; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
      .author-info {{ font-weight: bold; margin-bottom: 5px; }}
      .handle {{ color: #536471; font-weight: normal; font-size: 0.9em; }}
      .content {{ font-size: 1.1em; margin: 15px 0; white-space: pre-wrap; }}
      .date {{ color: #536471; font-size: 0.9em; border-top: 1px solid #eff3f4; pt: 10px; margin-top: 10px; }}
    </style>
  </head>
  <body>
    <div class="tweet-card">
      <div class="author-info">
        {author_name} <span class="handle">@{author_handle}</span>
      </div>
      <div class="content">{tweet_text}</div>
      <div class="date">{created_at}</div>
    </div>
  </body>
</html>"""
    return amp_template

def process_tweets(input_path):
    output_dir = 'amp_tweets'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            try:
                raw_data = json.loads(line)
                
                # Case 1: Standard / Older API format
                if "user" in raw_data:
                    text = raw_data.get("text", "")
                    date = raw_data.get("created_at", "")
                    author_name = raw_data["user"].get("name", "Unknown")
                    author_handle = raw_data["user"].get("screen_name", "unknown")
                    tweet_id = raw_data.get("id_str", str(i))

                # Case 2: New Twitter API v2 format
                elif "data" in raw_data:
                    text = raw_data["data"].get("text", "")
                    date = raw_data["data"].get("created_at", "")
                    tweet_id = raw_data["data"].get("id", str(i))
                    
                    # Author info is usually in the "includes" section
                    author_name = "Unknown"
                    author_handle = "unknown"
                    if "includes" in raw_data and "users" in raw_data["includes"]:
                        user_data = raw_data["includes"]["users"][0]
                        author_name = user_data.get("name", "Unknown")
                        author_handle = user_data.get("username", "unknown")
                
                else:
                    continue

                # Create the AMP file
                amp_content = create_amp_html(text, date, author_name, author_handle, tweet_id)
                filename=f"details {date} {text[:140]}.html"

                # Replace invalid characters with an underscore
                sanitized_filename = re.sub(invalid_chars_pattern, '_', filename)
                with open(f"{output_dir}/{sanitized_filename}", "w", encoding="utf-8") as out_file:
                    out_file.write(amp_content)
                
                print(f"Processed tweet {tweet_id}")

            except Exception as e:
                print(f"Error on line {i}: {e}")

if __name__ == "__main__":
    process_tweets('input.jsonl')
