from flask import Flask
from flask_restful import Api,Resource, abort,reqparse

app = Flask(__name__)
api = Api(app)

class GeneralInformation(Resource):
    def get(self):
        result = {"message":"hello world"}
        return result,200

api.add_resource(GeneralInformation,"/")

if __name__ == '__main__':
    app.run(debug=True,port=5000)
