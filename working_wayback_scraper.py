# @title Wayback Machine Twitter Extractor
# @markdown Run this cell to pull archived tweet URLs for @CMChiOsse.
import sys
import requests
import pandas as pd
# from google.colab import files
import json

def get_wayback_tweets(username):
    # The CDX API allows us to search for all archived URLs under a specific path
    # We use a wildcard (*) to find all specific tweet status pages
    target_url = f"twitter.com/{username}/status/*"
    # cdx_url = f"http://web.archive.org/cdx/search/cdx?url={target_url}&output=json&fl=timestamp,original&collapse=digest"
    # from parameter
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={target_url}&from=20260226&output=json&fl=timestamp,original&collapse=digest"

    print(f"📡 Querying Wayback Machine for @{username}...")
    
    try:
        response = requests.get(cdx_url)
        if response.status_code == 200:
            data = response.json()
            if len(data) <= 1:
                print("No archived tweets found.")
                return None
            print(f"Length {len(data)}")
            # The first row is the header [timestamp, original]
            headers = data[0]
            rows = data[1:]
            
            # Format into Wayback URLs: https://web.archive.org/web/{timestamp}/{original}
            results = []
            for row in rows:
                timestamp, original = row[0], row[1]
                wayback_link = f"https://web.archive.org/web/{timestamp}/{original}"
                results.append({
                    'date_archived': timestamp,
                    'original_url': original,
                    'wayback_url': wayback_link
                })
                json.dump(row,sys.stdout)
                print()
            
            df = pd.DataFrame(results)
            return df
        else:
            print(f"Error: Wayback API returned status {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Execute for Chi Ossé
userlist=[
    "ossechi", "NYCProgressives", "NYCCouncil", "tiffany_caban", "sandynurse", 
    "alexaaviles", "ksantosuosso", "ChrisMarteNYC", "GaleABrewer", 
    "HarveyforNY", "CnDelarosa", "PierinaSanchez", "LincolnRestler", 
    "OsseChi", "ShahanaFromBK", "JenGutierrezNYC", "NantashaW", 
    "voteshekar", "JulieWonNYC"
]
print(sys.argv)
if len(sys.argv) > 1:
    userlist=sys.argv[1].split(",")
# print(userlist)
# sys.exit(1)
for username in userlist:
    df_tweets = get_wayback_tweets(username)

    if df_tweets is not None:
        filename = f"{username}_archived_tweets.csv"
        df_tweets.to_csv(filename, index=False)
        print(f"\n✅ Success! Found {len(df_tweets)} unique archived tweet snapshots.")
        # files.download(filename)
    else:
        print("Failed to retrieve data.")
