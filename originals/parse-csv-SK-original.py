import tkinter as tk
from tkinter import filedialog
import csv
import codecs
import datetime
import os
import locale


# Dates
date_from = None
date_to = None

select_date_picker = input("(1) Zadat datum od do" + "\n"
                           + "(2) Zadat o kolik dní zpátky" + "\n"
                           + "Bez zadání automaticky nastaví variantu 2" + "\n"
                           + "Zadejte zvolené číslo: ")
while select_date_picker != "1" and select_date_picker != "2" and select_date_picker != "":
    select_date_picker = input("\n" + "Špatně zadáno, zkuste prosím znovu.: ")

if select_date_picker == "1":
    user_date_from_string = input("\n" + "Zadejte datum OD ve formátu rrrr/mm/dd  " + "\n"
                                  + "např. 2017/02/24 pro 24. února 2017" + "\n"
                                  + "Bez zadání nastaví datum před třiceti dny"
                                  + "\n")
    date_from = datetime.datetime.strptime(user_date_from_string, '%Y/%m/%d')

    if user_date_from_string == "":
        user_date_from_string = datetime.datetime.now() + datetime.timedelta(-30)

    user_date_to_string = input("\n" + "Zadejte datum OD ve formátu rrrr/mm/dd  " + "\n"
                                  + "např. 2017/02/24 pro 24. února 2017" + "\n"
                                  + "Bez zadání vyplní dnešek"
                                  + "\n")
    date_to = datetime.datetime.strptime(user_date_to_string, '%Y/%m/%d')
    if user_date_to_string == "":
        user_date_to_string = datetime.datetime.now()
elif select_date_picker == "2" or select_date_picker == "":
    dayBackString = input("\n" + "Z kolika dnů zpátky? Bez zadání je nastaveno 30 dnů: " + "\n")
    if dayBackString == "":
        date_from = datetime.datetime.now() + datetime.timedelta(-30)
    else:
        date_from = datetime.datetime.now() + datetime.timedelta(-int(dayBackString))
    date_to = datetime.datetime.now()


# Amount
money_value = input("\n" + "Nad jakou částku mají platby být?" + "\n"
                    + "Zadejte číslo bez mezer" + "\n"
                    + "Nevyplňujte pro 30 000"
                    + "\n")
if money_value == "":
    money_value = 30000
else:
    money_value = int(money_value)


# Show file dialog and get the path of the file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Change encoding of file to utf-8 and save it
utf8_file = "records-utf8.csv"
infile = codecs.open(file_path, 'r', encoding='windows-1250')
outfile = codecs.open(utf8_file, 'w', encoding='utf-8')

for line in infile:
    outfile.write(line)
infile.close()
outfile.close()

# Load csv
filtered_records_file = "records-filter.csv"
with open(utf8_file, newline='', encoding="utf-8") as csvfile:
    records_reader = csv.reader(csvfile, delimiter=';', quotechar='"')

    # Prepare writer
    file_out = open(filtered_records_file, 'w', encoding='utf-8')
    writer = csv.writer(file_out, delimiter=';')

    # Filter results
    for row in records_reader:
        # Check if date row contains necessary data
        if 14 < len(row):
            header_row = None
            # Castka column
            # print(row[3])
            input_string = row[7]
            # Check if the column is number
            try:
                value = float(input_string)
            # If it's not a number save it, because it's a header
            except ValueError as e:
                # print("Header found")
                continue
            else:
                if value >= money_value:
                    # Date column - Datum zpracovani
                    input_string = row[0]
                    # Check if the column is a date
                    try:
                        row_date = datetime.datetime.strptime(input_string, '%d.%m.%Y')
                    except ValueError as e:
                        continue
                    else:
                        if row_date >= date_from and row_date <= date_to:
                            writer.writerow(row)
    csvfile.close()
    file_out.close()

# Keep only columns I want
filtered_records_file_without_columns = "PLATBY.txt"

# Save to a file
with open(filtered_records_file, newline='', encoding="utf-8") as csvfile:
    records_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    # for row in records_reader:
    #     print(', '.join(row))

    # Prepare writer
    # remove old file
    try:
        os.remove(filtered_records_file_without_columns)
    except OSError:
        pass

    file_out = open(filtered_records_file_without_columns, 'w', encoding='utf-8')
    # writer = csv.writer(file_out, delimiter=';')


    # Filter columns and it's info to array
    infoArray = []
    for row in records_reader:
        # Check if date row contains necessary data
        if 14 < len(row):
            rowArray = []
            # Datum
            rowArray.append(row[0])
            # Komu
            rowArray.append(row[6])
            # Variabilni symbol
            rowArray.append(row[13])
            # Castka
            rowArray.append(row[7])

            infoArray.append(rowArray)

    # Change format of date
    for row in infoArray:
        tempDate = datetime.datetime.strptime(row[0], '%d.%m.%Y')
        row[0] = (tempDate.strftime('%d.%m.%Y')).strip()

    # Format Amount
    for row in infoArray:
        locale.setlocale(locale.LC_ALL, '')
        tempAmount = locale.format("%.2f", float(row[3].replace(',', '.')), grouping=True)
        row[3] = tempAmount

    # Format text file to have columns aligned
    padding = 2
    # Calculate columns widths
    col_width_date = max(len(row[0]) for row in infoArray ) + padding
    col_width_company = max(len(row[1]) for row in infoArray ) + padding
    col_width_varsymb = max(len(row[2]) for row in infoArray ) + padding
    col_width_amount = max(len(row[3]) for row in infoArray ) + padding

    col_width = max(len(word) for row in infoArray for word in row) + 2
    for row in infoArray:
        file_out.write(row[0].ljust(col_width_date)
                       + row[1].ljust(col_width_company)
                       + row[2].ljust(col_width_varsymb)
                       + row[3].ljust(col_width_varsymb)
                       + "\n")

    file_out.close()

print("Soubor byl vytvořen. Jmenuje se PLATBY.TXT")

try:
    os.remove(utf8_file)
    os.remove(filtered_records_file)
except OSError:
    pass
