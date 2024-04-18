import os
from datetime import datetime
import pytz

# List of files to read
file_names = ["temprule.list", "DouYin.list", "Zhihu.list"]
destination_folder = os.getcwd()

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
