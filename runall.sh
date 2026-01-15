#!
find ./ceaweaver/ ./amp_tweets/ -type f  -name "*.html" -not -name "tweet*"  -print |grep html$  |sort -r |python generate_amp_index.py
