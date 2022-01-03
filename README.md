[![Python](https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6--dev-blue.svg)]()
[![Travis](https://travis-ci.org/brennv/flask-app.svg?branch=master)](https://travis-ci.org/brennv/flask-app)
[![Coverage](https://codecov.io/gh/brennv/flask-app/branch/master/graph/badge.svg)](https://codecov.io/gh/brennv/flask-app)
[![Code Climate](https://codeclimate.com/github/brennv/flask-app/badges/gpa.svg)](https://codeclimate.com/github/brennv/flask-app)
[![Docker](https://img.shields.io/docker/automated/jrottenberg/ffmpeg.svg?maxAge=2592000)]()

# Introduction
Nodeflux Software Engineer Internship Batch 2 Technical Assessment 
<br />
<br />
A docker containerized HTTP API server that could retrieve GET information about current status of covid cases and vaccination rates in Indonesia. Server is able to list the data by yearly, monthly, daily, and be able to provide information on general situations. Data is fetched from official Indonesian Goverment APIs. 
<br />
<br />
HTTP API server is written in Python using Flask Framework. Flask Blueprint is used for code modularization. Error handling is defined for various scenario and will reports errors by returning appropriate HTTP status code. Postman is used during the development process and Python unittest module is used to do unit testing for each created API. Python coverage module is used to measure test coverage. Server is containerized using Docker. The Docker Image is pushed to Docker Hub.

## Getting started

# Docker

Install [docker](https://docs.docker.com/engine/installation/) and pull application's docker image from :
<br/>
Docker Image repository link : 
<br/> 
pull docker image using : https://hub.docker.com/r/davidf1000/api-nodeflux-assessment
```shell
docker pull davidf1000/api-nodeflux-assessment
```

Run the image using : 
```shell
docker run -it -d --rm -p 5000:5000 covid-api-assessment
```

Otherwise, for the standalone web service:
```shell
pip install -r requirements.txt
python3 app.py
```

Visit [http://localhost:5000](http://localhost:5000)

<br/> <br/>
To build Docker images using Dockerfile, run :
```shell
docker build -t <image-name> . 
```
<br/> <br/>

## Implementation
Documentation of API using Postman : 

1.  API used for Covid Cases Data : https://hub.docker.com/r/davidf1000/api-nodeflux-assessment

2. http://<host>:<port>/  

3. http://<host>:<port>/yearly

4. http://<host>:<port>/yearly/<year>

5. http://<host>:<port>/monthly

6. http://<host>:<port>/monthly/<year>

7. http://<host>:<port>/monthly/<year>/<month>

8. http://<host>:<port>/daily

9. http://<host>:<port>/daily/<year>

10. http://<host>:<port>/daily/<year>/<month>

11. http://<host>:<port>/daily/<year>/<month>/<date>

## Unit Tests
Unit Test using unitest module. List of unit testing criteria implemented: 
1. 200 OK response
2. Method allowed
3. Content return
4. Query string validity
5. Path param validity
6. Response body  
7. 404 Not found response
Unit tests individual API with:

```shell
python3 tests/test_all.py <apiClassName> 
```
1. GeneralTest : http://<host>:<port>/
2. YearlyTest : http://<host>:<port>/yearly
3. YearlyProvidedYearTest : http://<host>:<port>/yearly/<year>
4. MonthlyTest : http://<host>:<port>/monthly
5. MonthlyProvidedYearTest : http://<host>:<port>/monthly/<year>
6. MonthlyProvidedYearMonthTest : http://<host>:<port>/monthly/<year>/<month>
7. DailyTest http://<host>:<port>/daily
8. DailyProvidedYearTest : http://<host>:<port>/daily/<year>
9. DailyProvidedYearMonthTest : http://<host>:<port>/daily/<year>/<month>
10. DailyProvidedYearMonthDateTest : http://<host>:<port>/daily/<year>/<month>/<date>

Or to run every testcase from every API : 
```shell
python3 tests/test_all.py
```

# Unit Test Result 

# Unit Test Coverage

## Additional Information
# Conclusion

# Current Limitations

# Potential Issues

# Future Ideation