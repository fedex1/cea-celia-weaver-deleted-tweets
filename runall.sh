#!
# ./processwayback.sh input-celia-cea-weaver-deleted-tweets.txt
python convert_to_amp.py
find ./ceaweaver/ ./amp_tweets/ -type f  -name "*.html" -not -name "tweet*"  -print |grep html$  |sort |python generate_amp_index.py


