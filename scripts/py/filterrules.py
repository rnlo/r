import os
import re
import requests
import traceback

# Define a dictionary that contains the arrays of URLs, begin markers, end markers, and output files
filter_parameters = {
    "source_files": {
        "https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Amazon.list": "Amazon.list",
        #"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/Amazon/Amazon.list": "AmazonAll.list",
        #"https://raw.githubusercontent.com/LM-Firefly/Rules/master/PROXY/Google.list": "GoogleAll.list"
    },
    "markers": {
        "## >> Amazon Prime Video": "## >> Audible",
        #"## >> CreateSpace": "## >> End CreateSpace",
        #"## >> Youtube": "## >> End Youtube"
    },
    "lines_to_exclude": {
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Surge/AmazonPrimeVideo/AmazonPrimeVideo.list",
        "example1.example.com",
        "example2.example.com"
    }
}

# Local destination folder path
destination_folder = os.getcwd()

# Download list files and filter from filter_parameters
def fetch_and_filter_content(filter_parameters):
    # Fetch lines to exclude from URLs
    lines_to_exclude_temp = filter_parameters['lines_to_exclude'].copy()
    for line_to_exclude in lines_to_exclude_temp:
        if line_to_exclude.startswith('http://') or line_to_exclude.startswith('https://'):
            try:
                response = requests.get(line_to_exclude, timeout=10)
                if response.status_code == 200:
                    lines = response.text.split('\n')
                    for line in lines:
                        if not line.startswith('#'):
                            filter_parameters['lines_to_exclude'].add(line)
                filter_parameters['lines_to_exclude'].remove(line_to_exclude)
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching the exclude list from '{line_to_exclude}': {e}")
                print(traceback.format_exc())
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                print(traceback.format_exc())

    # Fetch and filter source files
    for source_url, filtered_file in filter_parameters['source_files'].items():
        try:
            response = requests.get(source_url, timeout=10)

            if response.status_code == 200:
                content = response.text
                for begin, end in filter_parameters['markers'].items():
                    pattern = r'{}.*?(?={})'.format(re.escape(begin), re.escape(end))
                    content = re.sub(pattern, '', content, flags=re.DOTALL)
                
                for line_to_exclude in filter_parameters['lines_to_exclude']:
                    content = content.replace(line_to_exclude, '')

                with open(os.path.join(destination_folder, filtered_file), 'w') as f:
                    f.write(content)
                print(f"File copied from {source_url} filtered and added to {filtered_file}.")
            else:
                print(f"File '{source_url}' not found.")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching the file from '{source_url}': {e}")
            print(traceback.format_exc())
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print(traceback.format_exc())

if __name__ == "__main__":
    fetch_and_filter_content(filter_parameters)
