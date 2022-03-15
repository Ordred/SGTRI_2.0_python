from flask import Flask, request
from flask_restful import Api, Resource
from motif import Motif
from patient import Patient
from question import Question
from flask_pymongo import PyMongo
from objectid import PydanticObjectId

import fastapi

from fastapi.encoders import jsonable_encoder

from objectid import PydanticObjectId
from tag import Tag
from motifquestion import MotifQuestion

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hesso:admin@hesso.q1q2q.mongodb.net/sgtri2?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)

class questionAPI(Resource):
    @app.route("/questions/<int:id>", methods=["GET"])
    def getQuestionByIDint(id):
        question = mongo.db.questions.find_one_or_404({"No_Controle": id})
        return Question(**question).to_json()

    @app.route("/questions/<string:id>", methods=["GET"])
    def getQuestionByIDstring(id):
        question = mongo.db.questions.find_one_or_404({"_id": PydanticObjectId(id)})
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
    def getTagByID(id):
        tag = mongo.db.tags.find_one_or_404({"id_int": id})
        return Tag(**tag).to_json()

    @app.route("/tags/<string:name>", methods=["GET"])
    def getTagByName(name):
        tag = mongo.db.tags.find_one_or_404({"name": name})
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

class motifAPI(Resource):
    @app.route("/motifs/<int:id>", methods=["GET"])
    def getMotifByID(id):
        motif = mongo.db.motifs.find_one_or_404({"id_int": id})
        return Motif(**motif).to_json()

    def post(self):   
        raw_motif = request.get_json()
        motif = Motif(**raw_motif)
        motifAPI.postFinal(motif)

    def postFinal(motif):
        motif = Motif(**motif)
        insert_result = mongo.db.motifs.insert_one(motif.to_bson())
        print(motif)
        return motif.to_json()

class motifquestionAPI(Resource):
    @app.route("/motifquestions/<int:id>", methods=["GET"])
    def getMotifQuestionByID(id):
        qmotif = mongo.db.motifquestions.find_one_or_404({"idMotif": id})
        return MotifQuestion(**qmotif).to_json()

    def post(self):   
        raw_qm = request.get_json()
        qmotif = MotifQuestion(**raw_qm)
        motifquestionAPI.postFinal(qmotif)

    def postFinal(qmotif):
        qmotif = MotifQuestion(**qmotif)
        insert_result = mongo.db.motifquestions.insert_one(qmotif.to_bson())
        print(qmotif)
        return qmotif.to_json()

class patientAPI(Resource):
    @app.route("/patients/<string:id>", methods=["GET"])
    def getPatientByID(id):
        patient = mongo.db.patients.find_one_or_404({"_id": PydanticObjectId(id)})
        return Patient(**patient).to_json()

    def post(self):   
        raw_patient = request.get_json()
        patient = Patient(**raw_patient)
        patientAPI.postFinal(patient)

    def postFinal(patient):
        insert_result = mongo.db.patients.insert_one(patient.to_bson())
        print(patient)
        return patient.to_json()

api.add_resource(motifquestionAPI, '/motifquestions')  # '/motifquestions' is our entry point for the questions for different motifs
api.add_resource(tagAPI, '/tags')  # '/tags' is our entry point for tags
api.add_resource(questionAPI, '/questions')  # '/questions' is our entry point for questions
api.add_resource(motifAPI, '/motifs')  # '/motifs' is our entry point for motifs
api.add_resource(patientAPI, '/patients')  # '/patients' is our entry point for patients

if __name__ == '__main__':
    app.run(host="0.0.0.0")

