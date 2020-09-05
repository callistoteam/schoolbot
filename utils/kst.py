import datetime


KST = datetime.timezone(datetime.timedelta(hours=9))


def kst_sft():
    return datetime.datetime.now(tz=KST)
