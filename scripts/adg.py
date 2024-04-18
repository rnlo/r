import requests
from datetime import datetime
import pytz

# Define the URL to scrape
url = 'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt'

response = requests.get(url)
response.raise_for_status()
lines = response.text.splitlines()

# Add an array to exclude specific lines
lines_to_exclude = [
    "logs.netflix.com",
    "example1.example.com",
    "example2.example.com",
]
filtered_lines = []
for line in lines:
    if line.startswith("||") and line.endswith("^"):
        rule = line[2:-1]  # Extract content between || and ^
        if not any(exclude_item in line for exclude_item in lines_to_exclude):
            filtered_lines.append("." + rule)

# Check if the result contains more than 100 lines, if so, write to file
if len(filtered_lines) > 100:
    # Get current timestamp in Eastern Standard Time (EST)
    eastern = pytz.timezone('US/Eastern')
    est_time = datetime.now(eastern).strftime('%m/%d/%Y %I:%M:%S %p')

    # Write the filtered content to a file with timestamp comments
    with open("dnsfilters.txt", "w") as output_file:
        output_file.write(f"# AdGuard DNS filter for Surge Generated from {url}\n")
        output_file.write(f"# Updated at {est_time} (EST)\n")
        output_file.write(f"# Total lines: {len(filtered_lines)}\n")
        output_file.write("# https://github.com/rnlo/r\n")
        for item in filtered_lines:
            output_file.write(item + '\n')
    print(f"AdGuard DNS filter for Surge Generated from {url} and saved to dnsfilters.txt.")
else:
    print("Result has less than 100 lines. Not writing to file.")
