import json

from datetime import datetime, timedelta
from itertools import count

MOCKED_DATETIME = "2020-03-09T14:55:47.365916+00:00"
MOCKED_DATETIME_1 = "2020-03-10T14:55:47.365916+00:00"


def gen_date():
    dt = datetime.fromisoformat(MOCKED_DATETIME)
    for i in count(0):
        yield dt + timedelta(days=i)


def mock_datetime_utcnow(mocker):
    dt = mocker.patch('api.controllers.swap.datetime')
    dt.now.side_effect = gen_date()


def parse_response_ok(response):
    status = response['statusCode']
    assert status == 200
    return json.loads(response['body'])


def sorted_ts(ts_list):
    return sorted(ts_list, key=lambda ts: ts['createdAt'])


def sorted_lp(lp_list):
    return sorted(lp_list, key=lambda ts: ts['tokenSymbol'])
