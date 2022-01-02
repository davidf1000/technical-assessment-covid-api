from flask import Flask
# Import Resource Class
from api.general.resource import general
from api.yearly.resource import yearly
from api.monthly.resource import monthly
from api.daily.resource import daily

app = Flask(__name__)
# api = Api(app)

blueprints = [general,yearly,monthly,daily]
# register blueprint
for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True,port=5000)
