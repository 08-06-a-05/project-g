import datetime
import sqlite3
from typing import Optional

import openpyxl
import openpyxl.styles


class Database:
    """
    Class for working with database
    """

    def __init__(self, path: str):
        self.__connection = sqlite3.connect(path)  # Database object
        self.__cursor = self.__connection.cursor()

    def close(self):
        self.__connection.close()

    def get_operations_for_user(self, user_id: int,
                                start_date: Optional[str] = None,
                                finish_date: Optional[str] = None):
        """

        :param user_id: id of the user whose operations information needs to be obtained
        :param start_date: from this date ("%Y-%m-%d")
        :param finish_date: until this date ("%Y-%m-%d")
        :return:
        """
        request = """SELECT datetime, operation_type, amount, currency, \
        (SELECT category_name FROM operations_categories WHERE \
        operations_categories.id = operations_operations.category_id), \
        description \
        FROM operations_operations \
        WHERE user_id = :user_id"""

        if start_date is not None:
            request += " AND datetime >= :start_date"

        if finish_date is not None:
            request += " AND datetime <= :finish_date)"

        request += ";"

        values = {"user_id": str(user_id),
                  "start_date": start_date,
                  "finish_date": finish_date}

        result = self.__cursor.execute(request, values)
        return result.fetchall()


class XlsxBook:
    """
    Class for saving data into .xlsx
    """

    TABLE_HEADERS = ["Date", "Operation type", "Amount", "Currency", "Category", "Description"]

    def __init__(self, path: str):
        self.__path = path
        self.__book = openpyxl.Workbook()
        self.__sheet = self.__book.active

    def create_table(self, data):
        """
        Create stylized table with headers and data.

        :param data: information about user's operations to be written to the table
        """
        self.__create_headers()
        self.__write_data(data)
        self.__add_styles()

    def save_file(self):
        self.__book.save(self.__path)

    def close(self):
        self.__book.close()

    def __create_headers(self):
        for i in range(len(self.TABLE_HEADERS)):
            self.__sheet[chr(i + 97) + "1"] = self.TABLE_HEADERS[i]

    def __write_data(self, data):
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.__sheet[2 + i][j].value = data[i][j]

    def __add_styles(self):
        self.__set_columns_width()
        self.__set_font_and_borders()

    def __set_columns_width(self):
        for i in range(len(self.TABLE_HEADERS)):
            self.__sheet.column_dimensions[chr(i + 97)].width = 18

    def __set_font_and_borders(self):
        bold_font = openpyxl.styles.Font(b=True, name="Arial")
        light_font = openpyxl.styles.Font(name="Arial")

        side = openpyxl.styles.Side(style="hair")
        border = openpyxl.styles.Border(left=side, right=side, top=side, bottom=side)
        for j in range(1, self.__sheet.max_row + 1):
            for i in range(len(self.TABLE_HEADERS)):
                self.__sheet[j][i].border = border
                if j == 1:
                    self.__sheet[j][i].font = bold_font
                else:
                    self.__sheet[j][i].font = light_font


class OperationsInfo:
    def __init__(self, user_id: int):
        self.__user_id = user_id
        self.__operations = None

    def load_from_db(self,
                     path: str,
                     start_date: Optional[str] = None,
                     finish_date: Optional[str] = None):
        """
        :param path: path to database file,
        :param start_date: from this date ("%Y-%m-%d")
        :param finish_date: until this date ("%Y-%m-%d")
        :return: list with info about user's operations
        """
        database = Database(path)
        self.__operations = database.get_operations_for_user(self.__user_id, start_date, finish_date)
        database.close()

    def change_datetime_format(self):
        new_operations = self.__operations
        for i in range(len(self.__operations)):
            new_operations[i] = list(self.__operations[i])
            new_operations[i][0] = self.__transform_datetime(new_operations[i][0])
        self.__operations = new_operations

    def export_to_xlsx_file(self, path: str):
        book = XlsxBook(path)
        book.create_table(self.__operations)
        book.save_file()

    def print_to_terminal(self):
        for operation in self.__operations:
            print(operation)

    @staticmethod
    def __transform_datetime(input_str):
        """
        Transform string with datetime from "%Y-%m-%d %H:%M:%S.%f" format into "%d.%m.%Y %H:%M" format
        """
        return datetime.datetime.strptime(input_str, "%Y-%m-%d %H:%M:%S.%f").strftime("%d.%m.%Y %H:%M")


def mainloop():
    user_id_inv = "Введите id пользователя или 'q' для выхода: "
    start_date_inv = "Введите дату в формате %Y-%m-%d, начиная с которой необходимо вывести операции, \
или 's', чтобы вывести опреции с первой: "
    finish_date_inv = "Введите дату в формате %Y-%m-%d, до которой необходимо вывести операции, \
или 'f', чтобы вывести опреции до последней: "

    info_for_user = "Информация о пользователе с id="
    info_saved = "Сохранено в .xlsx файл"

    while True:
        input_data = input(user_id_inv)
        print()
        if input_data == "q":
            print("bye")
            return
        else:
            user_id = int(input_data)

            start_date = input(start_date_inv)
            start_date = None if start_date == "s" else start_date

            finish_date = input(finish_date_inv)
            finish_date = None if finish_date == "f" else finish_date

            operations = OperationsInfo(user_id=user_id)
            operations.load_from_db("../export_data/db.sqlite3", start_date=start_date, finish_date=finish_date)
            operations.change_datetime_format()

            print(info_for_user + f"{user_id}:")
            operations.print_to_terminal()
            operations.export_to_xlsx_file(f"../export_data/data_{user_id}.xlsx")
            print(info_saved)

        print()


if __name__ == "__main__":
    mainloop()
