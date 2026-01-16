#!
# Set IFS to an empty value and use -r with read for robust line processing
while IFS= read -r line; do
  # Process the line here
  echo "Processing line: $line"
  waybackpack $line -d ceaweaver
done < "$1"
