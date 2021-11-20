import requests
import datetime

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo


BASE_URL = "https://www.cezdistribuce.cz/distHdo/adam/containers/"
CEZ_TIMEZONE = ZoneInfo("Europe/Prague")


def getCorrectRegionName(region: str):
    """
    Sanitize and validate region name variable.

    :param region: a string with a name of distribution region
    :return: string
    """
    region = region.lower()
    valid_regions = ["zapad", "sever", "stred", "vychod", "morava"]
    if region in valid_regions:
        return region
    else:
        raise KeyError(f"Region {region} is not valid region.")


def getRequestUrl(region: str, code: str):
    """
    Compose request URI

    :param region: a string with a name of distribution region
    :param code: a string with
    :return: string
    """
    region = getCorrectRegionName(region)
    url = BASE_URL + region + "?&code=" + code.upper()
    return url


def timeInRange(start: datetime, end: datetime, x: datetime):
    """
    :param start: datetime
    :param end: datetime
    :param x: datetime
    :return: bool
    """
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def parseTime(time_str: str):
    """
    Parse time from %H:%M string format into time object

    :param time_str: a string in %H:%M format
    :return: datetime
    """
    if not time_str:
        return datetime.time(0, 0)
    else:
        return datetime.datetime.strptime(time_str, "%H:%M").time()


def parseDate(date_time_str):
    """
    :param date_time_str:
    :return: datetime
    """
    return datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")


def isHdo(jsonCalendar, daytime=datetime.datetime.utcnow()):
    """
    Find out if the HDO is enabled for the current timestamp

    :param jsonCalendar: JSON with calendar schedule from CEZ
    :param daytime: relevant time in UTC to check if HDO is on or not
    :return: bool
    """
    # convert daytime to timezone CEZ is using on website
    daytime.replace(tzinfo=ZoneInfo("UTC"))
    daytime = daytime.astimezone(CEZ_TIMEZONE)
    daytime.replace(tzinfo=None)

    # select Mon-Fri schedule or Sat-Sun schedule according to current date
    if daytime.weekday() < 5:
        dayCalendar = jsonCalendar[0]
    else:
        dayCalendar = jsonCalendar[1]

    checkedTime = daytime.time()
    hdo = False

    # iterate over scheduled times in calendar schedule
    for i in range(1, 11):
        startTime = parseTime(dayCalendar["CAS_ZAP_" + str(i)])
        endTime = parseTime(dayCalendar["CAS_VYP_" + str(i)])
        hdo = hdo or timeInRange(start=startTime, end=endTime, x=checkedTime)
    return hdo
