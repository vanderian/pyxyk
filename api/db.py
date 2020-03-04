import os

import boto3

POOLS_TABLE = os.environ['POOLS_TABLE']
SWAPS_TABLE = os.environ['SWAPS_TABLE']

IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.resource(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )

else:
    client = boto3.resource('dynamodb')

tablePools = client.Table(POOLS_TABLE)
tableSwaps = client.Table(SWAPS_TABLE)

# todo refactor as module with REPOS
