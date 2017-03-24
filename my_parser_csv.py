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


def get_csv_reader(encoding, delimiter, quotechar):
    """ Open file in csv_reader and return the reader

    :param encoding: encoding of the file 
    :param delimiter: A one-character string used to separate fields
    :param quotechar: A one-character string used to quote fields 
                      containing special characters
    """
    csv_file = get_file_path()
    opened_csv_file = open(csv_file, newline='', encoding=encoding)
    csv_reader = csv.reader(opened_csv_file,
                            delimiter=delimiter,
                            quotechar=quotechar)
    return csv_reader


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


def get_payments(columns, csv_reader, date_format):
    """ Return dictionary with specified columns. 

    :param columns: dictionary in the format {column_type: column_number} 
    required keys: date, name, var_symbol, amount
    value: int

    :param csv_reader: csv_reader with a file to filter
    """
    filtered_csv = []
    for csv_row in csv_reader:
       # Check if it's a header or incomplete row
        if len(csv_row) < 5: 
            continue

        try:
            if (csv_row[columns['amount']][1]).isalpha():
                continue
        except IndexError:
            continue
        except ValueError:
            continue

        temp_date = date_from_string(csv_row[columns['date']], date_format)         
        filtered_csv_row = { 'date': temp_date,
                            'name': csv_row[columns['name']],
                            'var_symbol': csv_row[columns['var_symbol']],
                            'amount': csv_row[columns['amount']]}
        filtered_csv.append(filtered_csv_row)
    return filtered_csv


def filter_payments(payments):
    """ Return payment following user given filters

    :param payments: dictionary of payments 
                     must have keys date and amount
    """
    dates = get_date_range()
    filter_amount = get_amount()
    filtered_payments = []
    for payment in payments:
        try:
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
    locale.setlocale(locale.LC_ALL, '')
    return locale.format("%.2f", float(amount_string), grouping=True)


def create_final_file(filtered_payments, to_final_file):
    """ Use filtered payments to create formatted file

    :param filtered_payments: dictionary of payments
    :param to_final_file: string name of the final output file
    """
    to_final_file = os.path.expanduser("~/Desktop/" + to_final_file)
    try:
        os.remove(to_final_file)
    except OSError:
        pass

    file_out = open(to_final_file, 'w', encoding='utf-8')

    if len(filtered_payments) < 1:
        file_out.write("Nic nenalezeno")
    else:
       # Format text file to have columns aligned
        padding = 4
        # Calculate columns widths
        col_width_date = max(len(row['date']) for row in filtered_payments) + padding
        col_width_company = max(len(row['name']) for row in filtered_payments) + padding
        col_width_var_symbol = max(len(row['var_symbol']) for row in filtered_payments) + padding
        col_width_amount = max(len(row['amount']) for row in filtered_payments)
      
        for row_final in filtered_payments:
            file_out.write(row_final['date'].ljust(col_width_date)
                           + row_final['name'].ljust(col_width_company)
                           + row_final['var_symbol'].ljust(col_width_var_symbol)
                           + row_final['amount'].rjust(col_width_amount)
                           + "\n")

    file_out.close()

    output_file_path = os.path.abspath(to_final_file)
    print("\n Soubor byl vytvořen. Jmenuje se " + to_final_file
          + "a je ve složce \n"
          + output_file_path)
