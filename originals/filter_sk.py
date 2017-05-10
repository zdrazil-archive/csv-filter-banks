import my_parser_csv


def get_payments():
    csv_reader = my_parser_csv.get_csv_reader('utf-8', ';', '"')
    columns = {'date': 0,
               'name': 6,
               'var_symbol': 13,
               'amount': 7}
    payments = my_parser_csv.get_payments(columns, csv_reader, '%d.%m.%Y')
    filtered_payments = my_parser_csv.filter_payments(payments)

    return filtered_payments


def format_payments(payments):
    for payment in payments:
        payment['date'] = my_parser_csv.format_date(payment['date'])
        payment['amount'] = my_parser_csv.format_amount(payment['amount'])
    return payments


def create_file(payments, final_file):
    my_parser_csv.create_final_file(payments, final_file)


payments = get_payments()
formatted_payments = format_payments(payments)
create_file(formatted_payments, 'PLATBY-SK.txt')
