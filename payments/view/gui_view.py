# coding=utf-8
""" gui_view -- Create and layout widgets"""
import tkinter as tk
from tkinter import ttk, N, S, E, W

from typing import List, Tuple


class FilterWindow:
    """Configure filter window."""

    def __init__(self):
        """Configure filter window."""
        self.root = tk.Tk()
        self.root.title("Platby")
        self.content = ttk.Frame(self.root, padding=(12, 12, 12, 12))
        self.frame = ttk.Frame(self.content, borderwidth=5, relief="sunken", width=200, height=100)
        self.content.grid(column=0, row=0, sticky=(N, S, E, W))

        # Set window size
        screen_height = self.root.winfo_screenheight()  # height of the screen
        width = 800  # width for the Tk root
        height = 800  # height for the Tk root
        if screen_height < 800:
            height = screen_height - 100
        self.root.geometry(str(width) + "x" + str(height))

        # Set resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)
        self.content.columnconfigure(2, weight=1)
        self.content.columnconfigure(4, weight=1)
        self.content.rowconfigure(1, pad=5)
        self.content.rowconfigure(3, pad=5)
        self.content.rowconfigure(5, pad=5)
        self.content.rowconfigure(7, pad=10)
        self.content.rowconfigure(8, weight=2)

        self.widgets = Widgets(self.content)


class Widgets:
    """Widgets to add."""

    def __init__(self, master: ttk.Frame):
        self.bank_list = BankList(master)
        self.file_list = FileList(master)
        self.selected_file_label = SelectedFileLabel(master)

        self.column_list = ColumnList(master)
        self.days_back = DaysBack(master)
        self.amount_from = AmountFrom(master)

        self.copy_clipboard_button = CopyClipboardButton(master)
        self.default_columns_button = DefaultColumnsButton(master)
        self.filter_button = FilterButton(master)

        self.save_button = SaveButton(master)
        self.payments_table = PaymentsTable(master)


# Create widgets
class BankList:
    """Configure bank list."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Vybraná banka:")
        self.listbox = tk.Listbox(master, height=10, exportselection=0)
        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set

        self.description.grid(column=0, row=0, sticky=(N, W), pady=5)
        self.listbox.grid(column=0, row=1, sticky=(N, W, E, S))
        self.scrollbar.grid(column=1, row=1, sticky=(N, S, W))

        self.contentVar = tk.Variable()
        self.listbox["listvariable"] = self.contentVar

    def update(self, banklist: List[str]):
        """Update banks in banklist with new ones.

        :param banklist: List of bank names to show
        """
        self.contentVar.set(banklist)
        self.listbox.selection_set(0)

    def select(self, bank_name: str):
        """Select bank in bank list.

        :param bank_name: Name of bank
        """
        for i, value in enumerate(get_listbox_selected_values(self.listbox)):
            if bank_name == value:
                self.listbox.selection_clear(0, "end")
                self.listbox.selection_set(i)
                break

    def get_selected(self) -> str:
        """Return bank name."""
        bank_name = None
        try:
            bank_name = get_listbox_selected_values(self.listbox)[0]
            # bank_name = self.listbox.get(self.listbox.curselection()[0])
        except IndexError:
            pass
        return bank_name


class FilePicker:
    """Configure file picker."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Vybrat soubor")
        self.button = ttk.Button(master, text="Vybrat soubor....")
        self.button.state(["disabled"])


class FileList:
    """Configure filelist."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Soubory")
        self.listbox = tk.Listbox(master, height=10, width=35, exportselection=0)
        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set

        self.description.grid(column=2, row=0, columnspan=2, sticky=(N, W), pady=5)
        self.listbox.grid(column=2, row=1, columnspan=2, sticky=(N, W, E, S))
        self.scrollbar.grid(column=3, row=1, sticky=(N, S, E))

        self.contentVar = tk.Variable()
        self.listbox["listvariable"] = self.contentVar

    def update(self, filelist: List[str]):
        """Insert list of filenames to filelist.

        Select last one after update
        :param filelist: list of files to show
        """
        self.contentVar.set(filelist)

        # if len
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set("end")
        self.listbox.see("end")

    def selected(self) -> str:
        """Return selected filename."""
        try:
            selected = get_listbox_selected_values(self.listbox)[0]
            return selected
        except IndexError:
            raise

    def update_selected_file_label(self):
        """Update selected file label from selected file in filelist."""
        try:
            self.contentVar.set((get_listbox_selected_values(self.listbox[0])))
        except IndexError:
            raise


class SelectedFileLabel:
    """Configure selected file label."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Vybraný soubor:")
        self.label = ttk.Label(master)

        self.description.grid(column=0, row=2, sticky=(N, W), pady=5)
        self.label.grid(column=0, row=3, sticky=(N, W), padx=5)

        self.contentVar = tk.StringVar()
        self.label["textvariable"] = self.contentVar


class ColumnList:
    """Configure selected column list."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Vybrané sloupce:")
        self.listbox = tk.Listbox(master,
                                  height=10,
                                  width=35,
                                  selectmode=tk.MULTIPLE,
                                  exportselection=0)
        self.scrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox['yscrollcommand'] = self.scrollbar.set

        self.description.grid(column=2, row=2, sticky=(N, W), pady=5)
        self.listbox.grid(column=2, row=3, columnspan=2, sticky=(N, W, E, S))
        self.scrollbar.grid(column=4, row=3, columnspan=2, sticky=(N, S, W))

        self.contentVar = tk.Variable()
        self.listbox["listvariable"] = self.contentVar

    def update(self, column_list: List[str]):
        """Insert list to column list.

        :param column_list: list of column names
        """
        self.contentVar.set(column_list)

    def select(self, column_nums: Tuple):
        """Select column numbers in column list.

        :param column_nums: int numbers of columns to select
        """
        for column_num in column_nums:
            self.listbox.selection_set(column_num)

    def reset(self):
        """Clear column selections."""
        self.listbox.selection_clear(0, "end")

    def selected(self) -> List[str]:
        """Return list of selected columns."""
        return get_listbox_selected_values(self.listbox)

    def indexes(self) -> List[int]:
        """Return indexes of selected columns."""
        return self.listbox.curselection()


class DaysBack:
    """Configure days back spinbox."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Dnů zpátky:")
        self.spinbox = tk.Spinbox(master, from_=1.0, to=tk.sys.maxsize)

        self.description.grid(column=0, row=4, sticky=(N, W), padx=5)
        self.spinbox.grid(column=0, row=5, sticky=(N, W), padx=5)

        self.contentVar = tk.StringVar()
        self.spinbox["textvariable"] = self.contentVar


class AmountFrom:
    """Configure amount entry."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.description = ttk.Label(master, text="Částka nad:")
        self.spinbox = tk.Spinbox(master, from_=1.0, to=tk.sys.float_info.max, increment=500.0)

        self.description.grid(column=0, row=6, sticky=(N, W), padx=5)
        self.spinbox.grid(column=0, row=7, sticky=(N, W), padx=5)

        self.contentVar = tk.StringVar()
        self.spinbox["textvariable"] = self.contentVar


class CopyClipboardButton:
    """Configure copy clipboard button."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.button = ttk.Button(master, text="Kopírovat")
        self.button.grid(column=3, row=6, sticky=(N, S, W))


class DefaultColumnsButton:
    """Configure default column button."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.button = ttk.Button(master, text="Původní sloupce")
        self.button.grid(column=4, row=6, sticky=(N, S, E, W), padx=5)


class FilterButton:
    """Configure filter button."""

    def __init__(self, master: ttk.Frame):
        self.button = ttk.Button(master, text="Filtrovat")
        self.button.grid(column=2, row=5, rowspan=2, sticky=(N, W, S))


class SaveButton:
    """Configure save button."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.button = ttk.Button(master, text="Uložit")
        self.button.grid(column=3, row=5, sticky=(N, S, W), padx=5)


class PaymentsTable:
    """Configure payments table."""

    def __init__(self, master: ttk.Frame):
        """
        :param master: parent master to construct with.
        """
        self.content = tk.Text(master, height=30, wrap="none")
        self.vscrollbar = ttk.Scrollbar(master, orient=tk.VERTICAL, command=self.content.yview)
        self.content['yscrollcommand'] = self.vscrollbar.set
        self.hscrollbar = ttk.Scrollbar(master, orient=tk.HORIZONTAL, command=self.content.xview)
        self.content['xscrollcommand'] = self.hscrollbar.set

        self.content.grid(column=0, row=8, columnspan=5, rowspan=1, sticky=(N, W, S, E))
        self.vscrollbar.grid(column=5, row=8, sticky=(N, S, W))
        self.hscrollbar.grid(column=0, row=9, columnspan=5, sticky=(N, S, W, E), padx=5)

    def update(self, output_string: str):
        """Reset and add string to table.

        :param output_string: String to show in table
        """
        self.content.delete('1.0', tk.END)
        self.content.insert('1.0', output_string)

    def table_string(self) -> str:
        """Return table content as string."""
        return self.content.get('1.0', tk.END)


# Helper functions
def get_listbox_selected_values(widget: tk.Listbox) -> List[str]:
    """Return values of selections in Listbox.

    :param widget: Listbox to process
    """
    selections = widget.curselection()
    values = []
    for i, __ in enumerate(selections):
        value = widget.get(selections[i])
        values.append(value)
    return values
