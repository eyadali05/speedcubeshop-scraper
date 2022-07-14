import requests
import time
import csv
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime

# URL to scrape
data = []
base_url = "https://speedcubeshop.com"
urls = [
    "https://speedcubeshop.com/collections/3x3-speed-cubes",
    "https://speedcubeshop.com/collections/premium-puzzles",
    "https://speedcubeshop.com/collections/more-puzzles",
    "https://speedcubeshop.com/collections/must-haves",
    "https://speedcubeshop.com/collections/nanoblocks",
    "https://speedcubeshop.com/collections/plastic-kits",
]


# Get html and make request
def extract(url):
    # My request headers
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    # Getting request
    response = requests.get(url, headers=header)
    # Initializing Parser
    soup = BeautifulSoup(response.text, "html.parser")

    return soup


# Parse html and return data
def transform(data:list, soup):
    products = soup.find_all("div", class_="product-details")
    for product in products:
        data.append(
            {
                "Cube Name": product.find("a").text.replace("\n", "").strip(),
                "Cube Price": product.find("div", class_="price-regular").text.strip(),
                "Cube Link": base_url + str(product.find("a").get("href"))
            }
        )
    return data


# Output data to terminal
def load(data:list):
    date = datetime.now().strftime("%Y-%m-%d")
    keys = data[0].keys()

    with open(f"{date} SpeedCubeShop.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

# Pagination
for url_number, product_url in enumerate(tqdm(urls, desc="Scraping", position=0, leave=True)):
    print()
    print(f"----Scraping URL number {url_number + 1}----")
    time.sleep(0.1)
    for page in range(1, 10):
        try:
            product_url = f"{product_url}?page={page}"
            soup = extract(product_url)
            parsed_data = transform(data, soup)
            print(f"Finished Page {page}!")
        except AttributeError as e:
            print(e)
            continue

# Output data
print(f"TOTAL ITEMS: {len(data)}")
load(data)