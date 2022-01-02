from flask import Blueprint,request

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
    since = request.args.get('since')
    upto = request.args.get('upto')
    response = {
        "message":"covid cases yearly information",
        "since": since,
        "upto" : upto
        }
    return response,200
"""
Method: GET
Description: Provide yearly data of total covid cases of the year provided in <year>.
Response Body (JSON), example: /yearly/2020
"""
@yearly.get('/<year>')
def get_yearly_data_provided(year):
    response = {
        "message":"covid cases information of provided year",
        "year":year
        }
    return response,200
