import os
import unittest

import openpyxl

from export_data import Database, XlsxBook


class TestDatabase(unittest.TestCase):
    """
    Class for testing Database class
    """
    DB_PATH = "../export_data/test_db.db"
    database = None

    @classmethod
    def del_db_file(cls):
        if os.path.isfile(cls.DB_PATH):
            os.remove(cls.DB_PATH)

    @classmethod
    def setUpClass(cls):
        cls.del_db_file()
        cls.database = Database(path=cls.DB_PATH)
        cls.database.cursor.executescript(
            """
BEGIN TRANSACTION;
CREATE TABLE "operations_operations" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"operation_type" varchar(30) NOT NULL,
"datetime" datetime NOT NULL,
"amount" bigint unsigned NOT NULL CHECK ("amount" >= 0),
"currency" varchar(60) NOT NULL,
"description" text NOT NULL,
"category_id" bigint NOT NULL REFERENCES"operations_categories" ("id") DEFERRABLE INITIALLY DEFERRED,
"user_id" bigint NOT NULL REFERENCES "account_manager_users" ("id") DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE "operations_categories" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"category_name" varchar(60) NOT NULL,
"user_id" bigint NOT NULL REFERENCES "account_manager_users" ("id") DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 1', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 2', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 3', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 4', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 5', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 6', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 7', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 8', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 9', '0');
INSERT INTO "operations_categories" ("category_name", "user_id") VALUES ('category 10', '0');

INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2021-10-29 21:09:45.209337', '187', 'rub', 'description', '7', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2020-12-29 21:09:45.210184', '927', 'rub', 'description', '2', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('+', '2021-12-01 00:09:45.210271', '467', 'rub', 'description', '8', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2021-05-05 21:09:45.210329', '779', 'rub', 'description', '9', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2021-12-29 21:09:45.210360', '205', 'rub', 'description', '9', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('+', '2019-12-15 21:09:45.210391', '917', 'rub', 'description', '1', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2020-11-11 18:15:45.210426', '130', 'rub', 'description', '6', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('+', '2021-06-08 21:09:45.210466', '228', 'rub', 'description', '4', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('-', '2015-08-27 21:09:45.210499', '698', 'rub', 'description', '8', '1');
INSERT INTO "operations_operations" ("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ('+', '2021-03-20 16:09:45.210532', '693', 'rub', 'description', '9', '1');
            """)
        cls.database.connection.commit()

    @classmethod
    def tearDownClass(cls):
        cls.database.close()
        cls.del_db_file()

    def test_get_all_operations(self):
        # Arrange
        operations = [('2021-10-29 21:09:45.209337', '-', 187, 'rub', 'category 7', 'description'),
                      ('2020-12-29 21:09:45.210184', '-', 927, 'rub', 'category 2', 'description'),
                      ('2021-12-01 00:09:45.210271', '+', 467, 'rub', 'category 8', 'description'),
                      ('2021-05-05 21:09:45.210329', '-', 779, 'rub', 'category 9', 'description'),
                      ('2021-12-29 21:09:45.210360', '-', 205, 'rub', 'category 9', 'description'),
                      ('2019-12-15 21:09:45.210391', '+', 917, 'rub', 'category 1', 'description'),
                      ('2020-11-11 18:15:45.210426', '-', 130, 'rub', 'category 6', 'description'),
                      ('2021-06-08 21:09:45.210466', '+', 228, 'rub', 'category 4', 'description'),
                      ('2015-08-27 21:09:45.210499', '-', 698, 'rub', 'category 8', 'description'),
                      ('2021-03-20 16:09:45.210532', '+', 693, 'rub', 'category 9', 'description')]
        # Act
        result = self.database.get_operations_for_user(user_id=1)
        # Assert
        self.assertEqual(result, operations)

    def test_get_operations_from_date(self):
        # Arrange
        operations = [('2021-10-29 21:09:45.209337', '-', 187, 'rub', 'category 7', 'description'),
                      ('2021-12-01 00:09:45.210271', '+', 467, 'rub', 'category 8', 'description'),
                      ('2021-05-05 21:09:45.210329', '-', 779, 'rub', 'category 9', 'description'),
                      ('2021-12-29 21:09:45.210360', '-', 205, 'rub', 'category 9', 'description'),
                      ('2021-06-08 21:09:45.210466', '+', 228, 'rub', 'category 4', 'description'),
                      ('2021-03-20 16:09:45.210532', '+', 693, 'rub', 'category 9', 'description')]
        date = "2021-01-01"
        # Act
        result = self.database.get_operations_for_user(user_id=1, start_date=date)
        # Assert
        self.assertEqual(result, operations)

    def test_get_operations_until_date(self):
        # Arrange
        operations = [('2020-12-29 21:09:45.210184', '-', 927, 'rub', 'category 2', 'description'),
                      ('2019-12-15 21:09:45.210391', '+', 917, 'rub', 'category 1', 'description'),
                      ('2020-11-11 18:15:45.210426', '-', 130, 'rub', 'category 6', 'description'),
                      ('2015-08-27 21:09:45.210499', '-', 698, 'rub', 'category 8', 'description')]
        date = "2021-01-01"
        # Act
        result = self.database.get_operations_for_user(user_id=1, finish_date=date)
        # Assert
        self.assertEqual(result, operations)

    def test_get_operations_from_one_date_until_second_date(self):
        # Arrange
        operations = [('2020-12-29 21:09:45.210184', '-', 927, 'rub', 'category 2', 'description'),
                      ('2019-12-15 21:09:45.210391', '+', 917, 'rub', 'category 1', 'description'),
                      ('2020-11-11 18:15:45.210426', '-', 130, 'rub', 'category 6', 'description')]
        start_date = "2019-01-01"
        finish_date = "2020-12-31"
        # Act
        result = self.database.get_operations_for_user(user_id=1, start_date=start_date, finish_date=finish_date)
        # Assert
        self.assertEqual(result, operations)


class TestXlsxBook(unittest.TestCase):
    """
    Class for testing XlsxBook class
    """
    BOOK_PATH = "../export_data/test_book.xlsx"
    database = None

    @classmethod
    def del_book_file(cls):
        if os.path.isfile(cls.BOOK_PATH):
            os.remove(cls.BOOK_PATH)

    @classmethod
    def setUpClass(cls):
        cls.del_book_file()
        cls.book = XlsxBook(cls.BOOK_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.del_book_file()

    def test_create_table(self):
        # Arrange
        written_data = [['2020-12-29 21:09:45.210184', '-', 927, 'rub', 'category 2', 'description'],
                        ['2019-12-15 21:09:45.210391', '+', 917, 'rub', 'category 1', 'description']]
        headers = ["Date", "Operation type", "Amount", "Currency", "Category", "Description"]
        # Act for method under test
        self.book.create_table(written_data)
        self.book.save_file()
        self.book.close()
        # Act for check
        read_data = self.__get_data_from_xlsx_file()
        # Assert
        self.assertEqual([headers] + written_data, read_data)

    def __get_data_from_xlsx_file(self):
        book = openpyxl.open(self.BOOK_PATH, read_only=True)
        sheet = book.active

        read_data = []
        for i in range(1, sheet.max_row + 1):
            line = []
            for j in range(len(XlsxBook.TABLE_HEADERS)):
                line.append(sheet[i][j].value)
            read_data.append(line)

        book.close()

        return read_data


if __name__ == "__main__":
    unittest.main(failfast=False)
