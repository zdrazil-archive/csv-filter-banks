import parser


def get_payments():
    csv_reader = parser.get_csv_reader('utf-8', ';', '"')
    columns = {'date': 0,
               'name': 6,
               'var_symbol': 13,
               'amount': 7}
    payments = parser.get_payments(columns, csv_reader, '%d.%m.%Y')
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
create_file(formatted_payments, 'PLATBY-SK.txt')
