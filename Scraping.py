import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_amazon_product_listings(url, pages):
    all_product_urls = []

    for page in range(1, pages+1):
        print(f"Scraping page {page}")
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            for product in products:
                product_url = 'https://www.amazon.in' + product.find('a', class_='a-link-normal')['href']
                all_product_urls.append(product_url)

        time.sleep(2)  # Add a delay to avoid overwhelming the server

    return all_product_urls

def scrape_product_details(url):
    product_details = {}

    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Description
        description_meta = soup.find('meta', attrs={'name': 'description'})
        if description_meta:
            product_details['description'] = description_meta['content']
        else:
            product_details['description'] = 'Description not available'

        # ASIN
        asin_th = soup.find('th', string='ASIN')
        if asin_th:
            asin_td = asin_th.find_next('td')
            if asin_td:
                product_details['ASIN'] = asin_td.text.strip()
            else:
                product_details['ASIN'] = 'ASIN not available'
        else:
            product_details['ASIN'] = 'ASIN not available'

        # Product Description
        product_description_div = soup.find('div', id='productDescription')
        if product_description_div:
            product_details['product_description'] = product_description_div.text.strip()
        else:
            product_details['product_description'] = 'Product description not available'

        # Manufacturer
        manufacturer_th = soup.find('th', string='Manufacturer')
        if manufacturer_th:
            manufacturer_td = manufacturer_th.find_next('td')
            if manufacturer_td:
                manufacturer_info = manufacturer_td.text.strip()
                product_details['manufacturer'] = manufacturer_info.split('(')[0].strip() if '(' in manufacturer_info else manufacturer_info
            else:
                product_details['manufacturer'] = 'Manufacturer not available'
        else:
            product_details['manufacturer'] = 'Manufacturer not available'

    return product_details

def main():
    # URL of the Amazon product listing page
    url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

    # Number of pages to scrape for product listings
    pages_to_scrape = 20

    # Scrape product listings
    product_urls = scrape_amazon_product_listings(url, pages_to_scrape)

    all_products = []

    # Scrape product details
    for product_url in product_urls:
        print(f"Scraping details for product: {product_url}")
        product_details = scrape_product_details(product_url)
        all_products.append(product_details)
        time.sleep(2)  # Add a delay to avoid overwhelming the server

    # Save scraped data to CSV file
    csv_file = 'amazon_products_details.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['url', 'description', 'ASIN', 'product_description', 'manufacturer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products)

    print(f"Scraped data saved to {csv_file}")

if __name__ == "__main__":
    main()
