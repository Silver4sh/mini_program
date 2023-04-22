import csv, sqlite3

## Path data
csv_file = "list_anime.csv"
db_file = "anime.db"

## Connect to db
def connect_db(db_file):
    conn = sqlite3.connect(db_file, timeout=20)
    cur = conn.cursor()
    return conn, cur

# Created a DB
def created_db(db_file):
    conn, cur = connect_db(db_file)
    cur.execute("""
    CREATE TABLE anime_list (
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
    conn, cur = connect_db(db_file)
    with open(data_csv, mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(
            csv_file, 
            fieldnames=['Title', 'Genre_1', 'Genre_2', 
                        'Genre_3', 'Genre_4', 'Genre_5', 'Genre_6'])
        
        for row in csv_reader:
            placeholders = ', '.join(['?'] * len(row))
            query = 'INSERT INTO anime_list ({}) VALUES ({})'.format(
                ', '.join(row.keys()), placeholders)
            cur.execute(query, list(row.values()))

        conn.commit() # Commite data in db
        conn.close() # End season in db

try:
    created_db(db_file)
    import_data_to_db(csv_file)
except sqlite3.OperationalError:
    import_data_to_db(csv_file)