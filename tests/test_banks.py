# coding=utf-8
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from payments.model import banks


def test_identify_cs_bank():
    path = "/Users/johnny/Downloads/EXP_OBR_04.04.2017_07-31-00.csv"
    assert banks.identify_bank(path).bank_name == "Slovenská spořitelna"


def test_identify_sk_bank():
    path = "/Users/johnny/Downloads/EXP_OBR_04.04.2017_07-31-00.csv"
    assert banks.identify_bank(path).bank_name == "Slovenská spořitelna"


def test_create_cs_bank():
    banks.create_cs_bank()
    bank_name = "Česká spořitelna"
    assert banks.BANKS_INFO[bank_name]


def test_names():
    banks.create_cs_bank()
    banks.create_sk_bank()
    bank_name = "Česká spořitelna"
    assert bank_name in banks.names()
