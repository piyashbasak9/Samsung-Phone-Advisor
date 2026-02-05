from db_setup import get_db_connection, create_table

def seed_database():
    create_table()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    phones = [
        ("Samsung Galaxy S24 Ultra", "6.8-inch AMOLED", "200MP Main", "5000 mAh", "256GB/512GB/1TB", "$1299", "Titanium Gray, Titanium Black"),
        ("Samsung Galaxy S24 Plus", "6.7-inch AMOLED", "50MP Main", "4900 mAh", "256GB/512GB", "$999", "Onyx Black, Marble Grey"),
        ("Samsung Galaxy S24", "6.2-inch AMOLED", "50MP Main", "4000 mAh", "128GB/256GB", "$799", "Cobalt Violet, Amber Yellow"),
        ("Samsung Galaxy Z Fold 6", "7.6-inch Foldable", "50MP Main", "4400 mAh", "256GB/512GB/1TB", "$1899", "Silver Shadow, Pink, Navy"),
        ("Samsung Galaxy Z Flip 6", "6.7-inch Foldable", "50MP Main", "4000 mAh", "256GB/512GB", "$1099", "Mint, Blue, Yellow"),
        ("Samsung Galaxy S23 Ultra", "6.8-inch AMOLED", "200MP Main", "5000 mAh", "256GB/512GB", "$1199", "Phantom Black, Green, Cream"),
        ("Samsung Galaxy S23 Plus", "6.6-inch AMOLED", "50MP Main", "4700 mAh", "256GB/512GB", "$999", "Lavender, Green"),
        ("Samsung Galaxy S23", "6.1-inch AMOLED", "50MP Main", "3900 mAh", "128GB/256GB", "$799", "Phantom Black, Cream"),
        ("Samsung Galaxy S23 FE", "6.4-inch AMOLED", "50MP Main", "4500 mAh", "128GB/256GB", "$599", "Mint, Graphite, Purple"),
        ("Samsung Galaxy Z Fold 5", "7.6-inch Foldable", "50MP Main", "4400 mAh", "256GB/512GB", "$1799", "Icy Blue, Phantom Black"),
        ("Samsung Galaxy Z Flip 5", "6.7-inch Foldable", "12MP Main", "3700 mAh", "256GB/512GB", "$999", "Mint, Graphite, Lavender"),
        ("Samsung Galaxy S22 Ultra", "6.8-inch AMOLED", "108MP Main", "5000 mAh", "128GB/256GB/512GB", "$900", "Phantom Black, Burgundy"),
        ("Samsung Galaxy S22 Plus", "6.6-inch AMOLED", "50MP Main", "4500 mAh", "128GB/256GB", "$700", "White, Green, Pink Gold"),
        ("Samsung Galaxy S22", "6.1-inch AMOLED", "50MP Main", "3700 mAh", "128GB/256GB", "$600", "Phantom Black, Green"),
        ("Samsung Galaxy S21 Ultra", "6.8-inch AMOLED", "108MP Main", "5000 mAh", "128GB/256GB/512GB", "$800", "Phantom Black, Silver"),
        ("Samsung Galaxy S21 FE", "6.4-inch AMOLED", "12MP Main", "4500 mAh", "128GB/256GB", "$500", "Graphite, Olive, Lavender"),
        ("Samsung Galaxy Note 20 Ultra", "6.9-inch AMOLED", "108MP Main", "4500 mAh", "256GB/512GB", "$850", "Mystic Bronze, Black"),
        ("Samsung Galaxy A55", "6.6-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB/256GB", "$479", "Awesome Iceblue, Navy"),
        ("Samsung Galaxy A54", "6.4-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB/256GB", "$350", "Lime, Graphite, Violet"),
        ("Samsung Galaxy A35", "6.6-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB/256GB", "$399", "Iceblue, Lilac"),
        ("Samsung Galaxy A73 5G", "6.7-inch Super AMOLED", "108MP Main", "5000 mAh", "128GB/256GB", "$450", "Gray, Mint, White"),
        ("Samsung Galaxy M55", "6.7-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB/256GB", "$330", "Denim Black, Light Green"),
        ("Samsung Galaxy F55", "6.7-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB/256GB", "$360", "Apricot Crush, Black"),
        ("Samsung Galaxy XCover 7", "6.6-inch LCD", "50MP Main", "4050 mAh", "128GB", "$400", "Black"),
        ("Samsung Galaxy Quantum 4", "6.4-inch Super AMOLED", "50MP Main", "5000 mAh", "128GB", "$450", "Graphite, White"),
        ("Samsung Galaxy Z Fold 4", "7.6-inch Foldable", "50MP Main", "4400 mAh", "256GB/512GB", "$1499", "Graygreen, Beige"),
        ("Samsung Galaxy Z Flip 4", "6.7-inch Foldable", "12MP Main", "3700 mAh", "128GB/256GB", "$899", "Bora Purple, Blue"),
        ("Samsung Galaxy S21 Plus", "6.7-inch AMOLED", "12MP Main", "4800 mAh", "128GB/256GB", "$600", "Phantom Violet, Black"),
        ("Samsung W24", "7.6-inch Foldable", "50MP Main", "4400 mAh", "1TB", "$2200", "Gold, Gray"),
        ("Samsung W24 Flip", "6.7-inch Foldable", "12MP Main", "3700 mAh", "512GB", "$1300", "White, Gold")
    ]
    
    for p in phones:
        try:
            cursor.execute("INSERT INTO phones (model_name, display, camera, battery, storage, price, color) VALUES (%s, %s, %s, %s, %s, %s, %s)", p)
        except: continue
    conn.commit()
    cursor.close()
    conn.close()
    print("30 phones added successfully!")

if __name__ == "__main__":
    seed_database()