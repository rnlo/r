import os
from concurrent.futures import ThreadPoolExecutor
import requests
import traceback

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
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Youku/Youku.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/CIBN/CIBN.list",
    ],
}

# Local destination folder path
destination_folder = os.getcwd()


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


if __name__ == "__main__":
    copy_files_to_destination(file_names_dict)
