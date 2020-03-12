# pyxyk

## Requirements
Python 3.7.+


## Usage

```
$ npm install -g serverless
$ npm run setup
$ serverless deploy
```

Once the deploy is complete, run `sls info` to get the endpoint:

```
$ sls info
Service Information
<snip>
endpoints:
  ANY - https://abc6defghi.execute-api.us-east-1.amazonaws.com/dev <-- Endpoint
  ANY - https://abc6defghi.execute-api.us-east-1.amazonaws.com/dev/{proxy+}
```

Copy paste into your browser, and _voila_!

## Local development with Docker

Docker image can be used to run the API locally, API is exposed on :3000, local dynamoDb on :8000

```
docker-compose up -d --build
docker-compose down
```


## Local development

To develop locally, create a virtual environment and install your dependencies:

```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

Install DynamoDB Local and start serverless offline

```
sls dynamodb install
sls offline start
* Dynamodb Local Started, Visit: http://localhost:8000/shell
* Serverless: DynamoDB - created table pools-table-dev
* Serverless: DynamoDB - created table swaps-table-dev
* Serverless: Starting Offline: dev/eu-central-1.
```

## Testing

End-to-end tests on deployed API are missing, a custom implementation can be made or some tool levering openaapi.yml could be used.

You can use swagger-ui docker image with included openapi definition to test the REST methods. 
```
docker run -p 80:8080 -e SWAGGER_JSON=/api/openapi.yaml -v `pwd`/openapi:/api swaggerapi/swagger-ui
```

Some tests require local dynamo db. See local deployment.

To launch the tests use tox:
```
sudo pip install tox
tox
```