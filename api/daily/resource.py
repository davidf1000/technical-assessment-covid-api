from flask import Blueprint,request

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
@daily.get('')
def get_daily_data():
    since = request.args.get('since')
    upto = request.args.get('upto')
    response = {
        "message":"covid cases daily information",
        "since": since,
        "upto" : upto
        }
    return response,200


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
    since = request.args.get('since')
    upto = request.args.get('upto')
    response = {
        "message":"daily covid cases information of provided year",
        "year":year,
        "since": since,
        "upto" : upto
        }
    return response,200

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
    since = request.args.get('since')
    upto = request.args.get('upto')    
    response = {
        "message":"daily covid cases information in the provided year and month",
        "year":year,
        "month":month,
        "since":since,
        "upto":upto
        }
    return response,200

"""
URL: http://<host>:<port>/daily/<year>/<month>/<date>
Method: GET
Description: Provide daily data of covid cases on the day provided in <year>, <month> and, <date>.
Response Body (JSON), example: /daily/2020/05/01
"""
@daily.get('/<year>/<month>/<date>')
def get_daily_data_of_provided_year_month_date(year,month,date):
    response = {
        "message":"daily covid cases information in the provided year, month, and date",
        "year":year,
        "month":month,
        "date":date
        }
    return response,200