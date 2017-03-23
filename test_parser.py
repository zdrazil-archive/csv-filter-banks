from parser import *
import datetime

def test_get_date_range():
    
    from_date = datetime.datetime.now() + datetime.timedelta(-int(20))
    to_date = datetime.datetime.now
    assert get_date_range(20) == (from_date,to_date)
