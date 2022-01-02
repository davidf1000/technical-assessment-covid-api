from flask import Blueprint,request

general = Blueprint("general", __name__, url_prefix="/")

"""
URL: http://<host>:<port>/
Method: GET
Description: Entry point for all API, provide general information of covid cases.
Response Body (JSON)
"""
@general.get('/')
def get_general_info():
    response = {"message":"covid cases general information"}
    return response,200
