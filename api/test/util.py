import json

from datetime import datetime

MOCKED_DATETIME = "2020-03-09T14:55:47.365916+00:00"


def mock_datetime_utcnow(mocker):
    dt = mocker.patch('api.controllers.swap.datetime')
    dt.now.return_value = datetime.fromisoformat(MOCKED_DATETIME)


def parse_response_ok(response):
    status = response['statusCode']
    assert status == 200
    return json.loads(response['body'])
