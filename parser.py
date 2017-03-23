import codecs
import csv
import datetime
import locale
import os
import pandas
import tkinter as tk
from tkinter import filedialog


def get_days():
    while True:
        try:
            x = int(input("Údaje za kolik posledních dnů Vás zajímají? \n"))
            break
        except ValueError:
            print("Zadejte prosím číslo bez mezer")
    return x


def get_date_range():
    days = get_days()
    from_date = datetime.datetime.now() + datetime.timedelta(-int(days))
    to_date = datetime.datetime.now()
    return from_date, to_date


def get_amount():
    while True:
        try:
            amount = int(input("Nad jakou částku mají platby být? \n"
                         "Zadejte prosím číslo bez mezer \n"))
            break
        except ValueError:
            print("Zadejte prosím částku bez mezer")
    return amount


# Show file dialog and get the path of the file
def get_file_path():
    root = tk.Tk()
    root.withdraw()
    user_file_path = filedialog.askopenfilename()
    return user_file_path


def get_csv_reader(csv_file, encoding, delimiter, quotechar):
    opened_csv_file = open(csv_file, newline='', encoding=encoding)
    csv_reader = csv.reader(opened_csv_file,
                            delimiter=delimiter,
                            quotechar=quotechar)
    return csv_reader


def get_table_without_header(columns, csv_reader):
    columns = [amount:, date:, name: symbol:]
    filtered_csv = []
    for csv_row in csv_reader:
        try:
            amount = float(csv_row[columns[amount]])
        except ValueError:
            pass
        else:
            filtered_csv_row = [csv_row[columns[date]],
                                csv_row[columns[name]],
                                csv_row[columns[symbol]],
                                csv_row[columns[amount]]]
            filtered_csv.append(filtered_csv_row)
    return filtered_csv


def date_from_string(date_string, date_format):
    try:
        date = datetime.datetime.strptime(date_string, date_format)
    except ValueError:
        raise
    return date


def get_filtered_payments(payments, filter_amount):
    filtered_payments = []
    for payment in payments:
        try:
            dates = get_date_range()
            filter_amount = get_amount()
            if dates[0] <= payment[date] <= dates[1]:
                if float(payment[amount]) >= filter_amount:
                    filtered_payments.append(payment)
        except ValueError:
            pass
                                                 
    return filtered_payments


def create_final_file(filtered_payments, to_final_file):
    try:
        os.remove(to.final_file)
    except OSError:
        pass

    file_out = open(to_final_file, 'w', encoding='utf-8')

    if len(filtered_payments) < 1:
        file_out.write("Nic nenalezeno")
    else:
        for row_final in filtered_payments:
