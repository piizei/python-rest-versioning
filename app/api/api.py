from flask import Flask
from flask_restful import Resource, Api
from app.model.model import fit
from flask_healthz import Healthz

app = Flask(__name__)
Healthz(app)
api = Api(app)

class Model(Resource):
    def get(self):
        return {'version':'3', 'fit': fit().tolist() }

api.add_resource(Model, '/')

def run():
    app.run(debug=True)

if __name__ == '__main__':
    run()


app.config.update(
    HEALTHZ = {
        "live": "app.api.health.liveness",
        "ready": "app.api.health.readiness",
    }
)