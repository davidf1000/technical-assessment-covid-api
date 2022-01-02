from flask import Blueprint,request
import requests
from dateutil.parser import parse
import datetime

from api.constants.http_status_codes import HTTP_200_OK

yearly = Blueprint("yearly", __name__, url_prefix="/yearly")

"""
URL: http://<host>:<port>/yearly
Method: GET
Parameter:
- since: <year>
parameter to control since when (year) the data will be returned, by default since the year the first
cases detected. example: ?since=2020
- upto: <year>
parameter to control up to when (year) the data will be returned, by default up to the current year.
example: ?upto=2022
Description: Provide yearly data of total covid cases.
Response Body (JSON)
"""
@yearly.get('/')
def get_yearly_data():
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Find earliest daily data and current date 
    earliest = parse(min(list_daily,key=lambda x:parse(x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    since = parse(request.args.get('since')).replace(month=1,day=1) if request.args.get('since') is not None else earliest
    upto = parse(request.args.get('upto')).replace(month=12,day=31) if request.args.get('upto') is not None else current
    # Filter daily data that fits inside year range
    list_daily = [x for x in list_daily if since.timestamp()<=parse(x['key_as_string']).timestamp()<=upto.timestamp()]
    # Get set of year 
    list_daily_year_only = [parse(x['key_as_string']).year for x in list_daily]
    set_year = set(list_daily_year_only)
    # Create empty list 
    data = []
    # for each year, filter data in that year, then append 
    for year in set_year:
        positive = sum([x["jumlah_positif"]['value'] for x in list_daily if parse(x['key_as_string']).year == year])
        recovered = sum([x["jumlah_sembuh"]['value'] for x in list_daily if parse(x['key_as_string']).year == year])
        deaths = sum([x["jumlah_meninggal"]['value'] for x in list_daily if parse(x['key_as_string']).year == year])
        active = positive - recovered - deaths
        data.append({
            "year":year,
            "positive": positive ,
            "recovered": recovered,
            "deaths":deaths,
            "active":active
        })
    # Sort ASC by year
    data.sort(key = lambda x : x['year'])
    response = {
        "ok" : True,
        "data" : data,
        "message": "Request Successfull"     
        }
    return response,HTTP_200_OK
"""
Method: GET
Description: Provide yearly data of total covid cases of the year provided in <year>.
Response Body (JSON), example: /yearly/2020
"""
@yearly.get('/<year>')
def get_yearly_data_provided(year):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    res = requests.get(url)
    list_daily = res.json()['update']['harian']
    # Filter daily data that fits inside year range
    list_daily = [x for x in list_daily if parse(x['key_as_string']).year == int(year)]
    # Calculate positive, recovered, and deaths in that year, active = positive - recovered - deaths
    positive = sum([x["jumlah_positif"]['value'] for x in list_daily])
    recovered = sum([x["jumlah_sembuh"]['value'] for x in list_daily])
    deaths = sum([x["jumlah_meninggal"]['value'] for x in list_daily])
    active = positive - recovered - deaths
    data = {
        "year":year,
        "positive": positive ,
        "recovered": recovered,
        "deaths":deaths,
        "active":active
    }
    response = {
        "ok" : True,
        "data" : data,
        "message": "Request Successfull"       
        }
    return response,HTTP_200_OK
