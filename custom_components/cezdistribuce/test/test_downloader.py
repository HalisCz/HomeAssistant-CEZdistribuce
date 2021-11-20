import pytest
import datetime
import json
import requests
from urllib.parse import urlparse
from unittest.mock import MagicMock
from cezdistribuce import downloader

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo


@pytest.mark.parametrize("region", ("zapad", "zAPAD", "zapaD", "ZAPAD"))
def test_getCorrectRegionName(region):
    assert downloader.getCorrectRegionName(region) == "zapad"


@pytest.mark.parametrize("region", ("brno", "slezsko", "moon"))
def test_getIncorrectRegionName(region):
    with pytest.raises(KeyError):
        downloader.getCorrectRegionName(region)


@pytest.mark.parametrize(
    "region, code, result",
    [
        (
            "zapad",
            "some",
            "https://www.cezdistribuce.cz/distHdo/adam/containers/zapad?&code=SOME",
        ),
        (
            "stred",
            "a1b3dp6",
            "https://www.cezdistribuce.cz/distHdo/adam/containers/stred?&code=A1B3DP6",
        ),
    ],
)
def test_getRequestUrl(region, code, result):
    # check for expected result
    assert downloader.getRequestUrl(region, code) == result

    # check if query part is in the correct format
    assert (
        urlparse(downloader.getRequestUrl(region, code)).query
        == f"&code={code.upper()}"
    )

    # check last part of URL path
    assert (
        urlparse(downloader.getRequestUrl(region, code)).path.split("/")[-1] == region
    )


@pytest.mark.parametrize(
    "start, end, x, result",
    [
        (
            datetime.time(hour=1, minute=12),
            datetime.time(hour=1, minute=12),
            datetime.time(hour=1, minute=12),
            True,
        ),
        (
            datetime.time(hour=1, minute=12),
            datetime.time(hour=3, minute=1),
            datetime.time(hour=2, minute=0),
            True,
        ),
        (
            datetime.time(hour=1, minute=12),
            datetime.time(hour=2, minute=1),
            datetime.time(hour=5, minute=28),
            False,
        ),
        (
            datetime.time(hour=3, minute=12),
            datetime.time(hour=4, minute=1),
            datetime.time(hour=1, minute=28),
            False,
        ),
        # not sure why it is working like this, or if it is supposed to
        (
            datetime.time(hour=3, minute=12),
            datetime.time(hour=1, minute=1),
            datetime.time(hour=1, minute=28),
            False,
        ),
    ],
)
def test_timeInRange(start, end, x, result):
    assert downloader.timeInRange(start, end, x) == result


@pytest.mark.parametrize(
    "time_string, result",
    [
        (
            "1:12",
            datetime.time(hour=1, minute=12),
        ),
        (
            "6:55",
            datetime.time(hour=6, minute=55),
        ),
        (
            "15:10",
            datetime.time(hour=15, minute=10),
        ),
        (
            "18:15",
            datetime.time(hour=18, minute=15),
        ),
        (
            "",
            datetime.time(hour=0, minute=0),
        ),
    ],
)
def test_parseTime(time_string, result):
    assert downloader.parseTime(time_string) == result


JSON_SAMPLE = """
{
  "data" : [ {
    "primaryKey" : 4433,
    "ID" : 4433,
    "VALID_FROM" : 1635721200000,
    "VALID_TO" : 4070905200000,
    "DUMP_ID" : 42,
    "POVEL" : "A3B7DP6",
    "KOD" : null,
    "KOD_POVELU" : "458",
    "SAZBA" : "D57d",
    "INFO" : "TUV",
    "PLATNOST" : "Po - Pá",
    "DOBA" : "8",
    "CAS_ZAP_1" : "1:50",
    "CAS_VYP_1" : "6:55",
    "CAS_ZAP_2" : "15:10",
    "CAS_VYP_2" : "18:15",
    "CAS_ZAP_3" : null,
    "CAS_VYP_3" : null,
    "CAS_ZAP_4" : null,
    "CAS_VYP_4" : null,
    "CAS_ZAP_5" : null,
    "CAS_VYP_5" : null,
    "CAS_ZAP_6" : null,
    "CAS_VYP_6" : null,
    "CAS_ZAP_7" : null,
    "CAS_VYP_7" : null,
    "CAS_ZAP_8" : null,
    "CAS_VYP_8" : null,
    "CAS_ZAP_9" : null,
    "CAS_VYP_9" : null,
    "CAS_ZAP_10" : null,
    "CAS_VYP_10" : null,
    "DATE_OF_ENTRY" : 1635144876000,
    "DESCRIPTION" : "211101_podzim_stred"
  }, {
    "primaryKey" : 4434,
    "ID" : 4434,
    "VALID_FROM" : 1635721200000,
    "VALID_TO" : 4070905200000,
    "DUMP_ID" : 42,
    "POVEL" : "A3B7DP6",
    "KOD" : null,
    "KOD_POVELU" : "458",
    "SAZBA" : "D57d",
    "INFO" : "TUV",
    "PLATNOST" : "So - Ne",
    "DOBA" : "8",
    "CAS_ZAP_1" : "1:45",
    "CAS_VYP_1" : "6:50",
    "CAS_ZAP_2" : "15:10",
    "CAS_VYP_2" : "18:15",
    "CAS_ZAP_3" : null,
    "CAS_VYP_3" : null,
    "CAS_ZAP_4" : null,
    "CAS_VYP_4" : null,
    "CAS_ZAP_5" : null,
    "CAS_VYP_5" : null,
    "CAS_ZAP_6" : null,
    "CAS_VYP_6" : null,
    "CAS_ZAP_7" : null,
    "CAS_VYP_7" : null,
    "CAS_ZAP_8" : null,
    "CAS_VYP_8" : null,
    "CAS_ZAP_9" : null,
    "CAS_VYP_9" : null,
    "CAS_ZAP_10" : null,
    "CAS_VYP_10" : null,
    "DATE_OF_ENTRY" : 1635144876000,
    "DESCRIPTION" : "211101_podzim_stred"
  } ],
  "pageSize" : 20,
  "pageNumber" : 1,
  "pageOffset" : 0,
  "pageBarItems" : 5,
  "totalNumberOfRecords" : 2,
  "pagingModel" : { },
  "firstRecordNumberForPage" : 0,
  "lastPageNumber" : 1,
  "lastRecordNumber" : 2,
  "onePage" : true,
  "pageNumbersNavigation" : [ 1 ],
  "defaultPageNumbersAround" : [ 1 ],
  "fullyInitialized" : true,
  "last" : true,
  "first" : true
}"""


@pytest.mark.parametrize(
    "jsonCalendar, daytime, result",
    [
        # Thursday 0:46 UTC is 1:46 in Europe/Prague
        (
            JSON_SAMPLE,
            datetime.datetime(2021, 11, 18, 0, 46, tzinfo=ZoneInfo("UTC")),
            False,
        ),
        # Sunday 17:30 UTC+3 is 15:30 in Europe/Prague
        (
            JSON_SAMPLE,
            datetime.datetime(2021, 11, 21, 17, 30, tzinfo=ZoneInfo("Europe/Moscow")),
            True,
        ),
        # Sunday 14:30 UTC is 15:30 in Europe/Prague
        (
            JSON_SAMPLE,
            datetime.datetime(2021, 11, 21, 14, 30, tzinfo=ZoneInfo("UTC")),
            True,
        ),
    ],
)
def test_isHdo(jsonCalendar, daytime, result):
    assert downloader.isHdo(json.loads(jsonCalendar)["data"], daytime=daytime) == result
