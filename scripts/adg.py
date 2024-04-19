import requests
from datetime import datetime
import pytz

# Define the URL to scrape
url = 'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt'

# Add an array to exclude specific lines
lines_to_exclude = [
    ".log.netflix.com",
    ".example1.example.com",
    ".example2.example.com",
]

def get_filtered_lines(url, lines_to_exclude):
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    return ["." + line[2:-1] for line in lines if line.startswith("||") and line.endswith("^") and not any(exclude_item in line for exclude_item in lines_to_exclude)]

if __name__ == "__main__":
    filtered_lines = get_filtered_lines(url, lines_to_exclude)
    if len(filtered_lines) > 100:
        # Get current timestamp in Eastern Standard Time (EST)
        eastern = pytz.timezone('US/Eastern')
        est_time = datetime.now(eastern).strftime('%H:%M:%S %m/%d/%Y')

        # Write the filtered content to a file with timestamp comments
        with open('dnsfilters.txt', 'w') as output_file:
            output_file.write(f"# AdGuard DNS filter for Surge Generated from {url}\n")
            output_file.write(f"# Updated at EST {est_time}\n")
            output_file.write(f"# Total lines: {len(filtered_lines)}\n")
            output_file.write("# https://github.com/rnlo/r\n")
            output_file.writelines(f"{line}\n" for line in filtered_lines)
        print(f"AdGuard DNS filter for Surge Generated from {url} and saved to dnsfilters.txt.")
    else:
        print("Result has less than 100 lines. Not writing to file.")
