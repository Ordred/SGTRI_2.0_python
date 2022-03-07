from flask import Flask, request
from flask_restful import Api, Resource
from model import Project
from flask_pymongo import PyMongo

import fastapi

from fastapi.encoders import jsonable_encoder

from objectid import PydanticObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hesso:admin@hesso.q1q2q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)

class HESSO(Resource):
    @app.route("/hesso/<string:name>", methods=["GET"])
    def get(name):
        project = mongo.db.hesso.find_one_or_404({"name": name})
        return Project(**project).to_json() 

    def post(self):   
        raw_project = request.get_json()
        project = Project(**raw_project)
        insert_result = mongo.db.hesso.insert_one(project.to_bson())
        project.id = PydanticObjectId(str(insert_result.inserted_id))
        print(project)
        return project.to_json()

api.add_resource(HESSO, '/hesso')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run(host="0.0.0.0")

