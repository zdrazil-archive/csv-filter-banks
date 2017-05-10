# coding=utf-8
""" my_io -- File and path manipulation"""
import datetime
import os
import glob
from typing import List

import pandas as pd

from payments.model import banks, formatters


def write_file_from_data_frame(data_frame: pd.DataFrame,
                               columns: List[str],
                               date_column_name: str,
                               final_path: str) -> str:
    """Save data frame with specified columns to a given path.

    :param data_frame: data to save
    :param columns: columns to save
    :param date_column_name: name of the date column for formatting
    :param final_path: a normalized absolutized version of the pathname path
    :return: path of output file
    """
    remove_file(final_path)

    with open(final_path, 'w') as outfile:
        text_file_from_data_frame(data_frame, columns, date_column_name, outfile)

    return os.path.abspath(final_path)


def text_file_from_data_frame(data_frame: pd.DataFrame,
                              columns: List[str],
                              date_column_name: str,
                              output_file=None) -> str:
    """Return string from DataFrame and if given output also to given file.

    :param data_frame: DataFrame to convert
    :param columns: Columns to use
    :param date_column_name: Column containing date
    :param output_file: Filepath to output to
    """
    output_string = "Nic nenalezeno."
    if data_frame is not None:
        output_string = data_frame.to_string(buf=output_file,
                                             header=True,
                                             index=False,
                                             columns=columns,
                                             float_format=formatters.format_amount,
                                             formatters={date_column_name: formatters.format_date})
    return output_string


def remove_file(file_path: str):
    """Remove file at a given path.

    :param file_path: path of the file
    """
    try:
        os.remove(file_path)
    except OSError:
        pass


def get_data_frame(filepath: str) -> pd.DataFrame:
    """Return DataFrame loaded from csv.

    :param filepath: path to csv file
    :return: Pandas DataFrame
    """
    csv_info = banks.identify_bank(filepath)

    data_frame = None
    if csv_info:
        data_frame = pd.read_csv(filepath_or_buffer=filepath,
                                 delimiter=csv_info.delimiter,
                                 header=csv_info.header_row,
                                 index_col=False,
                                 encoding=csv_info.encoding,
                                 quotechar=csv_info.quotechar,
                                 decimal=csv_info.decimal,
                                 skip_blank_lines=False,
                                 dtype=csv_info.dtypes,
                                 parse_dates=csv_info.date_columns,
                                 infer_datetime_format=True,
                                 dayfirst=csv_info.dayfirst)
    return data_frame


LOCATIONS = {'downloads': "~/Downloads/",
             'desktop': "~/Desktop/"}


def get_full_path(file_name: str, file_path: str) -> str:
    """Return absolute path of a given file.

    :param file_name: filename
    :param file_path: path to filename from Locations enum
    """
    return os.path.expanduser(file_path + file_name)


def get_file_list(bank_name, filepath: str) -> List[str]:
    """Return bank files at given path.

    :param filepath: path from which to load files
    :return: list of absolute pathnames of bank files
    """
    os.chdir(os.path.expanduser(filepath))
    string_pattern = banks.BANKS_INFO[bank_name].filter_str_pattern

    file_list = [file for file in glob.glob(string_pattern + "*.csv")]
    return file_list


def days_to_date_range(days: int) -> (datetime, datetime):
    """Return date range of last user specified days.

    :return: Tuple in the format of (datetime_from, datetime_to)
    """
    try:
        int(days)
    except ValueError:
        raise
    else:
        from_date = datetime.datetime.today() + datetime.timedelta(-int(days))
    to_date = datetime.datetime.today()
    return from_date.date(), to_date.date()
