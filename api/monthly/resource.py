from flask import Blueprint,request

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
@monthly.get('')
def get_monthly_data():
    since = request.args.get('since')
    upto = request.args.get('upto')
    response = {
        "message":"covid cases monthly information",
        "since": since,
        "upto" : upto
        }
    return response,200


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
@monthly.get('/<year>')
def get_monthly_data_of_provided_year(year):
    since = request.args.get('since')
    upto = request.args.get('upto')
    response = {
        "message":"Monthly covid cases information of provided year",
        "year":year,
        "since": since,
        "upto" : upto
        }
    return response,200

"""
URL: http://<host>:<port>/monthly/<year>/<month>
Method: GET
Description: Provide monthly data of total covid cases in the month and year provided in <year> and
<month>.
Response Body (JSON), example: /monthly/2020/03
"""
@monthly.get('/<year>/<month>')
def get_monthly_data_of_provided_month_year(year,month):
    response = {
        "message":"monthly covid cases information in the provided month and year",
        "year":year,
        "month":month
        }
    return response,200
