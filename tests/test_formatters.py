# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from payments.model import formatters


def test_format_date():
    date = datetime.datetime(2016, 7, 2, 5, 3, 2)
    formatted_date = formatters.format_date(date)
    assert formatted_date == '02.07.2016'


def test_format_amount():
    amount = '2500000.20'
    custom_locale = 'cs_CZ'
    formatted_amount = formatters.format_amount(amount, custom_locale)
    print(type(formatted_amount))
    assert formatted_amount == "2 500 000,20"


def test_date_from_string():
    date_string = "2015/12/11"
    date_format = '%Y/%m/%d'
    result = formatters.date_from_string(date_string, date_format)
    assert result == datetime.datetime(2015, 12, 11)
