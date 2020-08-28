import datetime


def korean_date():
    KST = datetime.timezone(datetime.timedelta(hours=9))
    return datetime.datetime.now(tz=KST)


def kst_sft():
    return korean_date().strftime("%Y-%m-%d %H:%M:%S (%Z)")
