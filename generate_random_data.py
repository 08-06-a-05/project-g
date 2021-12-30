from export_data import Database

database = Database("Moneysite/db.sqlite3")
database.add_test_data_to_db()
database.close()
