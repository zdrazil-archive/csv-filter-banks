import parser


def get_payments():
    csv_reader = parser.get_csv_reader('windows-1250', ';', '"')
    columns = {'date': 13,
               'name': 9,
               'var_symbol': 16,
               'amount': 3}
    payments = parser.get_payments(columns, csv_reader, '%Y/%m/%d')
    for payment in payments:
        payment['amount'] = float(payment['amount'].replace(',', '.'))
    filtered_payments = parser.filter_payments(payments)

    return filtered_payments


def format_payments(payments):
    for payment in payments:
        payment['date'] = parser.format_date(payment['date'])
        payment['amount'] = parser.format_amount(payment['amount'])
    return payments


def create_file(payments, final_file):
    parser.create_final_file(payments, final_file)


payments = get_payments()
formatted_payments = format_payments(payments)
create_file(formatted_payments, 'PLATBY-CZ.txt')
