import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# Define the region flag emoji based on the region code
region_flags = {
    'US': '🇺🇸',  # United States
    'CN': '🇨🇳',  # China
}

# Define the header with the User-Agent for the latest macOS Safari browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15'
}

def scrape_data(region_code):
    # Define the URL to scrape
    url = f'https://bgp.he.net/country/{region_code}'

    # Create a session
    with requests.Session() as session:
        session.headers.update(headers)

        # Make the request with the specified headers
        response = session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract content from tbody table where td[2] is not empty or td[3] is not 0
        # Replace "AS" with "IP-ASN,"
        table = soup.find('tbody')

        selected_data = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 2 and columns[0].text.strip().startswith("AS"):
                if columns[1].text.strip() or columns[2].text.strip() != '0':
                    selected_data.append(columns[0].text.strip().replace("AS", "IP-ASN,"))

        # Check if the result contains more than 100 lines, if so, write to file
        if len(selected_data) > 100:

            # Write the scraped content to the file with EST timezone timestamp at the beginning
            eastern = pytz.timezone('US/Eastern')
            est_time = datetime.now(eastern).strftime('%m/%d/%Y %I:%M:%S %p')
            region_flag = region_flags.get(region_code.upper(), '')

            with open(f'ASN{region_code}.list', 'w') as file:
                file.write(f"# {region_flag}{region_code}ASN Generated from {url}\n")
                file.write(f"# Updated at {est_time} (EST)\n")
                file.write(f"# Total lines: {len(selected_data)}\n")
                file.write("# https://github.com/rnlo/r\n")
                file.writelines(f"{line}\n" for line in selected_data)
            print(f"{region_code}ASN Generated from {url} and saved to ASN{region_code}.list.")
        else:
            print(f"Result has less than 100 lines for {region_code}. Not writing to file.")

# Define the region code
scrape_data('US')  # United States
scrape_data('CN')  # China