from my_parser_csv import *
import locale
import datetime

def test_format_amount():
    locale.setlocale(locale.LC_ALL, 'cs_CZ')
    formatted_amount = '225 500,50'
    tested_amount = locale.format("%.2f", float(225500.50), grouping=True)
    assert formatted_amount == tested_amount


