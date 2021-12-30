from export_data import Database

database = Database("./export_data/db.sqlite3")
database.add_test_data_to_db()
database.close()
