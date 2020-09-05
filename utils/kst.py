import datetime


KST = datetime.timezone(datetime.timedelta(hours=9))


def korean_date():
    return datetime.datetime.now(tz=KST)
