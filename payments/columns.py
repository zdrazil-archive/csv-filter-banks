# coding=utf-8
""" columns -- Information about and manipulation of columns."""
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from payments.payments_table import PaymentsTable


class Columns:
    """Information about and manipulation of columns."""
    all = None
    selected_val = None
    selected_num = None
    default = None
    bank_name = None

    def update(self, payments_table: 'PaymentsTable'):
        """Update columns with data from PaymentsTable.

        :param payments_table: PaymentsTable
        """
        if self.bank_name != payments_table.bank_name:
            self.all = default_columns_first(payments_table)
            self.default = payments_table.csv_info.default_columns.keys()
            self.selected_val = self.default
            self.selected_num = (0, 1, 2, 3)
            self.bank_name = payments_table.bank_name

    def reset(self):
        """Reset selected columns to default."""
        self.selected_val = self.default
        self.selected_num = (0, 1, 2, 3)


def default_columns_first(payments_table: 'PaymentsTable') -> List[str]:
    """Return list of columns with bank default columns placed first.

    :param payments_table: PaymentsTable with CsvInfo
    """
    final_columns = []

    all_columns = list(payments_table.data_frame)
    for column in payments_table.csv_info.default_columns:
        try:
            default_column_index = all_columns.index(column)
        except ValueError:
            pass
        else:
            all_columns.pop(default_column_index)
        final_columns = list(payments_table.csv_info.default_columns) + all_columns
    return final_columns
