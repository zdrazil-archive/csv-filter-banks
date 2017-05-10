# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import datetime
from payments.model import my_io


def test_get_full_path(monkeypatch):
    def mockreturn(path):
        return '/Users/johnny/Downloads/abc.txt'

    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    expected_result = "/Users/johnny/Downloads/abc.txt"
    file_name = "foo"
    file_path = "foo"

    assert my_io.get_full_path(file_name, file_path) == expected_result


def test_days_to_date_range():
    from_date = datetime.datetime.today() + datetime.timedelta(-int(30))
    to_date = datetime.datetime.today()
    assert my_io.days_to_date_range(30) == (from_date.date(), to_date.date())
