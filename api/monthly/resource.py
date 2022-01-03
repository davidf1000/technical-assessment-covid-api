from flask import Blueprint,request
from dateutil.parser import parse
import requests
import datetime
import calendar
from api.checker.utils import check_param_date_range, check_param_month, check_param_year, check_string_year,check_string_year_month

from api.constants.http_status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST

monthly = Blueprint("monthly", __name__, url_prefix="/monthly")

"""
URL: http://<host>:<port>/monthly
Method: GET
Parameter:
- since: <year>.<month>
parameters to control since when (year, month) the data will be returned, by default since the month
the first cases detected. example: ?since=2020.03
- upto: <year>.<month>
parameters to control up to when (year, month) the data will be returned, by default up to the
current month. example: ?upto=2022.01
Description: Provide monthly data of total covid cases.
Response Body (JSON)
"""
@monthly.get('/')
def get_monthly_data():
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    try:
        res = requests.get(url,timeout=10)
    except:
        return {"ok" : False,"message" : "Error Fetching API from Goverment API"},HTTP_500_INTERNAL_SERVER_ERROR

    # Check query string validity 
    if 'since' in request.args:
        if not check_string_year_month(request.args['since']):
            return {"ok": False, "message": "Since parameter not valid"}, HTTP_400_BAD_REQUEST
    if 'upto' in request.args:
        if not check_string_year_month(request.args['upto']):
            return {"ok": False, "message": "Upto parameter not valid"}, HTTP_400_BAD_REQUEST
    if 'since' in request.args and 'upto' in request.args:
        if not check_param_date_range(request.args['since'], request.args['upto']):
            return {"ok": False, "message": "Since parameter must be older than upto"}, HTTP_400_BAD_REQUEST
            
    list_daily = res.json()['update']['harian']
    # Find earliest daily data and current date 
    earliest = parse(min(list_daily,key=lambda x:parse(x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    if request.args.get('since') is not None :
        since = parse(request.args.get('since').replace('.','-'))
        # replace hari dengan hari pertama dari bulan tersebut
        since.replace(day=1)
    else:
        since = earliest
    if request.args.get('upto') is not None : 
        upto = parse(request.args.get('upto').replace('.','-'))
        # replace hari dengan hari terakhir dari bulan tersebut
        upto.replace(day=calendar.monthrange(upto.year,upto.month)[1])
    else:
        upto = current
    
    # Filter daily data that fits inside year and month range
    list_daily = [x for x in list_daily if since.timestamp()<=parse(x['key_as_string']).timestamp()<=upto.timestamp()]
    # Get set of month 
    list_daily_date = [f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" for x in list_daily]
    set_date = set(list_daily_date)
    # Create empty list 
    data = []
    # for each date, filter data in that date, then append 
    # error handling
    try:
        for date in set_date:
            positive = sum([x["jumlah_positif"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            recovered = sum([x["jumlah_sembuh"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            deaths = sum([x["jumlah_meninggal"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            active = positive - recovered - deaths
            data.append({
                "month":date,
                "positive": positive ,
                "recovered": recovered,
                "deaths":deaths,
                "active":active
            })
    except Exception as e :
        return {"ok": False, "message": "System internal problem"}, HTTP_500_INTERNAL_SERVER_ERROR
    # if not a single record found, handle error
    if (len(data)==0):
        return {"ok": False, "message": "Data not found"}, HTTP_404_NOT_FOUND        
    # Sort ASC by month
    data.sort(key = lambda x : x['month'])
    response = {
        "ok" : True,
        "data" : data,
        "message": "Request Successfull"     
        }
    return response,HTTP_200_OK


"""
URL: http://<host>:<port>/monthly/<year>
Method: GET
Parameter:
- since: <year>.<month>
parameters to control since when (year, month) the data will be returned, by default since the first
month of the year. example: ?since=2020.03
- upto: <year>.<month>
parameters to control up to when (year, month) the data will be returned, by default up to the last
month of the year. example: ?upto=2020.12
Description: Provide monthly data of total covid cases in the year provided in <year>.
Response Body (JSON), example: /monthly/2020
"""
@monthly.get('/<year>/')
def get_monthly_data_of_provided_year(year):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    try:
        res = requests.get(url,timeout=10)
    except:
        return {"ok" : False,"message" : "Error Fetching API from Goverment API"},HTTP_500_INTERNAL_SERVER_ERROR
    # Check query string validity 
    if 'since' in request.args:
        if not check_string_year_month(request.args['since']):
            return {"ok": False, "message": "Since parameter not valid"}, HTTP_400_BAD_REQUEST
    if 'upto' in request.args:
        if not check_string_year_month(request.args['upto']):
            return {"ok": False, "message": "Upto parameter not valid"}, HTTP_400_BAD_REQUEST
    if 'since' in request.args and 'upto' in request.args:
        if not check_param_date_range(request.args['since'], request.args['upto']):
            return {"ok": False, "message": "Since parameter must be older than upto"}, HTTP_400_BAD_REQUEST
    # Check Param Path Validity
    if not check_param_year(year):
        return {"ok": False, "message": "Path parameter not valid"}, HTTP_400_BAD_REQUEST
    list_daily = res.json()['update']['harian']
    
    # Filter by year first before further processing
    list_daily = [x for x in list_daily if parse(x['key_as_string']).year == int(year)]
    # Find earliest daily data and current date 
    earliest = parse(min(list_daily,key=lambda x:parse(x['key_as_string']))['key_as_string'])
    current = datetime.datetime.now()
    # Get string query, if not found, use earliest data (since) or use current data (upto)
    if request.args.get('since') is not None :
        since = parse(request.args.get('since').replace('.','-')) - datetime.timedelta(days=1)
        # replace hari dengan hari pertama dari bulan tersebut
    else:
        since = earliest
    if request.args.get('upto') is not None : 
        upto = parse(request.args.get('upto').replace('.','-'))
        # replace hari dengan hari terakhir dari bulan tersebut
        upto.replace(day=calendar.monthrange(upto.year,upto.month)[1])
    else:
        upto = current
    # Make sure to check year == year in string query 
    # Filter daily data that fits inside year and month range
    list_daily = [x for x in list_daily if since.timestamp()<=parse(x['key_as_string']).timestamp()<=upto.timestamp()]
    # Get set of month 
    list_daily_date = [f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" for x in list_daily]
    set_date = set(list_daily_date)
    # Create empty list 
    data = []
    # for each date, filter data in that date, then append 
    # Error handle 
    try:
        for date in set_date:
            positive = sum([x["jumlah_positif"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            recovered = sum([x["jumlah_sembuh"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            deaths = sum([x["jumlah_meninggal"]['value'] for x in list_daily if f"{parse(x['key_as_string']).year}-{str(parse(x['key_as_string']).month).zfill(2)}" == date])
            active = positive - recovered - deaths
            data.append({
                "month":date,
                "positive": positive ,
                "recovered": recovered,
                "deaths":deaths,
                "active":active
            })
    except Exception as e :
        return {"ok": False, "message": "System internal problem"}, HTTP_500_INTERNAL_SERVER_ERROR
    # if not a single record found, handle error
    if (len(data)==0):
        return {"ok": False, "message": "Data not found"}, HTTP_404_NOT_FOUND                
    # Sort ASC by month
    data.sort(key = lambda x : x['month'])
    response = {
        "ok" : True,
        "data" : data,
        "message": "Request Successfull"     
        }
    return response,HTTP_200_OK

"""
URL: http://<host>:<port>/monthly/<year>/<month>
Method: GET
Description: Provide monthly data of total covid cases in the month and year provided in <year> and
<month>.
Response Body (JSON), example: /monthly/2020/03
"""
@monthly.get('/<year>/<month>')
def get_monthly_data_of_provided_month_year(year,month):
    # GET json data
    url = "https://data.covid19.go.id/public/api/update.json"
    try:
        res = requests.get(url,timeout=10)
    except:
        return {"ok" : False,"message" : "Error Fetching API from Goverment API"},HTTP_500_INTERNAL_SERVER_ERROR
    # Check Param Path Validity
    if not check_param_year(year) or not check_param_month(month):
        return {"ok": False, "message": "Path parameter not valid"}, HTTP_400_BAD_REQUEST
    list_daily = res.json()['update']['harian']
    list_daily = res.json()['update']['harian']
    # Filter by year and month first before further processing
    list_daily = [x for x in list_daily if f"{parse(x['key_as_string']).year}-{parse(x['key_as_string']).month}" == f"{year}-{int(month)}"]

    # if not a single record found, handle error
    if (len(list_daily)==0):
        return {"ok": False, "message": "Data not found"}, HTTP_404_NOT_FOUND        
   
    # Calculate positive, recovered, and deaths in that year, active = positive - recovered - deaths
    # Error handling
    try:
        positive = sum([x["jumlah_positif"]['value'] for x in list_daily])
        recovered = sum([x["jumlah_sembuh"]['value'] for x in list_daily])
        deaths = sum([x["jumlah_meninggal"]['value'] for x in list_daily])
        active = positive - recovered - deaths
        data = {
            "month":f"{year}-{str(month).zfill(2)}",
            "positive": positive ,
            "recovered": recovered,
            "deaths":deaths,
            "active":active
        }
    except Exception as e :
        return {"ok": False, "message": "System internal problem"}, HTTP_500_INTERNAL_SERVER_ERROR
   
    response = {
        "ok" : True,
        "data" : data,
        "message": "Request Successfull"     
        }
    return response,HTTP_200_OK
