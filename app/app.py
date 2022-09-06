from spreadsheet import orderSheet
from db import orderTable
from time import sleep


if __name__ == '__main__':
    while True:
        google_data = orderSheet.get_rows()
        print(google_data)
        orderTable.update_table(google_data)
        sleep(60)