import sys
from bs4 import BeautifulSoup
import re
invalid_chars_pattern = r'[%&<>:"/\\|?*\n\r#]'

def extract_tweet_text():
    # Check if a filename was provided as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename.html>")
        return

    file_path = sys.argv[1]

    try:
        # Open and read the file provided in the first parameter
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # The tweet text in this document is found in the 'og:description' meta tag
    meta_desc = soup.find('meta', property='og:description')

    if meta_desc and 'content' in meta_desc.attrs:
        tweet_text = meta_desc['content']
        # Clean up the surrounding smart quotes used in the source
        clean_tweet_text = tweet_text.strip('“”"')
        sanitized_filename = re.sub(invalid_chars_pattern, '_', clean_tweet_text)
        print(f'cp {file_path} "{sanitized_filename[:240]}.html"')
        print(clean_tweet_text)
    else:
        # Fallback to <title> tag if meta tag is missing
        if soup.title:
            print(soup.title.string)

if __name__ == "__main__":
    extract_tweet_text()

#import sys
#from bs4 import BeautifulSoup
#
#def extract_tweet_text():
#    # Read the entire HTML content from stdin
#    html_content = sys.stdin.read()
#
#    if not html_content:
#        return
#
#    # Parse the HTML content
#    soup = BeautifulSoup(html_content, 'html.parser')
#
#    # The tweet text in this document is found in the 'og:description' meta tag
#    # Content: "“117 organizers on the biweekly @housing4allNY call this afternoon.
#    # The NY mvmt to #CancelRent and house the homeless is on fire. 🔥🔥”"
#    meta_desc = soup.find('meta', property='og:description')
#
#    if meta_desc and 'content' in meta_desc.attrs:
#        tweet_text = meta_desc['content']
#        # Clean up the surrounding smart quotes used in the source
#        clean_tweet_text = tweet_text.strip('“”"')
#        print(clean_tweet_text)
#    else:
#        # Fallback to <title> tag if meta tag is missing
#        if soup.title:
#            print(soup.title.string)
#
#if __name__ == "__main__":
#    extract_tweet_text()
#
## from bs4 import BeautifulSoup
#
## Load the HTML content from the file
## file_path = '1259905837570670592.html'
## with open(file_path, 'r', encoding='utf-8') as f:
##    html_content = f.read()
##
### Parse the HTML content
##soup = BeautifulSoup(html_content, 'html.parser')
##
### Option 1: Extract from the <title> tag
### This often includes the user's name and "on Twitter:"
##tweet_title = soup.title.string if soup.title else "No title found"
##print(f"Tweet Title: {tweet_title}")
##
### Option 2: Extract from the 'og:description' meta tag
### This usually contains the raw text of the tweet
##meta_desc = soup.find('meta', property='og:description')
##tweet_text = meta_desc['content'] if meta_desc else "No tweet text found"
##
### Clean up the extracted text (removing leading/trailing quotes if necessary)
##clean_tweet_text = tweet_text.strip('“”"')
##print(f"Extracted Tweet Text: {clean_tweet_text}")
