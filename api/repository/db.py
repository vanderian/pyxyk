import os

from pynamodb.connection.base import Connection

POOLS_TABLE = os.environ['POOLS_TABLE']
SWAPS_TABLE = os.environ['SWAPS_TABLE']

IS_OFFLINE = os.environ.get('IS_OFFLINE')


class Offline:
    if IS_OFFLINE:
        host = 'http://localhost:8000'


if IS_OFFLINE:
    connection = Connection(host='http://localhost:8000')
else:
    connection = Connection()

"""
would be very reasonable to wrap DB models behind repository classes to separate
app storage requirements from DB implementation, would also benefit mocks in testing 
"""
