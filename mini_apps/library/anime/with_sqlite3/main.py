import csv, sqlite3

## Path data
csv_file = "E:\\Latihan\\data\\anime.csv"
db = "E:\\Latihan\\script\\data_base\\anime.db"

## Connect to db
def connect_db(db):
    conn = sqlite3.connect(db, timeout=20)
    cur = conn.cursor()
    return conn, cur

# Created a DB
def make_db(db):
    conn, cur = connect_db(db)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS anime_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Genre_1 TEXT,
        Genre_2 TEXT,
        Genre_3 TEXT,
        Genre_4 TEXT,
        Genre_5 TEXT,
        Genre_6 TEXT
    )
    """)
    conn.commit()
    conn.close()

def import_data_to_db(data_csv):
    conn, cur = connect_db(db)
    with open(data_csv, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
  
        for row in csv_reader:
            # Check if the data already exists in the database
            cur.execute("SELECT * FROM anime_list WHERE Title=?", [row['Title']])
            if cur.fetchone() is None:
                placeholders = ', '.join(['?'] * len(row))
                query = 'INSERT INTO anime_list ({}) VALUES ({})'.format(
                    ', '.join(row.keys()), placeholders)
                cur.execute(query, list(row.values()))
            
        conn.commit() # Commit data in db
        conn.close() # End session in db


try:
    make_db(db)
except sqlite3.OperationalError:
    pass

import_data_to_db(csv_file)
