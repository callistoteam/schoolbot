import datetime
import re

KST = datetime.timezone(datetime.timedelta(hours=9))

def format_date(argument):
    current_date = datetime.datetime.now(tz=KST)
    if not argument:
        date = ( current_date.year, current_date.month, current_date.day )
    else: 
        date = re.match(r'^(?:(?P<YY>\d{4}|\d{2})[| ])?(?P<MM>\d{2})[| ](?P<DD>\d{2})|$', argument) or re.match(r'^(?:(?P<YY>\d{4}|\d{2})년[| ])?(?P<MM>\d{1,2})월[| ](?P<DD>\d{1,2})일$', argument)
    
    if not date:
        return None

    date = date.groups()
    return f"{current_date.year if not date[0] else date[0]}{'0' + date[1] if len(date[1]) == 1 else date[1]}{'0' + date[2] if len(date[2]) == 1 else date[2]}"