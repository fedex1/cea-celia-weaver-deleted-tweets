#!
DATE=$(date +%Y-%m-%d)

if false; then
    FILE="log.20260226.input.txt"

    grep --no-filename "^\[\"" log.20260226 |jq -scr '.[]|.[1]' > $FILE
    # ./processwayback2.sh log.20260226.input.txt 20260226.on.$(date +%Y-%m-%d)
    #!
    # Set IFS to an empty value and use -r with read for robust line processing
    while IFS= read -r line; do
      # Process the line here
      echo "Processing line: $line"
      # waybackpack $line -d ceaweaver
      waybackpack $line -d "20260226.on.$DATE"
    done < "$FILE"

    python firecrawl-test.py |jq -c '.data.web[]' >firecrawl.$DATE.jsonl
fi

AGO=$(date -d "1 day ago" +%Y-%m-%d)
python firecrawl-test.py "site:x.com micah lasher after:$AGO" |jq -c '.data.web[]' >firecrawl.$DATE.json
jq -r '"🔗 URL: \(.url)\n📌 Title: \(.title)\n📝 Desc: \(.description)\n🔢 Rank: \(.position)\n---"' <firecrawl.$DATE.jsonl >firecrawl.$DATE.jsonl.txt
curl --location   --data-binary @firecrawl.$DATE.jsonl.txt   --trace-ascii debug_log.txt   "https://script.google.com/macros/s/AKfycbzPV-to5wu164gyz-c04BKiDG4hwm4E_2eG9viWFeL8Kc-SGZQGFohlZZ9WodgJwXCk/exec" --data "subject=Timmins For Congress latest social search research" --data "to=ralph@brooklynmarathon.com,danny@timminsforcongress.com"
