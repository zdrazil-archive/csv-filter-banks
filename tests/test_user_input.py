# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import mock
import datetime
from payments import user_input


def test_get_days():
    with mock.patch('builtins.input', return_value='5'):
        assert user_input.get_amount() == 5


def get_date_range():
    with mock.patch('builtins.input', return_value='30'):
        from_date = datetime.datetime.today() + datetime.timedelta(-int(30))
        to_date = datetime.datetime.today()
        assert user_input.get_amount() == (from_date, to_date)


def test_get_amount():
    with mock.patch('builtins.input', return_value='22.00'):
        assert user_input.get_amount() == 22.00


def test_get_bank_name():
    bank_names = ['Česká spořitelna', 'Slovenská spořitelna']
    with mock.patch('builtins.input', return_value='2'):
        assert user_input.get_bank_name(bank_names) == 'Slovenská spořitelna'


def test_print_numbered_list(capfd):
    bank_names = ['Česká spořitelna', 'Slovenská spořitelna']
    user_input.print_numbered_list(bank_names)
    expected_result = "1   Česká spořitelna\n2   Slovenská spořitelna\n"
    out, error = capfd.readouterr()
    assert out == expected_result


def test_show_info(capfd):
    file_name = "abc.txt"
    file_path = "/Users/johnny/Desktop/"
    expected_result = "\n Soubor byl vytvořen. Jmenuje se " + file_name + " a je ve složce \n" + file_path + "\n"
    user_input.show_info(file_name, file_path)
    out, error = capfd.readouterr()
    assert out == expected_result
