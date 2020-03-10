FROM openjdk:8

RUN apt-get update -y && apt-get upgrade -y

RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs
RUN npm install -g serverless
RUN apt-get install -y python3-pip

RUN mkdir -p /app
WORKDIR /app

COPY package.json /app
COPY serverless.yml /app
COPY requirements.txt /app
COPY api /app/api

RUN npm install
RUN pip3 install -r requirements.txt

RUN sls dynamodb install

CMD ["sls", "offline", "start", "--host", "0.0.0.0"]