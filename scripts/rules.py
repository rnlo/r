import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import pytz
import re
import requests
import traceback

# Dictionary of file URLs and new file names
file_urls = {
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_All_No_Resolve.list": "Apple.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Microsoft/Microsoft.list": "Microsoft.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list": "Google.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Facebook/Facebook.list": "Facebook.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list": "Netflix.list",
    # "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/AmazonIp.list": "AmazonIP.list",
    "https://iptv-org.github.io/iptv/countries/us.m3u": "us.m3u",
}

# Define a dictionary that contains the arrays of URLs, begin markers, end markers, and output files
filter_parameters = {
    "source_files": {
        "https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Amazon.list": "Amazon.list",
        # "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Amazon/Amazon.list": "AmazonAll.list",
        # "https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Google.list": "GoogleAll.list"
    },
    "markers": {
        "## >> Amazon Prime Video": "## >> Audible",
        # "## >> CreateSpace": "## >> End CreateSpace",
        # "## >> Youtube": "## >> End Youtube"
    },
    "lines_to_exclude": {
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonPrimeVideo/AmazonPrimeVideo.list",
        "DOMAIN-SUFFIX,cloudfront.net",
        "DOMAIN-SUFFIX,example.example.com",
    },
}

# List of files to read
file_names_dict = {
    "temp.list": [
        "temprule.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ByteDance/ByteDance.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Zhihu/Zhihu.list",
    ],
    "domain.list": [
        "domainrule.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/GitHub/GitHub.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Copilot/Copilot.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Telegram/Telegram.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/YouTube/YouTube.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/TikTok/TikTok.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Spotify/Spotify.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Discord/Discord.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/PayPal/PayPal.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitter/Twitter.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Wikipedia/Wikipedia.list",
    ],
    "streaminggeo.list": [
        "streaminggeorule.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/HuluUSA/HuluUSA.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Sling/Sling.list",
    ],
    "streaming.list": [
        "streamingrule.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonPrimeVideo/AmazonPrimeVideo.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Peacock/Peacock.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Twitch/Twitch.list",
    ],
    "cn.list": [
        "cnrule.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Alibaba/Alibaba_All_No_Resolve.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Tencent/Tencent.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/WeChat/WeChat.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/ByteDance/ByteDance.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/NetEase/NetEase.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Baidu/Baidu.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/XiaoMi/XiaoMi.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/MeiTuan/MeiTuan.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Zhihu/Zhihu.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/JingDong/JingDong.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Xunlei/Xunlei.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Youku/Youku.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/iQIYI/iQIYI.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/TencentVideo/TencentVideo.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Migu/Migu.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/CIBN/CIBN.list",
    ],
}

# Local destination folder path
destination_folder = os.getcwd()


# Download list files from file_urls
def download_file(file_url, new_file_name):
    try:
        response = requests.get(file_url)
        if response.status_code == 200:
            file_content = response.content

            target_file = os.path.join(destination_folder, new_file_name)
            with open(target_file, "wb") as f:
                f.write(file_content)
            print(f"File copied from {file_url} and saved to {new_file_name}.")
        else:
            print(f"Unable to retrieve file {file_url}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the file from '{file_url}': {e}")
    except Exception as e:
        print(f"Error occurred while downloading {file_url}. Error: {str(e)}")
        print(traceback.format_exc())


def download_files_in_parallel(file_urls):
    try:
        # Use a ThreadPoolExecutor to download the files in parallel
        with ThreadPoolExecutor() as executor:
            executor.map(download_file, file_urls.keys(), file_urls.values())
    except Exception as e:
        print(f"Error occurred while executing parallel downloads. Error: {str(e)}")
        print(traceback.format_exc())


# Download list files and filter from filter_parameters
def fetch_and_filter_content(filter_parameters):
    # Fetch lines to exclude from URLs
    lines_to_exclude_temp = filter_parameters["lines_to_exclude"].copy()
    for line_to_exclude in lines_to_exclude_temp:
        if line_to_exclude.startswith("http://") or line_to_exclude.startswith(
            "https://"
        ):
            try:
                response = requests.get(line_to_exclude, timeout=10)
                if response.status_code == 200:
                    lines = response.text.split("\n")
                    for line in lines:
                        if not line.startswith("#"):
                            filter_parameters["lines_to_exclude"].add(line)
                filter_parameters["lines_to_exclude"].remove(line_to_exclude)
            except requests.exceptions.RequestException as e:
                print(
                    f"An error occurred while fetching the exclude list from '{line_to_exclude}': {e}"
                )
                print(traceback.format_exc())
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print(traceback.format_exc())

    # Fetch and filter source files
    for source_url, filtered_file in filter_parameters["source_files"].items():
        try:
            response = requests.get(source_url, timeout=10)

            if response.status_code == 200:
                content = response.text
                for begin, end in filter_parameters["markers"].items():
                    pattern = r"{}.*?(?={})".format(re.escape(begin), re.escape(end))
                    content = re.sub(pattern, "", content, flags=re.DOTALL)

                for line_to_exclude in filter_parameters["lines_to_exclude"]:
                    content = content.replace(line_to_exclude, "")

                with open(os.path.join(destination_folder, filtered_file), "w") as f:
                    f.write(content)
                print(
                    f"File copied from {source_url} filtered and added to {filtered_file}."
                )
            else:
                print(f"File '{source_url}' not found.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the file from '{source_url}': {e}")
            print(traceback.format_exc())
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(traceback.format_exc())


# Get file content from file_names_dict and added to destination_file_name
def get_file_content(file_name):
    try:
        if file_name.startswith("http://") or file_name.startswith("https://"):
            response = requests.get(file_name)
            response.raise_for_status()  # Raise an exception if the request was unsuccessful
            return response.text
        else:
            with open(file_name, "r") as file:
                return file.read()
    except requests.exceptions.RequestException as e:
        print(
            f"Error occurred while fetching the file from URL: {file_name}. Error: {str(e)}"
        )
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(traceback.format_exc())


def copy_files_to_destination(file_names_dict):
    try:
        with ThreadPoolExecutor() as executor:
            for destination_file_name, file_names in file_names_dict.items():
                destination_file_path = os.path.join(
                    destination_folder, destination_file_name
                )
                lines = []
                # Check if the destination file exists before reading
                if os.path.exists(destination_file_path):
                    # Read the existing content first
                    with open(destination_file_path, "r") as destination_file:
                        lines = destination_file.readlines()
                    # Find the line with "# End rnlo rules"
                    end_line_index = None
                    for i, line in enumerate(lines):
                        if "# End rnlo rules" in line:
                            end_line_index = i
                            break
                    # If the line is found, keep the content before it and include it
                    if end_line_index is not None:
                        lines = lines[: end_line_index + 2]
                    else:
                        lines = (
                            []
                        )  # Clear the content if "# End rnlo rules" is not found
                # Write the old content and the new content
                with open(destination_file_path, "w") as destination_file:
                    destination_file.writelines(lines)
                    results = executor.map(get_file_content, file_names)
                    for file_name, content in zip(file_names, results):
                        if content is not None:
                            destination_file.write(content)
                            destination_file.write("\n")
                            print(
                                f"File copied from {file_name} and added to {destination_file_name}."
                            )
    except Exception as e:
        print(f"Error occurred while processing files. Error: {str(e)}")
        print(traceback.format_exc())


# Generate China IP filter for Surge
def generate_ip_filter():
    try:
        url = (
            "https://raw.githubusercontent.com/misakaio/chnroutes2/master/chnroutes.txt"
        )

        domains_to_exclude = ["#", "exampleip1", "exampleip2", "exampleip3"]

        response = requests.get(url)
        response.raise_for_status()
        lines = response.text.splitlines()

        filtered_lines = [
            "IP-CIDR," + line
            for line in lines
            if not any(exclude_item in line for exclude_item in domains_to_exclude)
        ]

        if len(filtered_lines) > 100:
            # Get current timestamp in Eastern Standard Time (EST)
            eastern = pytz.timezone("US/Eastern")
            est_time = datetime.now(eastern).strftime("%m/%d/%Y %I:%M:%S %p")

            # Write the filtered content to a file with timestamp comments
            with open(
                os.path.join(destination_folder, "CNIP.list"), "w"
            ) as output_file:
                output_file.write(f"# China IP for Surge Generated from {url}\n")
                output_file.write(f"# Updated at {est_time} (EST)\n")
                output_file.write(f"# Total lines: {len(filtered_lines)}\n")
                output_file.write("# https://github.com/rnlo/r\n")
                output_file.writelines(f"{line}\n" for line in filtered_lines)
            print(f"China IP for Surge Generated from {url} and saved to CNIP.list.")
        else:
            print("Result has less than 100 lines. Not writing to file.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the file from '{url}': {e}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(traceback.format_exc())


# Generate AWS IP for Surge
def generate_aws_ip():
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
            lines.append(f"IP-CIDR,{ipv4_prefix['ip_prefix']},no-resolve\n")

        # Write all IPv6 prefixes
        for ipv6_prefix in data["ipv6_prefixes"]:
            lines.append(f"IP-CIDR,{ipv6_prefix['ipv6_prefix']},no-resolve\n")

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
    download_files_in_parallel(file_urls)
    fetch_and_filter_content(filter_parameters)
    copy_files_to_destination(file_names_dict)
    generate_ip_filter()
    generate_aws_ip()
    generate_dns_filter()
