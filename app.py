from flask import Flask
from api.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_500_INTERNAL_SERVER_ERROR
# Import Resource Class
from api.general.resource import general
from api.yearly.resource import yearly
from api.monthly.resource import monthly
from api.daily.resource import daily

app = Flask(__name__)
# api = Api(app)

blueprints = [general, yearly, monthly, daily]
# register blueprint
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# Error Handler


@app.errorhandler(HTTP_404_NOT_FOUND)
def handle_404(e):
    return {
        "ok": False,
        "message": "Error not found"
    },HTTP_404_NOT_FOUND


@app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
def handle_500(e):
    return {
        "ok": False,
        "message": "Internal server problem"
    },HTTP_500_INTERNAL_SERVER_ERROR
    
@app.errorhandler(HTTP_405_METHOD_NOT_ALLOWED)
def handle_405(e):
    return {
        "ok": False,
        "message": "Method Not Allowed"
    },HTTP_405_METHOD_NOT_ALLOWED


if __name__ == '__main__':
    app.run(debug=False, port=5000)
