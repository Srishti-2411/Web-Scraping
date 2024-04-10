import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_amazon_products(url, pages):
    all_products = []

    for page in range(1, pages+1):
        print(f"Scraping page {page}")
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', {'data-component-type': 's-search-result'})

            for product in products:
                product_info = {}
                
                # Product URL
                product_info['url'] = 'https://www.amazon.in' + product.find('a', class_='a-link-normal')['href']
                
                # Product Name
                product_info['name'] = product.find('span', class_='a-text-normal').text.strip()
                
                # Product Price
                price = product.find('span', class_='a-price')
                if price:
                    product_info['price'] = price.find('span', class_='a-offscreen').text.strip()
                else:
                    product_info['price'] = 'Price not available'
                
                # Rating
                rating = product.find('span', class_='a-icon-alt')
                if rating:
                    product_info['rating'] = rating.text.split(' ')[0]
                else:
                    product_info['rating'] = 'No rating'
                
                # Number of Reviews
                reviews_count = product.find('span', {'class': 'a-size-base'})
                if reviews_count:
                    product_info['reviews_count'] = reviews_count.text.strip()
                else:
                    product_info['reviews_count'] = 'No reviews'

                all_products.append(product_info)

        time.sleep(2)  # Add a delay to avoid overwhelming the server

    return all_products

# URL of the Amazon product listing page
url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'

# Number of pages to scrape
pages_to_scrape = 20

# Scrape products
products = scrape_amazon_products(url, pages_to_scrape)

# Save scraped data to CSV file
csv_file = 'amazon_products.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['url', 'name', 'price', 'rating', 'reviews_count'])
    writer.writeheader()
    writer.writerows(products)

print(f"Scraped data saved to {csv_file}")
