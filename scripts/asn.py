from bs4 import BeautifulSoup
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pytz
import random
import requests
import time
import traceback

region_and_flag = {
    'CN': '🇨🇳',  # China
    'US': '🇺🇸',  # United States
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15'
}

def get_and_parse_data(region_code):
    try:
        url = f'https://bgp.he.net/country/{region_code}'

        with requests.Session() as session:
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 500, 502, 503, 504 ])
            session.mount('https://', HTTPAdapter(max_retries=retries))

            session.headers.update(headers)
            response = session.get(url)

            if response.status_code != 200:
                print(f"Request to {url} returned status code {response.status_code}.")
                return None, None

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('tbody')

            if table is None:
                print(f"No table found in the response from {url} .")
                return None, None

            selected_data = []
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) > 2 and columns[0].text.strip().startswith("AS"):
                    if columns[2].text.strip() != '0':
                        selected_data.append(columns[0].text.strip().replace("AS", "IP-ASN,"))
        return selected_data, url
    except requests.exceptions.RequestException as e:
        print(f"Request error occurred while scraping data for region code {region_code}. Error: {e}")
        return None, None
    except Exception as e:
        print(f"Error occurred while scraping data for region code {region_code}. Error: {e}")
        print(traceback.format_exc())
        return None, None

def write_data_to_file(region_code, selected_data, url):
    try:
        if len(selected_data) > 100:
            eastern = pytz.timezone('US/Eastern')
            est_time = datetime.now(eastern).strftime('%m/%d/%Y %I:%M:%S %p')
            region_flag = region_and_flag.get(region_code.upper(), '')

            with open(f'ASN{region_code}.list', 'w') as file:
                file.write(f"# {region_flag}{region_code}ASN Generated from {url}\n")
                file.write(f"# Updated at {est_time} (EST)\n")
                file.write(f"# Total lines: {len(selected_data)}\n")
                file.write("# https://github.com/rnlo/r\n")
                file.writelines(f"{line}\n" for line in selected_data)
            print(f"{region_code}ASN Generated from {url} and saved to ASN{region_code}.list.")

            # Write the sorted data to another file for all region codes
            sorted_data = sorted(selected_data)
            with open(f'A{region_code}.list', 'w') as file:
                file.writelines(f"{line}\n" for line in sorted_data)
            print(f"{region_code}ASN Generated from {url} sorted and saved to A{region_code}.list.")
        else:
            print(f"Result has less than 100 lines for {region_code}. Not writing to file.")
    except IOError as e:
        print(f"IOError occurred while writing data to file for region code {region_code}. Error: {e}")
    except Exception as e:
        print(f"Error occurred while writing data to file for region code {region_code}. Error: {e}")
        print(traceback.format_exc())

def scrape_data():
    try:
        for region_code in region_and_flag.keys():
            selected_data, url = get_and_parse_data(region_code)

            # Check if selected_data or url is None
            if selected_data is None or url is None:
                print(f"Skipping region code {region_code} due to missing data.")
                continue

            write_data_to_file(region_code, selected_data, url)

            # Add a random delay between requests
            time.sleep(random.uniform(2, 5))  # delay for a random number of seconds between * and *
    except Exception as e:
        print(f"Error occurred while scraping data. Error: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    scrape_data()