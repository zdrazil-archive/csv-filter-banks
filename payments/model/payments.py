# coding=utf-8
""" payments -- info about and manipulation of DataFrame with payments"""
import datetime

import pandas

from payments.model import my_io


def get_payments_data_frame(csv_filepath: str) -> pandas.DataFrame:
    """Return DataFrame given path to csv file.

    :param csv_filepath: Path to csv file
    """
    return my_io.get_data_frame(csv_filepath)


def filter_by_date(data_frame: pandas.DataFrame,
                   date_range: (datetime, datetime),
                   date_column: str) -> pandas.DataFrame:
    """Return DataFrame filtered by date.

    :param data_frame: DataFrame to filter
    :param date_range: Tuple with datetime objects (from_date, to_date)
    :param date_column: Name of column with date by which to filter
    """
    return data_frame[(data_frame[date_column] >= date_range[0]) & (data_frame[date_column] <= date_range[1])]


def filter_by_amount(data_frame: pandas.DataFrame,
                     filter_amount: float,
                     amount_column: str) -> pandas.DataFrame:
    """Return DataFrame filtered by amount.

    :param data_frame: DataFrame to filter
    :param filter_amount: Amount by which to filter
    :param amount_column: Name of column with amount by which to filter
    """
    try:
        float(filter_amount)
    except ValueError:
        return data_frame
    else:
        return data_frame[(data_frame[amount_column] >= float(filter_amount))]
