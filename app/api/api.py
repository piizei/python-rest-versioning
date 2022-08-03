from flask import Flask
from flask_restful import Resource, Api
from app.model.model import fit

app = Flask(__name__)
api = Api(app)

class Model(Resource):
    def get(self):
        return {'fit': fit().tolist() }

api.add_resource(Model, '/')

def run():
    app.run(debug=True)

if __name__ == '__main__':
    run()