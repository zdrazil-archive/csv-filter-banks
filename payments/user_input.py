# coding=utf-8
""" user_input - Getting data from/to user"""
import datetime
import tkinter as tk
from tkinter import filedialog
from typing import List

from payments.model import my_io


def get_days():
    """Ask user and return int representing nr. of users."""
    while True:
        try:
            days = int(input("Údaje za kolik posledních dnů Vás zajímají? \n"))
            break
        except ValueError:
            print("Zadejte prosím číslo bez mezer")
    return days


def get_date_range() -> (datetime, datetime):
    """ Return date range of last user specified days.

    :return: Tuple in the format of (datetime_from, datetime_to)
    """
    days = get_days()
    return my_io.days_to_date_range(days)


def get_amount() -> float:
    """ Ask user and return float amount by which to filter."""
    while True:
        try:
            amount = float(input("Nad jakou částku mají platby být? \n"
                                 "Zadejte prosím číslo bez mezer \n"))
            break
        except ValueError:
            print("Zadejte prosím částku bez mezer")
    return amount


def get_file_path() -> str:
    """Show file dialog, ask user and return path of file to filter."""
    root = tk.Tk()
    root.withdraw()
    user_file_path = filedialog.askopenfilename()
    return user_file_path


def get_bank_name(bank_names: List[str]) -> str:
    """Return name of the bank.

    :param bank_names: list of bank names
    :return: Name of bank that user wants
    """
    print_numbered_list(bank_names)
    while True:
        try:
            bank_int = int(input("Jakou Banku chcete zpracovat? \n"
                                 "Zadejte prosím číslo bez mezer \n"))
            break
        except ValueError:
            print("Zadejte prosím číslo bez mezer")

    return bank_names[bank_int - 1]


def print_numbered_list(bank_names: List[str]):
    """Print numbered list of banks.

    :param bank_names: List of banks
    """
    for i in bank_names:
        print(bank_names.index(i) + 1, end=' ')
        print(" ", i)


def show_info(file_name: str, file_path: str):
    """Print info about created file.

    :param file_name: name of the file
    :param file_path: path to a file
    """
    print("\n Soubor byl vytvořen. Jmenuje se " + file_name
          + " a je ve složce \n"
          + file_path)
