#!
DATE=$(date +%Y-%m-%d)
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


