import datetime
import random
import sqlite3

import openpyxl


class Database:
    """
    Class for working with database
    """

    def __init__(self, path: str):
        self.__connection = sqlite3.connect(path)  # Database object
        self.__cursor = self.__connection.cursor()

    @property
    def connection(self):
        return self.__connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.__cursor

    def close(self):
        self.__connection.close()

    def get_all_operations_for_user(self, user_id: int):
        request = """SELECT datetime, operation_type, amount, currency,
        (SELECT category_name FROM operations_categories WHERE operations_categories.id = operations_operations.category_id),
        description
        FROM operations_operations 
        WHERE user_id = :user_id;"""

        result = self.__cursor.execute(request, {"user_id": str(user_id)})
        return result.fetchall()

    def get_operations_for_the_period_for_user(self, user_id: int, start_date: str, finish_date: str):
        request = """SELECT datetime, operation_type, amount, currency,
                (SELECT category_name FROM operations_categories WHERE operations_categories.id = operations_operations.category_id),
                description
                FROM operations_operations 
                WHERE user_id = :user_id AND (datetime >= :start_date AND datetime <= :finish_date);"""

        keys = {"user_id": str(user_id),
                "start_date": start_date,
                "finish_date": finish_date}
        result = self.__cursor.execute(request, keys)
        return result.fetchall()

    def add_test_data_to_db(self):
        N = 10
        for i in range(N):
            request = f'INSERT INTO operations_operations' \
                      f'("operation_type", "datetime", "amount", "currency", "description", "category_id", "user_id") VALUES ' \
                      f'("{random.choice(("+", "-"))}", "{datetime.datetime.now()}",' \
                      f'{random.randint(0, 1000)}, "rub", "description", {random.randint(1, 10)}, 1);'
            self.__cursor.execute(request)
        self.__connection.commit()


""" .strftime() """


class XlsxBook():
    def __init__(self, name: str):
        self.__name = name
        self.__book = openpyxl.Workbook()
        self.__sheet = self.__book.active

    def create_headers(self):
        self.__sheet["A1"] = "Date"
        self.__sheet["B1"] = "Operation type"
        self.__sheet["C1"] = "Amount"
        self.__sheet["D1"] = "Currency"
        self.__sheet["E1"] = "Category"
        self.__sheet["F1"] = "Description"

    def write_data(self, operations):
        for i in range(len(operations)):
            for j in range(len(operations[i])):
                self.__sheet[2 + i][j].value = operations[i][j]

    def save(self):
        self.__book.save(self.__name + ".xlsx")

    def close(self):
        self.__book.close()


def export_operations_to_xlsx(operations):
    book = XlsxBook(name="./export_data/my_book")
    book.create_headers()

    book.write_data(operations)

    book.save()
    book.close()


def print_operations(operations):
    for operation in operations:
        print(operation)


def transform_datetime(input_str):
    return datetime.datetime.strptime(input_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%d.%m.%Y %H:%M")


def transform_datetime_in_all_operations(operations):
    new_operations = operations
    for i in range(len(operations)):
        new_operations[i] = list(operations[i])
        new_operations[i][0] = transform_datetime(new_operations[i][0])
    return new_operations


def mainloop():
    invitation = "Введите id пользователя или q для выхода: "
    info_for_user = "Информация о пользователе с id="

    database = Database("./export_data/db.sqlite3")

    print()
    while True:
        input_data = input(invitation)
        if input_data == "q":
            print("close db")
            database.close()
            return
        else:
            user_id = int(input_data)
            print(info_for_user + f"{user_id}:")
            start_date = "2021-01-29"
            finish_date = "2022-01-01"
            # operations = database.get_all_operations_for_user(user_id)
            operations = database.get_operations_for_the_period_for_user(user_id, start_date, finish_date)
            operations = transform_datetime_in_all_operations(operations)

            print_operations(operations)
            export_operations_to_xlsx(operations)
        print()


if __name__ == "__main__":
    mainloop()
