# coding=utf-8
""" banks -- Prepare info about banks's csv and their identification

Each bank's info can be found in csv dict of this format: {bankName.member: CsvInfo}
Use bank_dict in format of {str: bankName.member} for access with human friendly string
"""

from typing import List, Dict


BANKS_INFO = {}  # type: Dict[str, CsvInfo]


def names() -> List[str]:
    """Return list of bank names which are also keys for csv_info."""
    return list(BANKS_INFO.keys())


class CsvInfo:
    """Provide info about given bank's csv files and it's identification name."""

    def __init__(self,
                 bank_name: str,
                 amount_column: str,
                 date_columns: List[int],
                 date_column: str,
                 date_format: str,
                 dayfirst: bool,
                 decimal: str,
                 default_columns: Dict[str, int],
                 default_filter_amount: float,
                 delimiter: str,
                 dtypes: Dict[str, object],
                 encoding: str,
                 file_name_partial: str,
                 header_row: int,
                 quotechar: str) -> None:
        """

        :param bank_name: Name of banks
        :param amount_column: Name the column with amount by which to filter
        :param date_columns: Columns containing date
        :param date_column: Name of column with date by which to filter
        :param date_format: Format of date in date_column
        :param dayfirst: DD/MM format dates, international and European format
        :param decimal: Character to recognize as decimal point (e.g. use ‘,’ for European data).
        :param default_columns: Default columns to show/save
        :param delimiter: Delimiter to use.
        :param dtypes: Dictionary with column names (string) and data types.
        Dtypes supported by pandas.
        :param file_name_partial: Part of the filename of the csv files of the given bank.
        :param header_row: Row number at which to find header row
        :param quotechar: The character used to denote the start and end of a quoted item.
        """
        self.bank_name = bank_name
        self.date_column = date_column
        self.date_columns = date_columns
        self.date_format = date_format
        self.dayfirst = dayfirst
        self.decimal = decimal
        self.default_columns = default_columns
        self.default_filter_amount = default_filter_amount
        self.delimiter = delimiter
        self.dtypes = dtypes
        self.encoding = encoding
        self.filter_str_pattern = file_name_partial
        self.header_row = header_row
        self.quotechar = quotechar
        self.amount_column = amount_column


def identify_bank(filepath: str) -> CsvInfo:
    """Identify bank name from filename and return it's CsvInfo.

    :param filepath: Path to file
    :return: CsvInfo
    """
    bank_csv_info = None
    for bank in BANKS_INFO.values():
        filter_string = bank.filter_str_pattern
        if filter_string in filepath:
            bank_csv_info = bank
            break

    return bank_csv_info


def create_cs_bank():
    """Create Ceska Sporitelna csv info."""
    dtypes = {"Předčíslí účtu plátce/příjemce": object,
              "Číslo účtu plátce/příjemce": object,
              "Kód banky plátce/příjemce": object,
              "Částka (transakce)": float,
              "Příchozí/odchozí(kreditní-debetní položka)": object,
              "Účetní/neúčetní položka": object,
              "Konstantní symbol": object,
              "Specifický symbol": object,
              "Popis transakce": object,
              "Název protiúčtu": object,
              "Bankovní reference": object,
              "Zpráva pro příjemce": object,
              "Zpráva pro plátce": object,

              "Variabilní symbol 1": object,
              "Variabilní symbol 2": object,
              "Reference platby": object,
              "Kurz měny obratu": object,
              "Kurz měny účtu": object,
              "Částka obratu ISO": object,

              "Zpráva pro příjemce 2": object,
              "Zpráva pro příjemce 3": object,
              "Zpráva pro příjemce 4": object,
              "Popis transakce 2": object,
              "Popis transakce 3": object,
              "Popis transakce 4": object,
              "SWIFT kód banky příjemce-OUT/banky plátce-INC NEBO název banky příjemce část": object,
              "Název banky příjemce část2": object,
              "Detail poplatku-část1": object,
              "Poplatek příjemce-pole 71F - OUT": object,
              "Poplatek zahr.banky - INC - část2": object,
              "Originální částka transakce-část1": object,
              "MT191 - Reference došlé MT103 část2": object,
              "Reference banky plátce-část1": object,
              "Obsah pole 77T - SEPA info1": object,
              "Obsah pole 77T - SEPA info2": object,
              "Obsah pole 77T - SEPA info3": object,
              "Popis typu poplatku CL": object,
              "Upřesnění poplatku CL část1": object,
              "Upřesnění poplatku CL část2": object,
              "Poznámka příkazce část1": object,
              "Poznámka příkazce část2": object,
              "Poznámka příkazce část3": object,
              "Poznámka příkazce část4": object}

    # date_columns_dtypes = {"Datum valuty": datetime,
    #                        "Datum zpracování": datetime,
    #                        "Odepsáno": datetime,
    #                        "Splatnost": datetime}

    # default_columns = {'date': 13,
    #                    'name': 9,
    #                    'var_symbol': 16,
    #                    'amount': 3},

    bank_name = "Česká spořitelna"
    bank = CsvInfo(bank_name=bank_name,
                   amount_column='Částka (transakce)',
                   date_columns=[13, 14, 21, 22],
                   date_column='Datum zpracování',
                   date_format='%Y/%m/%d',
                   dayfirst=False,
                   decimal=',',
                   dtypes=dtypes,
                   default_columns={"Datum zpracování": 14,
                                    "Název protiúčtu": 9,
                                    "Variabilní symbol 1": 15,
                                    "Částka (transakce)": 3},
                   default_filter_amount=10000.0,
                   delimiter=';',
                   encoding='windows-1250',
                   file_name_partial='TH',
                   header_row=10,
                   quotechar='"')

    BANKS_INFO.update({bank_name: bank})


# def create_sk_bank(bank_name):
#     columns = {'date': 0,
#                'name': 6,
#                'var_symbol': 13,
#                'amount': 7}
#
#     bank = Bank(bank_name=bank_name,
#                 newline=None,
#                 encoding='utf-8',
#                 delimiter=';',
#                 quotechar='"',
#                 date_format='%d.%m.%Y',
#                 file_name_partial='EXP_OBR',
#                 columns=columns)
#
#     banks.update({bank_name: bank})


def create_sk_bank():
    """Create Slovenska Sporitelna csv info."""
    dtypes = {'Dátum_valuty': object,
              'Predčíslo_účtu': object,
              'Číslo_účtu': object,
              'Predčíslo_protiúčtu': object,
              'Číslo_protiúčtu': object,
              'Kód_banky_protiúčtu': object,
              'Názov_protiúčtu': object,
              'Suma': float,
              'Mena': object,
              'Kurz': object,
              'Zostatok': float,
              'Popis_obratu': object,
              'E2E_reference': object,
              'Variabilný_symbol': object,
              'Konštantný_symbol': object,
              'Špecifický_symbol': object,
              'Poznámka': object,
              'Číslo_výpisu': object,
              'Identifikácia_protiúčtu1': object,
              'Identifikácia_protiúčtu2': object, 'Identifikácia_protiúčtu3': object,
              'Identifikácia_protiúčtu4': object, 'Správa_pre_prijímateľa1': object,
              'Správa_pre_prijímateľa2': object, 'Správa_pre_prijímateľa3': object,
              'Správa_pre_prijímateľa4': object}

    bank_name = "Slovenská spořitelna"
    bank = CsvInfo(bank_name=bank_name,
                   amount_column='Suma',
                   date_columns=[0],
                   date_column='Dátum_valuty',
                   date_format='%d.%m.%Y',
                   dayfirst=True,
                   decimal='.',
                   dtypes=dtypes,
                   default_columns={"Dátum_valuty": 0,
                                    "Názov_protiúčtu": 6,
                                    "Variabilný_symbol": 13,
                                    "Suma": 7},
                   delimiter=';',
                   default_filter_amount=3000.0,
                   encoding='utf-8',
                   file_name_partial='EXP_OBR',
                   header_row=0,
                   quotechar='"')

    BANKS_INFO.update({bank_name: bank})


create_cs_bank()
create_sk_bank()
