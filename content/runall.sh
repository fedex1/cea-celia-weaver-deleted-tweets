#!
find ../ceaweaver/ -type f -name "*.html" -exec python ../extractonlytweettext.py {} \; |grep "^cp " >copywithcontent.sh
