import requests
import os
import traceback

# Local destination folder path
destination_folder = os.getcwd()


# Generate AWS IP for Surge
def get_aws_ip():
    # URL for AWS IP ranges JSON data
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

    try:
        # Fetch the data
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        lines = []

        # Write all IPv4 prefixes
        for ipv4_prefix in data["prefixes"]:
            lines.append(f"IP-CIDR,{ipv4_prefix['ip_prefix']}\n")

        # Write all IPv6 prefixes
        for ipv6_prefix in data["ipv6_prefixes"]:
            lines.append(f"IP-CIDR,{ipv6_prefix['ipv6_prefix']}\n")

        total_lines = len(lines)

        # Get the createDate from JSON
        date = data.get("createDate", "Unknown")

        with open(os.path.join(destination_folder, "AWSIP.list"), "w") as output_file:
            output_file.write(f"# AWS IP for Surge Generated from {url}\n")
            output_file.write(f"# CreateDate: {date}\n")
            output_file.write(f"# Total lines: {total_lines}\n")
            output_file.write("# https://github.com/rnlo/r\n")
            output_file.writelines(lines)

        print(f"AWS IP for Surge Generated from {url} and saved to AWSIP.list")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the file from '{url}': {e}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())


if __name__ == "__main__":
    # Call the function to fetch and save AWS IP ranges
    get_aws_ip()
