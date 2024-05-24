import os
from concurrent.futures import ThreadPoolExecutor
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


if __name__ == "__main__":
    download_files_in_parallel(file_urls)
