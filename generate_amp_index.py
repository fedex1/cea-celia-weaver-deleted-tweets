import sys
import os

# Configuration
OUTPUT_FILE = 'index.html'
PAGE_TITLE = "Celia (Cea) Weaver Deleted Tweets"

# AMP Boilerplate and Styles
AMP_HEADER = f"""<!doctype html>
<html ⚡>
<head>
  <meta charset="utf-8">
  <title>{PAGE_TITLE}</title>
  <link rel="canonical" href="{OUTPUT_FILE}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <style amp-custom>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.5; padding: 20px; color: #222; max-width: 800px; margin: auto; }}
    h1 {{ border-bottom: 2px solid #005af0; padding-bottom: 10px; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
    a {{ text-decoration: none; color: #007bff; }}
    a:hover {{ text-decoration: underline; }}
    .meta {{ font-size: 0.85em; color: #666; margin-left: 10px; }}
  </style>
</head>
<body>
  <h1>{PAGE_TITLE}</h1>
  <ul>
"""

AMP_FOOTER = """
  </ul>
</body>
</html>
"""

def main():
    # Check if stdin is empty (interactive check)
    if sys.stdin.isatty():
        print("Usage: ls | python3 generate_amp_index.py")
        return

    # Read lines from stdin, strip whitespace, and filter empty lines
    file_list = [line.strip() for line in sys.stdin if line.strip()]

    if not file_list:
        print("No input received via stdin.")
        return

    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(AMP_HEADER)
            for item in file_list:
                # Clean path for the link, but keep display name
                display_name = os.path.basename(item)
                f.write(f'    <li><a href="{item}">{display_name}</a><span class="meta">({item})</span></li>\n')
            f.write(AMP_FOOTER)

        print(f"AMP index generated: {OUTPUT_FILE} ({len(file_list)} links)")

    except IOError as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    main()
