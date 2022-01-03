from flask import Blueprint, request
import requests
from api.constants.http_status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
general = Blueprint("general", __name__)

"""
URL: http://<host>:<port>/
Method: GET
Description: Entry point for all API, provide general information of covid cases.
Response Body (JSON)
"""


@general.get('/')
def get_general_info():
    url = "https://data.covid19.go.id/public/api/update.json"
    try:
        res = requests.get(url, timeout=10)
    except:
        return {"ok": False, "message": "Error Fetching API from Goverment API"}, HTTP_500_INTERNAL_SERVER_ERROR
    data = res.json()
    # Catch Error if wrong dict structure
    try:
        total_positive = data['update']['total']['jumlah_positif']
        total_recovered = data['update']['total']['jumlah_sembuh']
        total_deaths = data['update']['total']['jumlah_meninggal']
        total_active = total_positive - total_recovered - total_deaths

        new_positive = data['update']['penambahan']['jumlah_positif']
        new_recovered = data['update']['penambahan']['jumlah_sembuh']
        new_deaths = data['update']['penambahan']['jumlah_meninggal']
        new_active = new_positive - new_recovered - new_deaths

        response = {
            "ok": True,
            "data": {
                "total_positive": total_positive,
                "total_recovered": total_recovered,
                "total_deaths": total_deaths,
                "total_active": total_active,
                "new_positive": new_positive,
                "new_recovered": new_recovered,
                "new_deaths": new_deaths,
                "new_active": new_active
            },
            "message": "Request Successfull"
        }
        return response, HTTP_200_OK
    except Exception as e:
        return {"ok": False, "message": "System internal problem"}, HTTP_500_INTERNAL_SERVER_ERROR
