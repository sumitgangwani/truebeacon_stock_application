import csv
import sqlite3

def create_database(database_name):
    """Create SQLite database and tables."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    # Create a table for Nifty data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nifty (
            date TEXT,
            price REAL,
            instrument_name TEXT
        )
    ''')

    # Create a table for user profiles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            user_id TEXT,
            user_type TEXT,
            email TEXT,
            user_name TEXT,
            broker TEXT,
            password TEXT
        )
    ''')

    # Create a table for holdings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holdings (
            user_id TEXT,
            tradingsymbol TEXT,
            exchange TEXT,
            isin TEXT,
            quantity INTEGER,
            authorised_date TEXT,
            average_price REAL,
            last_price REAL,
            close_price REAL,
            pnl REAL,
            day_change REAL,
            day_change_percentage REAL
        )
    ''')

    # Insert mock entry into profile table
    cursor.execute('''
        INSERT INTO profile (user_id, user_type, email, user_name, broker, password)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', ("AB1234", "individual", "xxxyyy@gmail.com", "AxAx Bxx", "ZERODHA", "1234"))

    # Insert mock data into holdings table
    holdings_data = [
        ("AB1234","GOLDBEES", "BSE", "INF204KB17I5", 2, "2021-06-08 00:00:00", 40.67, 42.47, 42.28, 3.6, 0.19, 0.44938505203405327),
        ("AB1234","IDEA", "NSE", "INE669E01016", 5, "2021-06-08 00:00:00", 8.466, 10, 10.1, 7.67, -0.1, -0.9900990099009866)
    ]

    cursor.executemany('''
        INSERT INTO holdings (
            user_id, tradingsymbol, exchange, isin, quantity, authorised_date,
            average_price, last_price, close_price, pnl, day_change, day_change_percentage
        )
        VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', holdings_data)

    connection.commit()
    connection.close()

def insert_data_from_csv(database_name, csv_file_path):
    """Insert data from CSV into SQLite database."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            cursor.execute('''
                INSERT INTO nifty (date, price, instrument_name)
                VALUES (?, ?, ?)
            ''', (row['date'], row['price'], row['instrument_name']))

    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Specify the SQLite database name
    db_name = "database/truebacon.db"

    # Specify the path to your CSV file
    csv_path = "historical_prices.csv"

    # Create the database and tables, including profile with mock entry and holdings with mock data
    create_database(db_name)

    # Insert data from CSV into the nifty table
    insert_data_from_csv(db_name, csv_path)

    print("Data inserted successfully.")
