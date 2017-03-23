""" Parser for payments in csv"""
import csv
import datetime
import locale
import os
import tkinter as tk
from tkinter import filedialog


def get_days():
    """ Ask user and return int representing nr. of users."""
    while True:
        try:
            x = int(input("Údaje za kolik posledních dnů Vás zajímají? \n"))
            break
        except ValueError:
            print("Zadejte prosím číslo bez mezer")
    return x


def get_date_range():
    """ Return date range of of last user specified days."""
    days = get_days()
    from_date = datetime.datetime.now() + datetime.timedelta(-int(days))
    to_date = datetime.datetime.now()
    return from_date, to_date


def get_amount():
    """ Ask user and return float representation amount"""
    while True:
        try:
            amount = float(input("Nad jakou částku mají platby být? \n"
                                 "Zadejte prosím číslo bez mezer \n"))
            break
        except ValueError:
            print("Zadejte prosím částku bez mezer")
    return amount


# Show file dialog and get the path of the file
def get_file_path():
    """ Ask user and return path of file to filter"""
    root = tk.Tk()
    root.withdraw()
    user_file_path = filedialog.askopenfilename()
    return user_file_path


def get_csv_reader(csv_file, encoding, delimiter, quotechar):
    """ Open file in csv_reader and return the reader

    :param csv_file: file to open
    :param encoding: encoding of the file 
    :param delimiter: A one-character string used to separate fields
    :param quotechar: A one-character string used to quote fields 
                      containing special characters
    """
    opened_csv_file = open(csv_file, newline='', encoding=encoding)
    csv_reader = csv.reader(opened_csv_file,
                            delimiter=delimiter,
                            quotechar=quotechar)
    return csv_reader


def get_clean_table(columns, csv_reader):
    """ Return dictionary with specified columns. 

    :param columns: dictionary in the format {column_type: column_number} 
    required keys: date, name, var_symbol, amount
    value: int

    :param csv_reader: csv_reader with a file to filter
    """
    filtered_csv = []
    for csv_row in csv_reader:
        filtered_csv_row = [csv_row[columns['date']],
                            csv_row[columns['name']],
                            csv_row[columns['var_symbol']],
                            csv_row[columns['amount']]]
        filtered_csv.append(filtered_csv_row)
    return filtered_csv


def date_from_string(date_string, date_format):
    """ Return date string as datetime object

    :param date_string: string with date to parse
    :param date_format: date_string format following strptime(format)
                        directives
    """
    try:
        date = datetime.datetime.strptime(date_string, date_format)
    except ValueError:
        raise
    return date


def get_filtered_payments(payments):
    """ Return payment following user given filters

    :param payments: dictionary of payments 
                     must have keys date and amount
    """
    filtered_payments = []
    for payment in payments:
        try:
            dates = get_date_range()
            filter_amount = get_amount()
            if dates[0] <= payment['date'] <= dates[1]:
                if float(payment['amount']) >= filter_amount:
                    filtered_payments.append(payment)
        except ValueError:
            pass
                                                 
    return filtered_payments


def format_date(date):
    """ Return formatted date 

    :param date: datetime object
    """
    return (date.strftime('%d.%m.%Y')).strip()


def format_amount(amount_string):
    """ Return formatted amount

    :param amount_string: float amount string
    """
    return locale.format("%.2f", float(amount_string), grouping=True)


def create_final_file(filtered_payments, to_final_file):
    """ Use filtered payments to create formatted file

    :param filtered_payments: dictionary of payments
    :param to_final_file: string name of the final output file
    """
    try:
        os.remove(to_final_file)
    except OSError:
        pass

    file_out = open(to_final_file, 'w', encoding='utf-8')

    # Format text file to have columns aligned
    padding = 2
    # Calculate columns widths
    col_width_date = max(len(row[0]) for row in filtered_payments) + padding
    col_width_company = max(len(row[1]) for row in filtered_payments) + padding
    col_width_var_symbol = max(len(row[2]) for row in filtered_payments) + padding
    
    if len(filtered_payments) < 1:
        file_out.write("Nic nenalezeno")
    for row_final in filtered_payments:
        file_out.write(row_final[0].ljust(col_width_date)
                       + row_final[1].ljust(col_width_company)
                       + row_final[2].ljust(col_width_var_symbol)
                       + row_final[3].ljust(col_width_var_symbol)
                       + "\n")

    file_out.close()

    output_file_path = os.path.abspath(to_final_file)
    print("\n Soubor byl vytvořen. Jmenuje se " + to_final_file
          + "a je ve složce \n"
          "odkud jste spustil/a tento program, tedy zde: \n"
          + output_file_path)

