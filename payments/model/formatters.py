# coding=utf-8
""" Helper methods for manipulating values from csv files"""
import datetime
import locale


def format_date(date: datetime) -> str:
    """Return formatted date.

    :param date: datetime object
    """
    # return (date.strftime('%d.%m.%Y')).strip()
    return date.strftime('%d.%m.%Y')


def format_amount(amount_string: str,
                  custom_locale: str = '') -> str:
    """Return formatted amount.

    :param amount_string: float amount string
    :param custom_locale: string representing locale to set.
    """
    locale.setlocale(locale.LC_ALL, custom_locale)
    return locale.format("%.2f", float(amount_string), grouping=True)


def date_from_string(date_string: str, date_format: str) -> datetime:
    """Return date string as datetime object.

    :param date_string: string with date to parse
    :param date_format: date_string format following strptime(format)
                        directives
    """
    try:
        date = datetime.datetime.strptime(date_string, date_format)
    except ValueError:
        raise
    return date
