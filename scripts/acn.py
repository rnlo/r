import requests
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://bgp.he.net/country/CN'

# Define the header with the User-Agent for the latest macOS Safari browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.3 Safari/605.1.15'
}

def get_sorted_data(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('tbody')

    selected_data = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 2 and columns[0].text.strip().startswith("AS"):
            if columns[1].text.strip() or columns[2].text.strip() != '0':
                selected_data.append(columns[0].text.strip().replace("AS", "IP-ASN,"))
    
    return sorted(selected_data)

if __name__ == "__main__":
    sorted_data = get_sorted_data(url, headers)
    
    if len(sorted_data) > 300:
        with open('ACN.list', 'w') as file:
            file.writelines(f"{line}\n" for line in sorted_data)
        print(f"CNASN Generated from {url} and saved to ACN.list.")
    else:
        print("Result has less than 300 lines. Not writing to file.")