from flask import Blueprint, request
from dateutil.parser import parse
import requests
import datetime
import calendar

from api.constants.http_status_codes import HTTP_200_OK

daily = Blueprint("daily", __name__, url_prefix="/daily")

"""
URL: http://<host>:<port>/daily
Method: GET
Parameter:
- since: <year>.<month>.<date>
parameters to control since when (year, month, date) the data will be returned, by default since the
day the first cases detected. example: ?since=2020.03.02
- upto: <year>.<month>.<date>
parameters to control up to when (year, month, date) the data will be returned, by default up to
today. example: ?upto=2022.01.01
Description: Provide daily data of covid cases.
Response Body (JSON)
"""


@daily.get('/')
def get_daily_data():
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Find earliest daily data and current date
    earliest = parse(min(list_daily, key=lambda x: parse(
        x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    since = parse(request.args.get('since').replace('.', '-')
                  ) if request.args.get('since') is not None else earliest
    upto = parse(request.args.get('upto').replace('.', '-') # Deltatime 1 day ahead to ensure that 'upto' date is included in filter
                 ) + datetime.timedelta(days=1) if request.args.get('upto') is not None else current
    print("since",since)
    print("upto",upto.timestamp())
    # Filter daily data that fits inside year, month, and day range
    list_daily = [x for x in list_daily if since.timestamp() <= parse(
        x['key_as_string']).timestamp() <= upto.timestamp()]
    # Restructure every element in list to fit the needed structure
    # Create empty list
    data = []
    for item in list_daily:
        date = parse(item["key_as_string"])
        positive = item["jumlah_positif"]['value']
        recovered = item["jumlah_sembuh"]['value']
        deaths = item["jumlah_meninggal"]['value']
        active = positive - recovered - deaths
        data.append({
            "date": f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}',
            "positive": positive,
            "recovered": recovered,
            "deaths": deaths,
            "active": active
        })
    # Sort ASC
    data.sort(key=lambda x: x['date'])
    response = {
        "ok": True,
        "data": data,
        "message": "Request Successfull"
    }
    return response, HTTP_200_OK


"""
URL: http://<host>:<port>/daily/<year>
Method: GET
Parameter:
- since: <year>.<month>.<date>
parameters to control since when (year, month, date) the data will be returned, by default since the
first day of the year. example: ?since=2020.03.02
- upto: <year>.<month>.<date>
parameters to control up to when (year, month, date) the data will be returned, by default up to the
last day of the year. example: ?upto=2022.01.01
Description: Provide daily data of covid cases in the year provided in <year>
Response Body (JSON), example: /daily/2020
"""


@daily.get('/<year>')
def get_daily_data_of_provided_year(year):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Filter by year first before further processing
    list_daily = [x for x in list_daily if parse(x['key_as_string']).year == int(year)]        
    # Find earliest daily data and current date
    earliest = parse(min(list_daily, key=lambda x: parse(
        x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    since = parse(request.args.get('since').replace('.', '-')
                  ) if request.args.get('since') is not None else earliest
    upto = parse(request.args.get('upto').replace('.', '-') # Deltatime 1 day ahead to ensure that 'upto' date is included in filter
                 ) + datetime.timedelta(days=1) if request.args.get('upto') is not None else current
    # Filter daily data that fits inside year, month, and day range
    list_daily = [x for x in list_daily if since.timestamp() <= parse(
        x['key_as_string']).timestamp() <= upto.timestamp()]
    # Restructure every element in list to fit the needed structure
    # Create empty list
    data = []
    for item in list_daily:
        date = parse(item["key_as_string"])
        positive = item["jumlah_positif"]['value']
        recovered = item["jumlah_sembuh"]['value']
        deaths = item["jumlah_meninggal"]['value']
        active = positive - recovered - deaths
        data.append({
            "date": f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}',
            "positive": positive,
            "recovered": recovered,
            "deaths": deaths,
            "active": active
        })
    # Sort ASC
    data.sort(key=lambda x: x['date'])
    response = {
        "ok": True,
        "data": data,
        "message": "Request Successfull"
    }
    return response, HTTP_200_OK


"""
URL: http://<host>:<port>/daily/<year>/<month>
Method: GET
Parameter:
- since: <year>.<month>.<date>
parameters to control since when (year, month, date) the data will be returned, by default since the
first day of the month. example: ?since=2020.05.01
- upto: <year>.<month>.<date>
parameters to control up to when (year, month, date) the data will be returned, by default up to the
last day of the month. example: ?upto=2020.05.31
Description: Provide daily data of covid cases in the year and month provided in <year> and <month>.
Response Body (JSON), example: /daily/2020/05
"""


@daily.get('/<year>/<month>')
def get_daily_data_of_provided_year_month(year,month):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Filter by year and month first before further processing
    list_daily = [x for x in list_daily if f"{parse(x['key_as_string']).year}-{parse(x['key_as_string']).month}" == f"{year}-{int(month)}"]
    # Find earliest daily data and current date
    earliest = parse(min(list_daily, key=lambda x: parse(
        x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    since = parse(request.args.get('since').replace('.', '-')
                  ) if request.args.get('since') is not None else earliest
    upto = parse(request.args.get('upto').replace('.', '-') # Deltatime 1 day ahead to ensure that 'upto' date is included in filter
                 ) + datetime.timedelta(days=1) if request.args.get('upto') is not None else current
    
    # Filter daily data that fits inside year, month, and day range
    list_daily = [x for x in list_daily if since.timestamp() <= parse(
        x['key_as_string']).timestamp() <= upto.timestamp()]
    # Restructure every element in list to fit the needed structure
    # Create empty list
    data = []
    for item in list_daily:
        date = parse(item["key_as_string"])
        positive = item["jumlah_positif"]['value']
        recovered = item["jumlah_sembuh"]['value']
        deaths = item["jumlah_meninggal"]['value']
        active = positive - recovered - deaths
        data.append({
            "date": f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}',
            "positive": positive,
            "recovered": recovered,
            "deaths": deaths,
            "active": active
        })
    # Sort ASC
    data.sort(key=lambda x: x['date'])
    response = {
        "ok": True,
        "data": data,
        "message": "Request Successfull"
    }
    return response, HTTP_200_OK


"""
URL: http://<host>:<port>/daily/<year>/<month>/<date>
Method: GET
Description: Provide daily data of covid cases on the day provided in <year>, <month> and, <date>.
Response Body (JSON), example: /daily/2020/05/01
"""


@daily.get('/<year>/<month>/<day>')
def get_daily_data_of_provided_year_month_date(year, month, day):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Filter by year, month, and date first before further processing
    list_daily = [x for x in list_daily if f"{parse(x['key_as_string']).year}-{parse(x['key_as_string']).month}-{parse(x['key_as_string']).day}" == f"{year}-{int(month)}-{int(day)}"]
    print("list daily: ",list_daily)
    item = list_daily[0] 
    # Create empty list
    date = parse(item["key_as_string"])
    positive = item["jumlah_positif"]['value']
    recovered = item["jumlah_sembuh"]['value']
    deaths = item["jumlah_meninggal"]['value']
    active = positive - recovered - deaths
    data = {
        "date": f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}',
        "positive": positive,
        "recovered": recovered,
        "deaths": deaths,
        "active": active
    }
    response = {
        "ok": True,
        "data": data,
        "message": "Request Successfull"
    }
    return response, HTTP_200_OK
