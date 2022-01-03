[![Python](https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6--dev-blue.svg)]()
[![Travis](https://travis-ci.org/brennv/flask-app.svg?branch=master)](https://travis-ci.org/brennv/flask-app)
[![Coverage](https://codecov.io/gh/brennv/flask-app/branch/master/graph/badge.svg)](https://codecov.io/gh/brennv/flask-app)
[![Code Climate](https://codeclimate.com/github/brennv/flask-app/badges/gpa.svg)](https://codeclimate.com/github/brennv/flask-app)
[![Docker](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)]()

# Introduction
Nodeflux Software Engineer Internship Batch 2 Technical Assessment 
<br />
A docker containerized HTTP API server that could retrieve GET information about current status of covid cases and vaccination rates in Indonesia. Server is able to list the data by yearly, monthly, daily, and be able to provide information on general situations. Data is fetched from official Indonesian Goverment APIs. 
<br />
HTTP API server is written in Python using Flask Framework. Flask Blueprint is used for code modularization. Error handling is defined for various scenario and will reports errors by returning appropriate HTTP status code. Postman is used during the development process and Python unittest module is used to do unit testing for each created API. Python coverage module is used to measure test coverage. Server is containerized using Docker. The Docker Image is pushed to Docker Hub.

## Getting started




Install [docker](https://docs.docker.com/engine/installation/) and run:

```shell
docker-compose up
# docker-compose stop
```

Otherwise, for the standalone web service:

```shell
pip install -r requirements.txt
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

## Implementation

## Unit Tests

Standalone unit tests run with:

```shell
pip install pytest pytest-cov pytest-flask
pytest --cov=web/ --ignore=tests/integration tests
```

Integration and unit tests run with:

```shell
docker-compose -f test.yml -p ci build
docker-compose -f test.yml -p ci run test python -m pytest --cov=web/ tests
# docker stop ci_redis_1 ci_web_1
```

After testing, submit a pull request to merge changes with **develop**.

## Additional Information