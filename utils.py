from datetime import datetime

def days_between(d1, d2):
    d1 = datetime(2000, d1.month, d1.day)
    d2 = datetime(2000, d2.month, d2.day)
    delta = abs((d1 - d2).days)
    return min(delta, 365 - delta)

def is_within_buffer(glaze_date, birthday, buffer_days):
    year = glaze_date.year
    bday_this_year = datetime(year, birthday[0], birthday[1])
    delta = abs((glaze_date - bday_this_year).days)
    if delta > 182:
        bday_next = datetime(year + 1, birthday[0], birthday[1])
        bday_prev = datetime(year - 1, birthday[0], birthday[1])
        delta = min(abs((glaze_date - bday_next).days), abs((glaze_date - bday_prev).days))
    return delta <= buffer_days
