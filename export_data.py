import datetime
import random
import sqlite3


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

    def get_operations_for_user(self, user_id: int):
        request = "SELECT datetime, operation_type, amount, currency, description FROM operations_operations \
        WHERE user_id = :user_id;"

        result = self.__cursor.execute(request, {"user_id": str(user_id)})
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


class OperationInfo:
    pass


def mainloop():
    invitation = "Введите id пользователя или q для выхода: "
    info_for_user = "Информация о пользователе с id="

    database = Database("Moneysite/db.sqlite3")

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
            result = database.get_operations_for_user(user_id)
            for r in result:
                print(r)
        print()


def add_test_data():
    database = Database("Moneysite/db.sqlite3")
    database.add_test_data_to_db()
    database.close()


if __name__ == "__main__":
    mainloop()
    # add_test_data()
