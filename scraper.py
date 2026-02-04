from db_setup import get_db_connection, create_table

def seed_database():
    # 1. Re-create the table with the new 'color' column
    create_table()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 2. 30 Premium Samsung Phones Data
    # Format: (Model, Display, Camera, Battery, Storage, Price, Color)
    phones = [
        # --- S24 Series ---
        ("Samsung Galaxy S24 Ultra", "6.8-inch Dynamic LTPO AMOLED 2X", "200MP Main, 50MP Periscope", "5000 mAh, 45W", "256GB/512GB/1TB", "$1299", "Titanium Gray, Titanium Black, Titanium Violet, Titanium Yellow"),
        ("Samsung Galaxy S24 Plus", "6.7-inch Dynamic LTPO AMOLED 2X", "50MP Main, 10MP Telephoto", "4900 mAh, 45W", "256GB/512GB", "$999", "Onyx Black, Marble Grey, Cobalt Violet, Amber Yellow"),
        ("Samsung Galaxy S24", "6.2-inch Dynamic LTPO AMOLED 2X", "50MP Main, 10MP Telephoto", "4000 mAh, 25W", "128GB/256GB/512GB", "$799", "Onyx Black, Marble Grey, Cobalt Violet, Amber Yellow"),
        
        # --- Z Fold & Flip 6/5 Series ---
        ("Samsung Galaxy Z Fold 6", "7.6-inch Foldable Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "4400 mAh, 25W", "256GB/512GB/1TB", "$1899", "Silver Shadow, Pink, Navy, Crafted Black, White"),
        ("Samsung Galaxy Z Flip 6", "6.7-inch Foldable Dynamic AMOLED 2X", "50MP Main, 12MP Ultrawide", "4000 mAh, 25W", "256GB/512GB", "$1099", "Yellow, Silver Shadow, Mint, Blue, Peach"),
        ("Samsung Galaxy Z Fold 5", "7.6-inch Foldable Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "4400 mAh, 25W", "256GB/512GB/1TB", "$1799", "Icy Blue, Phantom Black, Cream, Gray, Blue"),
        ("Samsung Galaxy Z Flip 5", "6.7-inch Foldable Dynamic AMOLED 2X", "12MP Main, 12MP Ultrawide", "3700 mAh, 25W", "256GB/512GB", "$999", "Mint, Graphite, Cream, Lavender, Gray"),

        # --- S23 Series ---
        ("Samsung Galaxy S23 Ultra", "6.8-inch Dynamic AMOLED 2X", "200MP Main, 10MP Telephoto", "5000 mAh, 45W", "256GB/512GB/1TB", "$1199", "Phantom Black, Green, Cream, Lavender, Graphite"),
        ("Samsung Galaxy S23 Plus", "6.6-inch Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "4700 mAh, 45W", "256GB/512GB", "$999", "Phantom Black, Cream, Green, Lavender"),
        ("Samsung Galaxy S23", "6.1-inch Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "3900 mAh, 25W", "128GB/256GB", "$799", "Phantom Black, Cream, Green, Lavender"),
        ("Samsung Galaxy S23 FE", "6.4-inch Dynamic AMOLED 2X", "50MP Main, 8MP Telephoto", "4500 mAh, 25W", "128GB/256GB", "$599", "Mint, Cream, Graphite, Purple, Indigo"),

        # --- Z Fold & Flip 4 Series ---
        ("Samsung Galaxy Z Fold 4", "7.6-inch Foldable Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "4400 mAh, 25W", "256GB/512GB/1TB", "$1499", "Graygreen, Phantom Black, Beige, Burgundy"),
        ("Samsung Galaxy Z Flip 4", "6.7-inch Foldable Dynamic AMOLED 2X", "12MP Main, 12MP Ultrawide", "3700 mAh, 25W", "128GB/256GB/512GB", "$899", "Bora Purple, Graphite, Pink Gold, Blue"),

        # --- S22 Series ---
        ("Samsung Galaxy S22 Ultra", "6.8-inch Dynamic AMOLED 2X", "108MP Main, 10MP Periscope", "5000 mAh, 45W", "128GB/256GB/512GB/1TB", "$900", "Phantom Black, White, Burgundy, Green, Graphite"),
        ("Samsung Galaxy S22 Plus", "6.6-inch Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "4500 mAh, 45W", "128GB/256GB", "$700", "Phantom Black, White, Pink Gold, Green"),
        ("Samsung Galaxy S22", "6.1-inch Dynamic AMOLED 2X", "50MP Main, 10MP Telephoto", "3700 mAh, 25W", "128GB/256GB", "$600", "Phantom Black, White, Pink Gold, Green"),

        # --- S21 Series ---
        ("Samsung Galaxy S21 Ultra", "6.8-inch Dynamic AMOLED 2X", "108MP Main, 10MP Periscope", "5000 mAh, 25W", "128GB/256GB/512GB", "$800", "Phantom Black, Phantom Silver, Phantom Titanium"),
        ("Samsung Galaxy S21 FE", "6.4-inch Dynamic AMOLED 2X", "12MP Main, 8MP Telephoto", "4500 mAh, 25W", "128GB/256GB", "$500", "White, Graphite, Lavender, Olive"),
        ("Samsung Galaxy S21 Plus", "6.7-inch Dynamic AMOLED 2X", "12MP Main, 64MP Telephoto", "4800 mAh, 25W", "128GB/256GB", "$600", "Phantom Black, Phantom Silver, Phantom Violet"),

        # --- Note Series (Legendary) ---
        ("Samsung Galaxy Note 20 Ultra", "6.9-inch Dynamic AMOLED 2X", "108MP Main, 12MP Periscope", "4500 mAh, 25W", "256GB/512GB", "$850", "Mystic Bronze, Mystic Black, Mystic White"),
        
        # --- High-End A Series & Others ---
        ("Samsung Galaxy A55", "6.6-inch Super AMOLED", "50MP Main, 12MP Ultrawide", "5000 mAh, 25W", "128GB/256GB", "$479", "Awesome Iceblue, Awesome Lilac, Awesome Navy"),
        ("Samsung Galaxy A54", "6.4-inch Super AMOLED", "50MP Main, 12MP Ultrawide", "5000 mAh, 25W", "128GB/256GB", "$350", "Lime, Graphite, Violet, White"),
        ("Samsung Galaxy A35", "6.6-inch Super AMOLED", "50MP Main, 8MP Ultrawide", "5000 mAh, 25W", "128GB/256GB", "$399", "Awesome Iceblue, Awesome Lilac, Awesome Navy"),
        ("Samsung Galaxy A73 5G", "6.7-inch Super AMOLED Plus", "108MP Main, 12MP Ultrawide", "5000 mAh, 25W", "128GB/256GB", "$450", "Gray, Mint, White"),
        ("Samsung Galaxy F55", "6.7-inch Super AMOLED Plus", "50MP Main, 8MP Ultrawide", "5000 mAh, 45W", "128GB/256GB", "$360", "Apricot Crush, Raisin Black"),
        ("Samsung Galaxy M55", "6.7-inch Super AMOLED Plus", "50MP Main, 8MP Ultrawide", "5000 mAh, 45W", "128GB/256GB", "$330", "Denim Black, Light Green"),
        ("Samsung Galaxy Quantum 4", "6.4-inch Super AMOLED", "50MP Main, 12MP Ultrawide", "5000 mAh, 25W", "128GB", "$450", "Graphite, White, Lime"),
        ("Samsung Galaxy XCover 7", "6.6-inch PLS LCD", "50MP Main", "4050 mAh (Removable), 15W", "128GB", "$400", "Black"),
        ("Samsung W24", "7.6-inch Foldable AMOLED", "50MP Main, 10MP Telephoto", "4400 mAh, 25W", "1TB", "$2200", "Gray, Gold (China Exclusive)"),
        ("Samsung W24 Flip", "6.7-inch Foldable AMOLED", "12MP Main, 12MP Ultrawide", "3700 mAh, 25W", "512GB", "$1300", "White, Gold (China Exclusive)")
    ]
    
    print(f"Inserting {len(phones)} phones into database...")
    
    for p in phones:
        try:
            # Note: We added %s for the color column
            cursor.execute("""
                INSERT INTO phones (model_name, display, camera, battery, storage, price, color)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, p)
        except Exception as e:
            print(f"Skipped {p[0]}: {e}")
            
    conn.commit()
    cursor.close()
    conn.close()
    print("All 30 phones inserted successfully with colors!")

if __name__ == "__main__":
    seed_database()