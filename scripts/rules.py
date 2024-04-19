import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import pytz
import requests

# List of file URLs
file_urls = [
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Apple/Apple_All_No_Resolve.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Google/Google.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Microsoft/Microsoft.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/GitHub/GitHub.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/OpenAI/OpenAI.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Telegram/Telegram.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Spotify/Spotify.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Netflix/Netflix.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/HuluUSA/HuluUSA.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/YouTube/YouTube.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Amazon/Amazon.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/DouYin/DouYin.list",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Zhihu/Zhihu.list",
    "https://raw.githubusercontent.com/geekdada/surge-list/master/domain-set/dns-filter.txt"
]

# List of files to read
file_names = ["temprule.list", "DouYin.list", "Zhihu.list"]

# Local destination folder path
destination_folder = os.getcwd()

# New file names list
new_file_names = [
    "Apple.list",
    "Google.list",
    "Microsoft.list",
    "GitHub.list",
    "OpenAI.list",
    "Telegram.list",
    "Spotify.list",
    "Netflix.list",
    "Hulu.list",
    "YouTube.list",
    "Amazon.list",
    "DouYin.list",
    "Zhihu.list",
    "dns-filter.txt"
]

def download_file(file_url, new_name):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_content = response.content

        target_file = os.path.join(destination_folder, new_name)
        with open(target_file, "wb") as f:
            f.write(file_content)
        print(f"File copied from {file_url} and saved to {new_name}.")
    else:
        print(f"Unable to retrieve file {file_url}.")

def download_files_in_parallel(file_urls, new_file_names):
    # Use a ThreadPoolExecutor to download the files in parallel
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, file_urls, new_file_names)

def copy_files_to_temp(file_names, destination_folder):
    # Define the Eastern Time Zone
    est = pytz.timezone('US/Eastern')

    # Open or create the "temp.list" file for writing
    with open("temp.list", "w") as temp_file:
        for file_name in file_names:
            # Construct the file path
            file_path = os.path.join(destination_folder, file_name)
            
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    # Get the current time in EST
                    est_time = datetime.now(est).strftime("%m/%d/%Y %I:%M:%S %p")
                    # Append EST timestamp before the file content
                    temp_file.write(f"# {est_time} (EST)\n")
                    # Write file content to "temp.list"
                    temp_file.write(file.read())
                    temp_file.write("\n")
                print(f"File copied from '{file_name}' and saved to temp.list.")
            else:
                print(f"File '{file_name}' not found.")

def generate_dns_filter():

    url = 'https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_15_DnsFilter/filter.txt'
    
    lines_to_exclude = [
        ".log.netflix.com",
        ".example1.example.com",
        ".example2.example.com"
    ]
    
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    filtered_lines = ["." + line[2:-1] for line in lines if line.startswith("||") and line.endswith("^") and not any(exclude_item in line for exclude_item in lines_to_exclude)]
    
    if len(filtered_lines) > 100:
        # Get current timestamp in Eastern Standard Time (EST)
        eastern = pytz.timezone('US/Eastern')
        est_time = datetime.now(eastern).strftime('%H:%M:%S %m/%d/%Y')

        # Write the filtered content to a file with timestamp comments
        with open(os.path.join(destination_folder, 'dnsfilters.txt'), 'w') as output_file:
            output_file.write(f"# AdGuard DNS filter for Surge Generated from {url}\n")
            output_file.write(f"# Updated at EST {est_time}\n")
            output_file.write(f"# Total lines: {len(filtered_lines)}\n")
            output_file.write("# https://github.com/rnlo/r\n")
            output_file.writelines(f"{line}\n" for line in filtered_lines)
        print(f"AdGuard DNS filter for Surge Generated from {url} and saved to dnsfilters.txt.")
    else:
        print("Result has less than 100 lines. Not writing to file.")

if __name__ == "__main__":
    download_files_in_parallel(file_urls, new_file_names)
    copy_files_to_temp(file_names, destination_folder)
    generate_dns_filter()