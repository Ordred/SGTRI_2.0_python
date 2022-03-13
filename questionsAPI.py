from flask import Flask, request
from flask_restful import Api, Resource
from question import Question
from flask_pymongo import PyMongo

import fastapi

from fastapi.encoders import jsonable_encoder

from objectid import PydanticObjectId
from tag import Tag

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hesso:admin@hesso.q1q2q.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)

class questionAPI(Resource):
    @app.route("/questions/<int:id>", methods=["GET"])
    def getQuestion(id):
        question = mongo.db.questions.find_one_or_404({"No_Controle": id})
        return Question(**question).to_json() 

    def post(self):   
        raw_question = request.get_json()
        question = Question(**raw_question)
        questionAPI.postFinal(question)

    def postFinal(question):
        question = Question(**question)
        insert_result = mongo.db.questions.insert_one(question.to_bson())
        print(question)
        return question.to_json()

class tagAPI(Resource):
    @app.route("/tags/<int:id>", methods=["GET"])
    def getTag(id):
        tag = mongo.db.tags.find_one_or_404({"id_int": id})
        return Tag(**tag).to_json() 

    def post(self):   
        raw_tag = request.get_json()
        tag = Tag(**raw_tag)
        tagAPI.postFinal(tag)

    def postFinal(tag):
        tag = Tag(**tag)
        insert_result = mongo.db.tags.insert_one(tag.to_bson())
        print(tag)
        return tag.to_json()

api.add_resource(tagAPI, '/tags')  # '/tags' is our entry point for Users
api.add_resource(questionAPI, '/questions')  # '/questions' is our entry point for Users

if __name__ == '__main__':
    app.run()

