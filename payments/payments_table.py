# coding=utf-8
""" payments_table -- Representation of data file."""
import pandas

from payments.model import banks, my_io, payments
from payments.columns import Columns

OUTPUTPATH = "~/Desktop/"


class PaymentsTable:
    """Representation and manipulation of data source."""

    def __init__(self, bank_name: str, filename: str, filepath: str):
        """

        :param bank_name: Name of bank
        :param filename: Filename
        :param filepath: Path to file without filename
        """
        self.csv_info = get_csv_info(bank_name)
        self.data_frame = get_data_frame(filename, filepath)
        self.bank_name = bank_name

        self.filtered_data_frame = None

    def filter_table(self, amount: float, days: int, columns: Columns) -> str:
        """Filter table by amount and date and return the result.

        :param amount: Lowest amount to show
        :param days: Number of days back to show
        :param columns: Columns to show
        :return:
        """
        by_amount = payments.filter_by_amount(self.data_frame,
                                              amount,
                                              self.csv_info.amount_column)

        date_range = my_io.days_to_date_range(days)

        by_date = payments.filter_by_date(by_amount,
                                          date_range,
                                          self.csv_info.date_column)

        output_string = self.to_string(by_date, columns)

        return output_string

    def to_file(self, columns: Columns):
        """Save table to file.

        :param columns: Columns with data about selected columns
        """
        output_string = self.to_string(self.data_frame, columns)
        final_file = "PLATBY_" + self.bank_name + ".txt"
        full_path = my_io.get_full_path(final_file, OUTPUTPATH)
        with open(full_path, 'w') as outfile:
            outfile.write(output_string)

    def to_string(self, custom_data_frame, columns: Columns) -> str:
        """Return string representing DataFrame.

        :param custom_data_frame: DataFrame to convert to string
        :param columns: Columns with selected columns
        """
        selected_columns = columns.selected_val
        output_string = "Nic nenalezeno."
        if self.csv_info:
            output_string = my_io.text_file_from_data_frame(custom_data_frame,
                                                            selected_columns,
                                                            self.csv_info.date_column)
        return output_string


def get_data_frame(filename: str, filepath: str) -> pandas.DataFrame:
    """Return DataFrame of selected file.

    :param filename: Filename
    :param filepath: Path to file without filename
    :return:
    """
    full_path = my_io.get_full_path(filename, filepath)
    return my_io.get_data_frame(full_path)


def get_csv_info(bank_name: str) -> banks.CsvInfo:
    """Return CsvInfo of selected bank.

    :param bank_name: Name of bank
    """
    try:
        bank_csv_info = banks.BANKS_INFO[bank_name]
        return bank_csv_info
    except KeyError:
        raise
