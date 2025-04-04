import requests
from bs4 import BeautifulSoup
import openpyxl
from datetime import datetime

def scrape_product_info(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://www.titanfittings.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try multiple selectors to find the product title
        selectors = [
            'h1.product-name',                # Original selector
            'h1.product-title',               # Common alternative
            'h1.product-detail__title',       # Another common pattern
            'h1.productView-title',           # Yet another common pattern
            'h1[itemprop="name"]',           # Schema.org markup
            'h1.title'                        # Simple fallback
        ]
        
        product_title = None
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                product_title = element.get_text(strip=True)
                break
        
        if not product_title:
            # Fallback to searching for any h1 if specific selectors fail
            h1 = soup.find('h1')
            if h1:
                product_title = h1.get_text(strip=True)
        
        if not product_title:
            raise ValueError("Could not find product title on page")
            
        return product_title
        
    except Exception as e:
        print(f"Error scraping product info: {str(e)}")
        print(f"Response status code: {response.status_code if 'response' in locals() else 'No response'}")
        return None

def save_to_excel(data, file_path):
    try:
        # Try to load existing workbook
        try:
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
        except:
            # If file doesn't exist, create new workbook
            wb = openpyxl.Workbook()
            sheet = wb.active
            sheet.append(["Product Information", "Date Added"])  # Add headers
        
        # Write data
        sheet.append([data, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
        
        # Save workbook
        wb.save(file_path)
        print(f"Data successfully saved to {file_path}")
        
    except Exception as e:
        print(f"Error saving to Excel: {e}")

if __name__ == "__main__":
    product_url = "https://www.titanfittings.com/adapters-and-fittings/hydraulic-adapters/steel-hydraulic-adapters/37-degree-jic-an-fittings/2406/tube-expander-reducer-3-8-jic-9-16-18-thread-female-x-1-2-jic-3-4-16-thread-male"
    excel_path = r"C:\Users\Exlterra CAD 02\Documents\GitHub\pjbrich.github.io\BOP\BOP3.xlsx"
    
    product_info = scrape_product_info(product_url)
    
    if product_info:
        print(f"Scraped product info: {product_info}")
        save_to_excel(product_info, excel_path)
    else:
        print("Failed to scrape product information")