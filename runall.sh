#!
DATE=$(date +%Y-%m-%d)
# python working_wayback_scraper.py |tee log.${DATE}
# grep --no-filename "^\[" log.${DATE} |jq -scr '.[]|.[1]' >cm-tweets.txt
# ./processwayback.sh cm-tweets.txt
exit
# ./processwayback.sh input-celia-cea-weaver-deleted-tweets.txt 
python convert_to_amp.py
find ./ceaweaver/ ./amp_tweets/ ./content/ -type f  -name "*.html" -not -name "tweet*"  -print |grep html$  |sort |python generate_amp_index.py


