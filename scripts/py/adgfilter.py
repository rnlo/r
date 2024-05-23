import os
from datetime import datetime
import pytz
import requests
import traceback

# Local destination folder path
destination_folder = os.getcwd()


# Generate AdGuard DNS filter for Surge
def generate_dns_filter():
    try:
        url = "https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt"

        domains_to_exclude = [
            "*",
            "logs.netflix.com",
            "example1.example.com",
            "example2.example.com",
            "example3.example.com",
        ]

        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()

        filtered_lines = [
            "." + line[2:-1]
            for line in lines
            if line.startswith("||")
            and line.endswith("^")
            and not any(exclude_item in line for exclude_item in domains_to_exclude)
        ]

        if len(filtered_lines) > 100:
            # Get current timestamp in Eastern Standard Time (EST)
            eastern = pytz.timezone("US/Eastern")
            est_time = datetime.now(eastern).strftime("%m/%d/%Y %I:%M:%S %p")

            # Write the filtered content to a file with timestamp comments
            with open(
                os.path.join(destination_folder, "dnsfilters.txt"), "w"
            ) as output_file:
                output_file.write(
                    f"# AdGuard DNS filter for Surge Generated from {url}\n"
                )
                output_file.write(f"# Updated at {est_time} (EST)\n")
                output_file.write(f"# Total lines: {len(filtered_lines)}\n")
                output_file.write("# https://github.com/rnlo/r\n")
                output_file.writelines(f"{line}\n" for line in filtered_lines)
            print(
                f"AdGuard DNS filter for Surge Generated from {url} and saved to dnsfilters.txt."
            )
        else:
            print("Result has less than 100 lines. Not writing to file.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the file from '{url}': {e}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    generate_dns_filter()
