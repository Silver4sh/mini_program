from prettytable import PrettyTable
import csv, sqlite3, os, sys

## Path data
#csv_file = "E:\\Latihan\\data\\anime.csv"
db = "E:\\Latihan\\script\\data_base\\anime.db"

## Connect to DB
def connect_db(db):
    conn = sqlite3.connect(db, timeout=10)
    cur = conn.cursor()
    return conn, cur

# Created DB
def make_db(database):
    database[1].execute("""
    CREATE TABLE IF NOT EXISTS anime_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT,
        Genre_1 TEXT,
        Genre_2 TEXT,
        Genre_3 TEXT,
        Genre_4 TEXT,
        Genre_5 TEXT,
        Genre_6 TEXT)
    """)
    database[0].commit()

# Import data to DB
def import_data(database,data_csv):
    with open(data_csv, mode="r", encoding="utf-8-sig") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Check if the data already exists in the database
            database[1].execute("SELECT * FROM anime_list WHERE Title=?", [row["Title"]])
            if database[1].fetchone() is None:
                placeholders = ", ".join(["?"] * len(row))
                query = "INSERT INTO anime_list ({}) VALUES ({})".format(", ".join(row.keys()), placeholders)
                database[1].execute(query, list(row.values()))
        database[0].commit() # Commit data in db

# Menu
def menu():
    os.system("cls")
    database = connect_db(db)
    main_menu = False
    print("---------------\nWellcome to MyAnime List!\n---------------")
    while main_menu == False:
        ans1 = int(input("[0]Show All Anime\n[1]Search Anime\n[2]Insert Data\n[99]Exit\n\nChoose Menu > "))
        os.system("cls")
        if ans1 == 0:
            datas = database[1].execute("SELECT Title, Genre_1, Genre_2, Genre_3, Genre_4, Genre_5, Genre_6 FROM anime_list")
            if not datas:
                print("Anime list is empty.")
            else:
                table = PrettyTable()
                table.field_names = ["Title", "Genre 1", "Genre 2", "Genre 3", "Genre 4", "Genre 5", "Genre 6"]
                for data in datas:
                    table.add_row(data)
            print(table)
        elif ans1 == 1:
            database = connect_db(db) # Connect in DB
            if not database[1].execute("SELECT id FROM anime_list").fetchall():
                print("Empty Data\nPliss Insert data...\n")
            else :
                print(2)
        elif ans1 == 2:
            print("Format: Tittle, Genre_1, Genre_2, Genre_3, Genre_4, Genre_5, Genre_6")
            path_csv = input("*without header\n[99]Back\nDrag n Drop file in this area: ")
            if path_csv == "99":
                os.system("cls")
            else:
                try:
                    make_db(database)
                    import_data(database,path_csv)
                    os.system('cls')
                    print("Done make and inject a database!!\n")
                except sqlite3.OperationalError:
                    import_data(database,path_csv)
                    os.system("cls")
                    print("Done inject a database!!\n")
                except FileNotFoundError:
                    os.system("cls")
                    print("False Path\n")
                except OSError:
                    os.system("cls")
                    print("Data already!!\n")
        elif ans1 == 99:
            print("---------------\nThankyou for coming!!\n---------------\n")
            database[0].close()
            sys.exit(1)
        else: 
            print("---------------\nThat is not a valid number.\n---------------\n")
            database[0].close()

menu()