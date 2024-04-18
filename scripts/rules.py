import requests
import os

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

for file_url, new_name in zip(file_urls, new_file_names):
    response = requests.get(file_url)
    if response.status_code == 200:
        file_content = response.content
        file_name = os.path.basename(file_url)

        target_file = os.path.join(destination_folder, new_name)
        with open(target_file, "wb") as f:
            f.write(file_content)
        print(f"File copied from {file_url} and saved to {new_name}.")
    else:
        print(f"Unable to retrieve file {file_url}.")
