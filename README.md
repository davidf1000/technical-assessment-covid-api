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
docker run -it -d --network=host --rm -p 5000:5000 davidf1000/api-nodeflux-assessment
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
Run inside docker image : 
![dockerrun](https://user-images.githubusercontent.com/47879766/147946745-672f0062-04d5-4ad0-8591-aa87ab783b89.png)
Run using standalone web service : 
![pythonapp](https://user-images.githubusercontent.com/47879766/147946749-2c42667c-4736-4bb5-a116-578fba987e60.png)
Documentation of API using Postman : 

1.  API used for Covid Cases Data : https://hub.docker.com/r/davidf1000/api-nodeflux-assessment
![1](https://user-images.githubusercontent.com/47879766/147946715-f8430315-53eb-42a3-94a1-487afd811ea6.png)
2. "http://\<host\>:\<port\>/"  
![2](https://user-images.githubusercontent.com/47879766/147946723-e6319177-75a4-4b39-b30f-8b862d8914db.png)
3. http://\<host\>:\<port\>/yearly
![3](https://user-images.githubusercontent.com/47879766/147946724-14bf78b9-97b0-4d61-b6b2-bd575aea6b48.png)
4. http://\<host\>:\<port\>/yearly/\<year\>
![4](https://user-images.githubusercontent.com/47879766/147946726-5d0fad28-60af-4ca5-a1de-05505c2c2e46.png)
5. http://\<host\>:\<port\>/monthly
![5](https://user-images.githubusercontent.com/47879766/147946729-2ed9de3f-5758-44bc-a3a6-9b783effb4a2.png)
6. http://\<host\>:\<port\>/monthly/\<year\>
![6](https://user-images.githubusercontent.com/47879766/147946731-21255bd9-2123-43b3-a79d-758b74dcd5a7.png)
7. http://\<host\>:\<port\>/monthly/\<year\>/\<month\>
![7](https://user-images.githubusercontent.com/47879766/147946735-f31add29-a24c-472b-a0e9-84eca79ce55f.png)
8. http://\<host\>:\<port\>/daily
![8](https://user-images.githubusercontent.com/47879766/147946737-12e35e71-14dc-4419-b53f-5e3677c63c82.png)
9. http://\<host\>:\<port\>/daily/\<year\>
![9](https://user-images.githubusercontent.com/47879766/147946739-090e2886-2915-47e9-8df4-9deb0c528cca.png)
10. http://\<host\>:\<port\>/daily/\<year\>/\<month\>
![10](https://user-images.githubusercontent.com/47879766/147946741-7b0e0ffa-ea46-4dc5-959f-7e70143eff0c.png)
11. http://\<host\>:\<port\>/daily/\<year\>/\<month\>/\<date\>
![11](https://user-images.githubusercontent.com/47879766/147946742-8498c6ac-c39b-49d7-9197-253a63a9ad6b.png)
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
1. GeneralTest : http://\<host\>:\<port\>/
2. YearlyTest : http://\<host\>:\<port\>/yearly
3. YearlyProvidedYearTest : http://\<host\>:\<port\>/yearly/\<year\>
4. MonthlyTest : http://\<host\>:\<port\>/monthly
5. MonthlyProvidedYearTest : http://\<host\>:\<port\>/monthly/\<year\>
6. MonthlyProvidedYearMonthTest : http://\<host\>:\<port\>/monthly/\<year\>/\<month\>
7. DailyTest http://\<host\>:\<port\>/daily
8. DailyProvidedYearTest : http://\<host\>:\<port\>/daily/\<year\>
9. DailyProvidedYearMonthTest : http://\<host\>:\<port\>/daily/\<year\>/\<month\>
10. DailyProvidedYearMonthDateTest : http://\<host\>:\<port\>/daily/\<year\>/\<month\>/\<date\>

Or to run every testcase from every API : 
```shell
python3 tests/test_all.py
```

### Unit Test Result 
![test_result](https://user-images.githubusercontent.com/47879766/147946754-04927e16-e575-4d6a-987e-3dcfe1b5b4e1.png)
### Unit Test Coverage
To Check the coverage of unit test run: 
```shell
cd tests
coverage run -m unittest test_all.py
```
To show report of the results : 
```shell
coverage report
```
![coverage](https://user-images.githubusercontent.com/47879766/147946744-cc18c41c-4619-4937-9a5a-596f8595a51f.png)
Based on test coverage report, unit test has a test coverage of 95% 
## Additional Information
Based on Implementation of Covid Cases HTTP API, server is able to meet all the requirements needed and provide error handling for various scenarios. Unit testing of the API shows average test coverage of 95%. 
### Current Limitations
System still doesnt fully handle internal system error, especially when caused by improper JSON response structure and querying data  
### Future Ideation
- Use the API to create Covid Cases Plotter Website (Reference : https://github.com/davidf1000/Corona-Tracker-React , https://warm-mesa-01623.herokuapp.com/ ) 
- Further containerizing Flask Web Apps together with uWSGI and NGINX using docker compose so that it can be deployed securely with high performance and efficiency 
- Create new string query to sort lists of data with ASC or DESC order
- Create new string query to limit the elements of data lists for the first X latest data
