import codecs
import csv
import datetime
import locale
import os
import tkinter as tk
from tkinter import filedialog


# Dates
def get_dates_from_usr() -> (datetime.datetime, datetime.datetime):
    date_from_picker = None
    date_to_picker = None
    select_date_picker = input("Jaké dny Vás zajímají? \n"
                               "(1) Zadat datum od do \n"
                               "(2) Zadat o kolik dní zpátky (rozsah) \n"
                               "Pokud nic nezadáte a stisknete Enter, použije se varianta č. 2. \n"
                               "Zadejte číslo zvolené varianty: ")
    while select_date_picker != "1" and select_date_picker != "2" and select_date_picker != "":
        select_date_picker = input("\n Špatně zadáno, zkuste prosím znovu.: ")

    if select_date_picker == "1":

        # Datum OD
        user_date_from_string = input("\n Zadejte datum OD ve formátu rrrr/mm/dd  \n"
                                      "např. 2017/02/24 pro 24. února 2017 \n"
                                      "Pokud nic nezadáte a stisknete Enter, použije se "
                                      "datum před třiceti dny. \n")

        if user_date_from_string == "":
            date_from_picker = datetime.datetime.now() + datetime.timedelta(-30)
        else:
            while True:
                try:
                    date_from_picker = datetime.datetime.strptime(user_date_from_string, '%Y/%m/%d')
                    break
                except ValueError:
                    user_date_from_string = input("\n Špatně zadané datum. \n"
                                                  "Zadejte datum OD ve formátu rrrr/mm/dd  \n"
                                                  "např. 2017/02/24 pro 24. února 2017 \n")
                    continue

        # Datum DO
        user_date_to_string = input("\n Zadejte datum DO ve formátu rrrr/mm/dd \n"
                                    "např. 2017/02/26 pro 26. února 2017 \n"
                                    "Pokud nic nezadáte a stisknete Enter, použije se dnešní datum. \n")

        if user_date_to_string == "":
            date_to_picker = datetime.datetime.now()
        else:
            while True:
                try:
                    date_to_picker = datetime.datetime.strptime(user_date_to_string, '%Y/%m/%d')
                    break
                except ValueError:
                    user_date_to_string = input("\n Špatně zadané datum. \n"
                                                "Zadejte datum OD ve formátu rrrr/mm/dd  \n"
                                                "např. 2017/02/26 pro 26. února 2017 \n")
                    continue
    elif select_date_picker == "2" or select_date_picker == "":
        day_back_string = input("\n Údaje za kolik posledních dnů Vás zajímají? \n"
                                "Pokud nic nezadáte a stisknete Enter, použije se 30 dnů. \n")
        if day_back_string == "":
            date_from_picker = datetime.datetime.now() + datetime.timedelta(-30)
        else:
            while not day_back_string.isdigit():
                day_back_string = input("Špatně napsané číslo. Nezadal/a jste ho s mezerami? \n"
                                        "Zkuste to prosím znovu: ")
            date_from_picker = datetime.datetime.now() + datetime.timedelta(-int(day_back_string))
        date_to_picker = datetime.datetime.now()

    return date_from_picker, date_to_picker


# Amount
def get_amount_from_user() -> int:
    amount_user = input("\n Nad jakou částku mají platby být? \n"
                        "Zadejte prosím číslo bez mezer \n"
                        "Pokud nic nezadáte a stisknete Enter, použije se 30000. \n")
    if amount_user == "":
        amount_user_entered = 30000
        return amount_user_entered
    else:
        while not amount_user.isdigit():
            amount_user = input("Špatně napsané číslo. Nezadal/a jste ho s mezerami? \n"
                                "Zkuste to prosím znovu: ")
        return int(amount_user)


# Show file dialog and get the path of the file
def get_file_path_from_user() -> str:
    root = tk.Tk()
    root.withdraw()
    user_file_path = filedialog.askopenfilename()
    return user_file_path


# Change encoding of file to utf-8 and save it
def get_utf8_file(from_encode_file: str) -> str:
    to_encode_file = "records-utf8.csv"
    infile = codecs.open(from_encode_file, 'r', encoding='windows-1250')
    outfile = codecs.open(to_encode_file, 'w', encoding='utf-8')

    for line in infile:
        outfile.write(line)
    infile.close()
    outfile.close()

    return to_encode_file


# Load, filter and create a filtered csv
def create_filtered_csv(from_utf8_file: str) -> str:
    filtered_records_csv = "records-filter.csv"
    with open(from_utf8_file, newline='', encoding="utf-8") as from_utf8_file_csv:
        records_reader_csv = csv.reader(from_utf8_file_csv, delimiter=';', quotechar='"')

        # Prepare writer
        file_out_csv = open(filtered_records_csv, 'w', encoding='utf-8')
        writer_csv = csv.writer(file_out_csv, delimiter=';')

        # Filter results
        for row_csv in records_reader_csv:
            # Check if date row contains necessary data
            if 14 < len(row_csv):
                # header_row = None
                # Castka column
                input_string = row_csv[7]
                # Check if the column is number
                try:
                    value_csv = float(input_string.replace(',', '.'))
                # If it's not a number save it, because it's a header
                except ValueError:
                    # print("Header found")
                    continue
                else:
                    if value_csv >= money_value:
                        # Date column - Datum zpracovani
                        input_string_csv = row_csv[0]
                        # Check if the column is a date
                        try:
                            row_date_csv = datetime.datetime.strptime(input_string_csv, '%Y/%m/%d')
                        except ValueError:
                            continue
                        else:
                            if date_from <= row_date_csv <= date_to:
                                writer_csv.writerow(row_csv)
        from_utf8_file_csv.close()
        file_out_csv.close()
        return filtered_records_csv


def create_final_file(from_final_file: str) -> str:
    to_final_file = "PLATBY-CZ.txt"

    # Save to a file
    with open(from_final_file, newline='', encoding="utf-8") as from_final_file_csv:
        records_reader_final = csv.reader(from_final_file_csv, delimiter=';', quotechar='"')

        # Prepare writer
        # remove old file
        try:
            os.remove(to_final_file)
        except OSError:
            pass

        file_out = open(to_final_file, 'w', encoding='utf-8')

        # Filter columns and it's info to array
        info_array = []
        for row_final in records_reader_final:
            # Check if date row contains necessary data
            if 14 < len(row_final):
                # [Datum, Komu, Variabilni symbol, Castka]
                row_array = [row_final[13], row_final[9], row_final[16], row_final[3]]

                info_array.append(row_array)
        
        if len(info_array) < 1:
            # info_array = ["Nic Nenalezeno", "0" , "0", "0"]
            file_out.write("Nic nenalezeno")
        else:
            for row_final in info_array:
                # Change format of date
                temp_date = datetime.datetime.strptime(row_final[0], '%Y/%m/%d')
                row_final[0] = (temp_date.strftime('%d.%m.%Y')).strip()

                # Format Amount
                # locale.setlocale(locale.LC_ALL, '')
                temp_amount = locale.format("%.2f", float(row_final[3].replace(',', '.')), grouping=True)
                row_final[3] = temp_amount


            # Format text file to have columns aligned
            padding = 2
            # Calculate columns widths
            col_width_date = max(len(row[0]) for row in info_array) + padding
            col_width_company = max(len(row[1]) for row in info_array) + padding
            col_width_var_symbol = max(len(row[2]) for row in info_array) + padding

            for row_final in info_array:
                file_out.write(row_final[0].ljust(col_width_date)
                           + row_final[1].ljust(col_width_company)
                           + row_final[2].ljust(col_width_var_symbol)
                           + row_final[3].ljust(col_width_var_symbol)
                           + "\n")

        file_out.close()

    output_file_path = os.path.abspath(to_final_file)
    print("\n Soubor byl vytvořen. Jmenuje se PLATBY-CZ.TXT a je ve složce \n"
          "odkud jste spustil/a tento program, tedy zde: \n"
          + output_file_path)
    return to_final_file


def delete_cache_files():
    try:
        os.remove(utf8_file)
        os.remove(filtered_records_file)
    except OSError:
        pass


date_from, date_to = get_dates_from_usr()
money_value = get_amount_from_user()
file_path = get_file_path_from_user()
utf8_file = get_utf8_file(file_path)
filtered_records_file = create_filtered_csv(utf8_file)
final_file = create_final_file(filtered_records_file)
delete_cache_files()
