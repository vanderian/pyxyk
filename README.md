# pyxyk

## Requirements
Python 3.5.2+


## Usage

```
$ npm install -g serverless
$ serverless install --url https://github.com/alexdebrie/serverless-flask --name my-flask-app
$ cd my-flask-app && npm run setup
<answer prompts>
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

## Local development

To develop locally, create a virtual environment and install your dependencies:

```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

Install and start DynamoDB Local

```
sls dynamodb install
sls dynamodb start
* Dynamodb Local Started, Visit: http://localhost:8000/shell
* Serverless: DynamoDB - created table pools-table-dev
* Serverless: DynamoDB - created table swaps-table-dev
```

Then, run your app:

```
sls wsgi serve
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
```

To see your app running locally navigate your browser
to [here:](http://localhost:8080/vanderian/pyxyk/1.0.0/ui/)

```
http://localhost:8080/vanderian/pyxyk/1.0.0/ui/
```

Your Swagger definition lives [here:](http://localhost:8080/vanderian/pyxyk/1.0.0/swagger.json)

```
http://localhost:8080/vanderian/pyxyk/1.0.0/swagger.json
```


To run the server directly, please setup virtualenv and execute the following from the root directory:

```
python3 -m api.app
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server
```