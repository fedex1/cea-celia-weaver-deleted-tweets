#!
DATE=$(date +%Y-%m-%d)
# python working_wayback_scraper.py "stopvickie" |tee log.${DATE}
grep --no-filename "^\[\"" log.${DATE} |jq -scr '.[]|.[1]' >restore-tweets.${DATE}.txt
./processwayback.sh restore-tweets.${DATE}.txt
exit

# ./processwayback.sh input-celia-cea-weaver-deleted-tweets.txt 
python convert_to_amp.py
find ./ceaweaver/ ./amp_tweets/ ./content/ -type f  -name "*.html" -not -name "tweet*"  -print |grep html$  |sort |python generate_amp_index.py


