from tabnanny import check
from flask import Flask, jsonify, request
from flask_cors import cross_origin
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
app.config["MONGO_URI"] = "mongodb+srv://hesso:LrnKxTD4CMngTQph@hesso.q1q2q.mongodb.net/sgtri2?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)


class questionAPI(Resource):
    @app.route("/questions/<int:id>", methods=["GET"])
    @cross_origin()
    def getQuestionByIDint(id):
        question = mongo.db.questions.find_one_or_404({"No_Controle": id})
        return Question(**question).to_json()

    @app.route("/questions/<string:id>", methods=["GET"])
    @cross_origin()
    def getQuestionByIDstring(id):
        question = mongo.db.questions.find_one_or_404(
            {"id": PydanticObjectId(id)})
        return Question(**question).to_json()

    @cross_origin()
    def post(self):
        question = request.get_json()
        questionAPI.postFinal(question)

    @cross_origin()
    def postFinal(raw_question):
        question = Question(**raw_question)
        insert_result = mongo.db.questions.insert_one(question.to_bson())
        print(question)
        return question.to_json()


class tagAPI(Resource):

    @app.route("/tags/<int:id>", methods=["GET"])
    @cross_origin() 
    def getTagByID(id):
        tag = mongo.db.tags.find_one_or_404({"id_int": id})
        return Tag(**tag).to_json()

    @app.route("/tags/<string:name>", methods=["GET"])
    @cross_origin()
    def getTagByName(name):
        tag = mongo.db.tags.find_one_or_404({"name": name})
        return Tag(**tag).to_json()
    @cross_origin()
    def post(self):
        tag = request.get_json()
        tagAPI.postFinal(tag)
    @cross_origin()
    def postFinal(raw_tag):
        tag = Tag(**raw_tag)
        insert_result = mongo.db.tags.insert_one(tag.to_bson())
        print(tag)
        return tag.to_json()


class motifAPI(Resource):
    @app.route("/motifs/<int:id>", methods=["GET"])
    @cross_origin()
    def getMotifByID(id):
        motif = mongo.db.motifs.find_one_or_404({"id_int": id})
        return Motif(**motif).to_json()

    @cross_origin()    
    def post(self):
        motif = request.get_json()
        motifAPI.postFinal(motif)

    @cross_origin()
    def postFinal(raw_motif):
        motif = Motif(**raw_motif)
        insert_result = mongo.db.motifs.insert_one(motif.to_bson())
        print(motif)
        return motif.to_json()


class motifquestionAPI(Resource):
    @app.route("/motifquestions/<int:id>", methods=["GET"])
    @cross_origin()
    def getMotifQuestionByID(id):
        qmotif = mongo.db.motifquestions.find_one_or_404({"idMotif": id})
        return MotifQuestion(**qmotif).to_json()

    @cross_origin()
    def post(self):
        qm = request.get_json()
        motifquestionAPI.postFinal(qm)

    @cross_origin()
    def postFinal(raw_qm):
        qmotif = MotifQuestion(**raw_qm)
        insert_result = mongo.db.motifquestions.insert_one(qmotif.to_bson())
        print(qmotif)
        return qmotif.to_json()


class patientAPI(Resource):
    @app.route("/patients/<string:id>", methods=["GET"])
    @cross_origin()
    def getPatientByID(id):
        patient = mongo.db.patients.find_one_or_404(
            {"id": PydanticObjectId(id)})
        return Patient(**patient).to_json()

    @app.route("/patients/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientByIDint(id):
        patient = mongo.db.patients.find_one_or_404({"id_int": id})
        return Patient(**patient).to_json()

    @cross_origin()
    def post(self):
        patient = request.get_json()
        patientAPI.postFinal(patient)

    @cross_origin()
    def postFinal(raw_patient):
        patient = Patient(**raw_patient)
        insert_result = mongo.db.patients.insert_one(patient.to_bson())
        print(patient)
        return patient.to_json()

class checkVitalsAPI(Resource):

    @app.route("/checkGlasgow/<int:glasgow>", methods=["GET"])
    @cross_origin()
    def checkGlasgow(glasgow):
        return check(glasgow, 0, 8, 9, 13, 14, 15)
    
    @app.route("/checkPulse/<int:pulse>", methods=["GET"])
    @cross_origin()
    def checkPulse(pulse):
        if pulse <= 40 or pulse >= 150: return jsonify({"degree": 1})
        elif pulse in [40-50] or pulse in [130-150]: return jsonify({"degree": 2})
        elif pulse in [51-129]: return jsonify({"degree": 3})

    @app.route("/checkTAS/<int:tas>", methods=["GET"])
    @cross_origin()
    def checkTAS(tas):
        if tas >= 230 or tas <= 70: return jsonify({"degree": 1})
        elif tas in [181-229] or tas in [71-90]: return jsonify({"degree": 2})
        elif tas in [91-180]: return jsonify({"degree": 3})
        
    
    @app.route("/checkTAD/<int:tad>", methods=["GET"])
    @cross_origin()
    def checkTAD(tad):
        if tad >= 130: return jsonify({"degree": 1})
        elif tad in [115-129]: return jsonify({"degree": 2})
        elif tad <= 115: return jsonify({"degree": 3})
        
    @app.route("/checkIDC/<int:pulse>/<int:tas>", methods=["GET"])
    @cross_origin()
    def checkIDC(pulse, tas):
        if pulse > tas: return jsonify({"degree": 2})
        elif pulse <= tas: return jsonify({"degree": 3})
    
    @app.route("/checkFR/<int:fr>", methods=["GET"])
    @cross_origin()
    def checkFR(fr):
        if fr >= 35: return jsonify({"degree": 1})
        elif fr in [25-35] or fr in [9-12]: return jsonify({"degree": 2})
        elif fr in [13-24]: return jsonify({"degree": 3})
    
    @app.route("/checkCYANOSE/<string:cyanose>", methods=["GET"])
    @cross_origin()
    def checkCYANOSE(cyanose):
        if cyanose == 'TRUE': return jsonify({"degree": 2})
        else: return jsonify({"degree": 3})

    @app.route("/checkSPO2/<int:spo2>", methods=["GET"])
    @cross_origin()
    def checkSPO2(spo2):
        if spo2 < 90 : return jsonify({"degree": 1})
        elif spo2 in [90-93]: return jsonify({"degree": 2})
        elif spo2 in [94-100]: return jsonify({"degree": 3})
    
    @app.route("/checkPEAKFL/<int:peakfl>", methods=["GET"])
    @cross_origin()
    def checkPEAKFL(peakfl):
        if peakfl <= 50 : return jsonify({"degree": 2})
        elif peakfl >= 50 : return jsonify({"degree": 3})
    
    @app.route("/checkTEMP/<float:temp>", methods=["GET"])
    @cross_origin()
    def checkTEMP(temp):
        if temp < 32 : return jsonify({"degree": 1})
        elif temp in [32-35] or temp > 40: return jsonify({"degree": 2})
        elif temp in [35.1-40]: return jsonify({"degree": 3})
    
    @app.route("/checkSUGAR/<float:sugar>", methods=["GET"])
    @cross_origin()
    def checkSUGAR(sugar):
        if sugar < 4 or sugar > 25 : return jsonify({"degree": 2})
        elif sugar in [4-24.9]: return jsonify({"degree": 3})

    @app.route("/checkACENTONURIA/<float:acen>", methods=["GET"])
    @cross_origin()
    def checkACENTONURIA(acen):
        if acen > 0.6: return jsonify({"degree": 2})
        elif acen < 0.6: return jsonify({"degree": 3})
    


# '/motifquestions' is our entry point for the questions for different motifs
api.add_resource(motifquestionAPI, '/motifquestions')
api.add_resource(tagAPI, '/tags')  # '/tags' is our entry point for tags
# '/questions' is our entry point for questions
api.add_resource(questionAPI, '/questions')
# '/motifs' is our entry point for motifs
api.add_resource(motifAPI, '/motifs')
# '/patients' is our entry point for patients
api.add_resource(patientAPI, '/patients')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
