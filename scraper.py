

import requests
from bs4 import BeautifulSoup
from db_setup import insert_smartphone
import time

# Sample Samsung phones data (simulated scraping from a phone specification site)
SAMPLE_PHONES = [
    {
        'model_name': 'Samsung Galaxy S24 Ultra',
        'display': '6.8 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '5000 mAh, 45W fast charging',
        'camera': '200MP main, 12MP ultra-wide, 10MP 3x telephoto, 10MP 10x periscope telephoto',
        'ram': '12GB',
        'storage': '256GB / 512GB / 1TB',
        'price': '$1299'
    },
    {
        'model_name': 'Samsung Galaxy S24 Plus',
        'display': '6.7 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4900 mAh, 45W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP 3x telephoto',
        'ram': '12GB',
        'storage': '256GB / 512GB',
        'price': '$999'
    },
    {
        'model_name': 'Samsung Galaxy S24',
        'display': '6.2 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4000 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP 3x telephoto',
        'ram': '8GB / 12GB',
        'storage': '128GB / 256GB',
        'price': '$799'
    },
    {
        'model_name': 'Samsung Galaxy S23 Ultra',
        'display': '6.8 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '5000 mAh, 45W fast charging',
        'camera': '200MP main, 12MP ultra-wide, 10MP 3x telephoto, 10MP 10x periscope',
        'ram': '8GB / 12GB',
        'storage': '256GB / 512GB / 1TB',
        'price': '$999'
    },
    {
        'model_name': 'Samsung Galaxy S23 Plus',
        'display': '6.6 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4700 mAh, 45W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP 3x telephoto',
        'ram': '8GB',
        'storage': '256GB / 512GB',
        'price': '$899'
    },
    {
        'model_name': 'Samsung Galaxy S23',
        'display': '6.1 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '3900 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP 3x telephoto',
        'ram': '8GB',
        'storage': '128GB / 256GB',
        'price': '$799'
    },
    {
        'model_name': 'Samsung Galaxy Z Fold 5',
        'display': '7.6 inches main, 6.2 inches cover, Dynamic AMOLED 2X, 120Hz',
        'battery': '4400 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP telephoto',
        'ram': '12GB',
        'storage': '256GB / 512GB / 1TB',
        'price': '$1799'
    },
    {
        'model_name': 'Samsung Galaxy Z Flip 5',
        'display': '6.7 inches main, 3.4 inches cover, Dynamic AMOLED 2X, 120Hz',
        'battery': '3700 mAh, 25W fast charging',
        'camera': '12MP main, 12MP ultra-wide',
        'ram': '8GB',
        'storage': '256GB / 512GB',
        'price': '$999'
    },
    {
        'model_name': 'Samsung Galaxy A54 5G',
        'display': '6.4 inches Super AMOLED, 120Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 5MP macro',
        'ram': '6GB / 8GB',
        'storage': '128GB / 256GB',
        'price': '$449'
    },
    {
        'model_name': 'Samsung Galaxy A34 5G',
        'display': '6.6 inches Super AMOLED, 120Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '48MP main, 8MP ultra-wide, 5MP macro',
        'ram': '6GB / 8GB',
        'storage': '128GB / 256GB',
        'price': '$349'
    },
    {
        'model_name': 'Samsung Galaxy A15 5G',
        'display': '6.5 inches Super AMOLED, 90Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '50MP main, 5MP ultra-wide, 2MP macro',
        'ram': '4GB / 6GB / 8GB',
        'storage': '128GB',
        'price': '$199'
    },
    {
        'model_name': 'Samsung Galaxy M54 5G',
        'display': '6.7 inches Super AMOLED Plus, 120Hz',
        'battery': '6000 mAh, 25W fast charging',
        'camera': '108MP main, 8MP ultra-wide, 2MP macro',
        'ram': '8GB',
        'storage': '128GB / 256GB',
        'price': '$399'
    },
    {
        'model_name': 'Samsung Galaxy M34 5G',
        'display': '6.5 inches Super AMOLED, 120Hz',
        'battery': '6000 mAh, 25W fast charging',
        'camera': '50MP main, 8MP ultra-wide, 2MP macro',
        'ram': '6GB / 8GB',
        'storage': '128GB',
        'price': '$279'
    },
    {
        'model_name': 'Samsung Galaxy F54 5G',
        'display': '6.7 inches Super AMOLED Plus, 120Hz',
        'battery': '6000 mAh, 25W fast charging',
        'camera': '108MP main, 8MP ultra-wide, 2MP macro',
        'ram': '8GB',
        'storage': '256GB',
        'price': '$369'
    },
    {
        'model_name': 'Samsung Galaxy S21 FE 5G',
        'display': '6.4 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4500 mAh, 25W fast charging',
        'camera': '12MP main, 12MP ultra-wide, 8MP telephoto',
        'ram': '6GB / 8GB',
        'storage': '128GB / 256GB',
        'price': '$599'
    },
    {
        'model_name': 'Samsung Galaxy Note 20 Ultra',
        'display': '6.9 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4500 mAh, 25W fast charging',
        'camera': '108MP main, 12MP ultra-wide, 12MP periscope telephoto',
        'ram': '12GB',
        'storage': '128GB / 256GB / 512GB',
        'price': '$849'
    },
    {
        'model_name': 'Samsung Galaxy Z Fold 4',
        'display': '7.6 inches main, 6.2 inches cover, Dynamic AMOLED 2X, 120Hz',
        'battery': '4400 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP telephoto',
        'ram': '12GB',
        'storage': '256GB / 512GB / 1TB',
        'price': '$1499'
    },
    {
        'model_name': 'Samsung Galaxy Z Flip 4',
        'display': '6.7 inches main, 1.9 inches cover, Dynamic AMOLED, 120Hz',
        'battery': '3700 mAh, 25W fast charging',
        'camera': '12MP main, 12MP ultra-wide',
        'ram': '8GB',
        'storage': '128GB / 256GB / 512GB',
        'price': '$899'
    },
    {
        'model_name': 'Samsung Galaxy A73 5G',
        'display': '6.7 inches Super AMOLED Plus, 120Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '108MP main, 12MP ultra-wide, 5MP macro, 5MP depth',
        'ram': '6GB / 8GB',
        'storage': '128GB / 256GB',
        'price': '$469'
    },
    {
        'model_name': 'Samsung Galaxy A53 5G',
        'display': '6.5 inches Super AMOLED, 120Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '64MP main, 12MP ultra-wide, 5MP macro, 5MP depth',
        'ram': '4GB / 6GB / 8GB',
        'storage': '128GB / 256GB',
        'price': '$349'
    },
    {
        'model_name': 'Samsung Galaxy A14 5G',
        'display': '6.6 inches PLS LCD, 90Hz',
        'battery': '5000 mAh, 15W charging',
        'camera': '50MP main, 2MP macro, 2MP depth',
        'ram': '4GB / 6GB',
        'storage': '64GB / 128GB',
        'price': '$179'
    },
    {
        'model_name': 'Samsung Galaxy M14 5G',
        'display': '6.6 inches PLS LCD, 90Hz',
        'battery': '6000 mAh, 25W fast charging',
        'camera': '50MP main, 2MP macro, 2MP depth',
        'ram': '4GB / 6GB',
        'storage': '64GB / 128GB',
        'price': '$189'
    },
    {
        'model_name': 'Samsung Galaxy F14 5G',
        'display': '6.6 inches PLS LCD, 90Hz',
        'battery': '6000 mAh, 25W fast charging',
        'camera': '50MP main, 2MP macro, 2MP depth',
        'ram': '4GB / 6GB',
        'storage': '64GB / 128GB',
        'price': '$179'
    },
    {
        'model_name': 'Samsung Galaxy S22 Ultra',
        'display': '6.8 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '5000 mAh, 45W fast charging',
        'camera': '108MP main, 12MP ultra-wide, 10MP 3x telephoto, 10MP 10x periscope',
        'ram': '8GB / 12GB',
        'storage': '128GB / 256GB / 512GB / 1TB',
        'price': '$849'
    },
    {
        'model_name': 'Samsung Galaxy S22 Plus',
        'display': '6.6 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '4500 mAh, 45W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP telephoto',
        'ram': '8GB',
        'storage': '128GB / 256GB',
        'price': '$749'
    },
    {
        'model_name': 'Samsung Galaxy S22',
        'display': '6.1 inches Dynamic AMOLED 2X, 120Hz',
        'battery': '3700 mAh, 25W fast charging',
        'camera': '50MP main, 12MP ultra-wide, 10MP telephoto',
        'ram': '8GB',
        'storage': '128GB / 256GB',
        'price': '$699'
    },
    {
        'model_name': 'Samsung Galaxy XCover 6 Pro',
        'display': '6.6 inches TFT, 120Hz',
        'battery': '4050 mAh, removable, 25W fast charging',
        'camera': '50MP main, 8MP ultra-wide',
        'ram': '6GB',
        'storage': '128GB',
        'price': '$599'
    },
    {
        'model_name': 'Samsung Galaxy A05s',
        'display': '6.7 inches PLS LCD, 90Hz',
        'battery': '5000 mAh, 25W fast charging',
        'camera': '50MP main, 2MP macro, 2MP depth',
        'ram': '4GB / 6GB',
        'storage': '64GB / 128GB',
        'price': '$149'
    },
    {
        'model_name': 'Samsung Galaxy M13',
        'display': '6.6 inches PLS LCD, 60Hz',
        'battery': '5000 mAh, 15W charging',
        'camera': '50MP main, 5MP ultra-wide, 2MP macro',
        'ram': '4GB / 6GB',
        'storage': '64GB / 128GB',
        'price': '$139'
    },
    {
        'model_name': 'Samsung Galaxy F04',
        'display': '6.5 inches PLS LCD, 60Hz',
        'battery': '5000 mAh, 10W charging',
        'camera': '13MP main, 2MP depth',
        'ram': '4GB',
        'storage': '64GB',
        'price': '$99'
    }
]

def scrape_samsung_phones(url=None):
    print("🔄 Starting scraper...")
    
    if url:
        print(f"Attempting to scrape from: {url}")
        # In production, implement actual web scraping here
        # For now, we use sample data
        phones = SAMPLE_PHONES
    else:
        print("Using sample Samsung phone data (demo mode)")
        phones = SAMPLE_PHONES
    
    return phones

def save_to_db():
    print("\n" + "="*60)
    print("Samsung Phone Advisor - Web Scraper")
    print("="*60 + "\n")
    
    # Scrape phone data
    phones_data = scrape_samsung_phones()
    
    print(f"\n✓ Found {len(phones_data)} phones\n")
    
    # Insert each phone into the database
    for phone in phones_data:
        try:
            insert_smartphone(
                model_name=phone['model_name'],
                display=phone['display'],
                battery=phone['battery'],
                camera=phone['camera'],
                ram=phone['ram'],
                storage=phone['storage'],
                price=phone['price']
            )
            time.sleep(0.2)  # Rate limiting
        except Exception as e:
            print(f"✗ Error saving {phone['model_name']}: {e}")
    
    print("\n✓ Scraping and database insertion complete!")

def scrape_with_bs4(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        # Parse logic would go here based on target website structure
        
        return []
    except Exception as e:
        print(f"✗ Error scraping URL: {e}")
        return []

if __name__ == "__main__":
    # Run the scraper and save to database
    save_to_db()
