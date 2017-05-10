# coding=utf-8
""" controller_cli -- Commandline interface for payment filtering."""
from payments import user_input
from payments.model import banks, my_io, payments
import pandas

# Prepare data
BANK_NAME = user_input.get_bank_name(banks.names())
CSV_INFO = banks.BANKS_INFO[BANK_NAME]


# Filter
def filter_data() -> pandas.DataFrame:
    """Filter data given input."""
    amount = user_input.get_amount()
    date_range = user_input.get_date_range()
    filepath = user_input.get_file_path()

    data_frame = my_io.get_data_frame(filepath)

    by_amount = payments.filter_by_amount(data_frame,
                                          amount,
                                          CSV_INFO.amount_column)
    by_date = payments.filter_by_date(by_amount,
                                      date_range,
                                      CSV_INFO.date_column)
    return by_date


# Save
def save_data():
    """Save filtered data to text file."""
    final_file = "PLATBY_" + BANK_NAME + ".txt"
    location = '~/Desktop/'
    full_path = my_io.get_full_path(file_name=final_file, file_path=location)

    data_frame = filter_data()
    my_io.write_file_from_data_frame(data_frame=data_frame,
                                     columns=CSV_INFO.default_columns,
                                     date_column_name=CSV_INFO.date_column,
                                     final_path=full_path)

    present_info(data_frame, final_file, full_path)


# Present
def present_info(data_frame: pandas.DataFrame, final_file: str, location: str):
    """Show info to user.

    :param data_frame: DataFrame that was saved.
    :param final_file: Name of saved file.
    :param location: Location of saved file.
    """
    user_input.show_info(final_file, location)


save_data()
