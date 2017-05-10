# coding=utf-8
""" gui_controller -- Show and manipulate GUI for payment filtering"""

from payments.model import banks, my_io
from payments.view import gui_view as gv
from payments.columns import Columns
from payments.payments_table import PaymentsTable

INPUTPATH = "~/Downloads/"


class FilterController:
    """Manipulation between data file and view."""
    filter_window = gv.FilterWindow()
    widgets = filter_window.widgets

    # Widgets
    tk_amount_from = widgets.amount_from
    tk_bank_list = widgets.bank_list
    tk_days_back = widgets.days_back

    tk_default_columns_button = widgets.default_columns_button
    tk_columnlist = widgets.column_list
    tk_copy_clipboard_button = widgets.copy_clipboard_button

    tk_file_list = widgets.file_list
    tk_filter_button = widgets.filter_button
    tk_payments_table_widget = widgets.payments_table

    tk_save_button = widgets.save_button
    tk_selected_file_label = widgets.selected_file_label

    payments_table = None
    columns = Columns()

    def __init__(self):
        """Prepare for window presentation."""
        self.on_load()

    def on_load(self):
        """Prepare and present window."""
        self.tk_amount_from.contentVar.set(10000)
        self.tk_days_back.contentVar.set(3)

        self.bind_events()
        self.add_default_banks_to_banklist()
        self.onselect_banklist()

        self.tk_days_back.spinbox.focus()
        self.filter_window.root.mainloop()

    # Commands
    # Bank list
    def onselect_banklist(self, event=None):
        """Action when bank clicked."""
        self.update_on_bank_change()

    def add_default_banks_to_banklist(self):
        """Add banks to bank list."""
        self.tk_bank_list.update(banks.names())

    def update_on_bank_change(self):
        """Update all that is necessary when selected bank is changed."""
        selected_bank = self.tk_bank_list.get_selected()

        self.tk_file_list.update(my_io.get_file_list(selected_bank, INPUTPATH))
        self.onselect_filelist()

    # Table
    def filter_table(self):
        """Filter table by amount and date and present the result."""
        selected_amount = self.tk_amount_from.contentVar.get()
        selected_days = self.tk_days_back.contentVar.get()
        output_string = self.payments_table.filter_table(selected_amount,
                                                         selected_days,
                                                         self.columns)
        self.tk_payments_table_widget.update(output_string)

    # Filelist
    def onselect_filelist(self, event=None):
        """Action when file in filelist clicked."""
        self.tk_selected_file_label.contentVar.set(self.tk_file_list.selected())

        selected_bank = self.tk_bank_list.get_selected()
        selected_file = self.tk_file_list.selected()
        self.payments_table = PaymentsTable(selected_bank, selected_file, INPUTPATH)

        self.columns.update(self.payments_table)

        self.reset_columns()
        self.tk_columnlist.update(self.columns.all)
        self.tk_columnlist.select(self.columns.selected_num)

        self.onselect_columnlist()

        self.filter_table()

    # Column list
    def onselect_columnlist(self, event=None):
        """Action when column in columnlist clicked."""
        self.columns.selected_val = self.tk_columnlist.selected()
        self.columns.selected_num = self.tk_columnlist.indexes()
        self.filter_table()

    def reset_columns(self):
        """Reset columns to default selections."""
        self.columns.reset()
        self.tk_columnlist.reset()
        self.tk_columnlist.select(self.columns.selected_num)
        self.filter_table()

    # Days back and amount
    def on_days_back_change(self, *_):
        """Action when days back is changed."""
        self.filter_table()

    def on_amount_change(self, *_):
        """Action when amount is changed."""
        self.filter_table()

    def on_save_button(self, *_):
        """Action when save button is clicked."""
        self.payments_table.to_file(self.columns)

    def on_filter_button(self, *_):
        """Action when filter button is clicked."""
        self.filter_table()

    def on_save_to_clipboard(self):
        """Save content of table to clipboard. Clear previous content of clipboard."""
        output_string = self.tk_payments_table_widget.table_string()
        self.filter_window.root.clipboard_clear()
        self.filter_window.root.clipboard_append(output_string)

    # Event
    def bind_events(self):
        """ Bind functions to tkinter widgets."""
        self.tk_file_list.listbox.bind('<<ListboxSelect>>', self.onselect_filelist)
        self.tk_bank_list.listbox.bind('<<ListboxSelect>>', self.onselect_banklist)
        self.tk_columnlist.listbox.bind('<<ListboxSelect>>', self.onselect_columnlist)

        self.tk_filter_button.button["command"] = self.on_filter_button
        self.tk_save_button.button["command"] = self.on_save_button
        self.tk_default_columns_button.button["command"] = self.reset_columns
        self.tk_copy_clipboard_button.button["command"] = self.on_save_to_clipboard

        self.filter_window.root.bind('<Return>', self.on_filter_button)

        self.tk_days_back.contentVar.trace('w', self.on_days_back_change)
        self.tk_amount_from.contentVar.trace('w', self.on_amount_change)


FilterController()
