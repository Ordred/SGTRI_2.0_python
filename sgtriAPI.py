import json
import math
from tabnanny import check
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_restful import Api, Resource
from motif import Motif
from patient import Patient
from question import Question
from flask_pymongo import PyMongo
from objectid import PydanticObjectId
from bson import json_util
import fastapi
import numpy as np
from bson.json_util import dumps, loads
from fastapi.encoders import jsonable_encoder

from objectid import PydanticObjectId
from tag import Tag
from motifquestion import MotifQuestion

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://hesso:LrnKxTD4CMngTQph@hesso.q1q2q.mongodb.net/sgtri2?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)

#Methods to get and post question data
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

    def postFinal(raw_question):
        questions = mongo.db.questions.find().sort('No_Controle', -1);
        question = Question(**raw_question)
        if questions[0] is not None: 
            lastQuestion = Question(**questions[0])
            question.No_Controle = lastQuestion.No_Controle + 1
        else : question.No_Controle = 1
        insert_result = mongo.db.questions.insert_one(question.to_bson())
        print(question)
        return question.to_json()

#Methods to get and post tag data
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
        tags = mongo.db.tags.find().sort('id_int', -1);
        tag = Tag(**raw_tag)
        if tags[0] is not None:
            lastTag = Tag(**tags[0])
            tag.id_int = lastTag.id_int + 1
        else:
            tag.id_int = 1
        insert_result = mongo.db.tags.insert_one(tag.to_bson())
        print(tag)
        return tag.to_json()

#Methods to get and post motif data
class motifAPI(Resource):
    @app.route("/motifs/<int:id>", methods=["GET"])
    @cross_origin()
    def getMotifByID(id):
        motif = mongo.db.motifs.find_one_or_404({"id_int": id})
        return Motif(**motif).to_json()

    @cross_origin()    
    def post(self):
        motif = request.get_json()
        return motifAPI.postFinal(motif)

    @cross_origin()
    def postFinal(raw_motif):
        motif = Motif(**raw_motif)
        motifs = mongo.db.motifs.find().sort('id_int', -1);
        if motifs[0] is not None:
            lastMotif = Motif(**motifs[0])
            motif.id_int = lastMotif.id_int + 1
        else:
            motif.id_int = 1
        insert_result = mongo.db.motifs.insert_one(motif.to_bson())
        print(motif)
        return motif.to_json()

#Methods to get and post motifs connected to questions data
class motifquestionAPI(Resource):
    @app.route("/motifquestions/<int:id>", methods=["GET"])
    @cross_origin()
    def getMotifQuestionByID(id):
        qmotif = mongo.db.motifquestions.find_one_or_404({"idMotif": id})
        return MotifQuestion(**qmotif).to_json()

    @cross_origin()
    def post(self):
        qm = request.get_json()
        return motifquestionAPI.postFinal(qm)

    @cross_origin()
    def postFinal(raw_qm):
        qmotif = MotifQuestion(**raw_qm)
        insert_result = mongo.db.motifquestions.insert_one(qmotif.to_bson())
        print(qmotif)
        return qmotif.to_json()

#Methods to get and post patient data
class patientAPI(Resource):
    @app.route("/patients", methods=["GET"])
    @cross_origin()
    def getAllPatients():
        patients = mongo.db.patients.find()
        documents = [doc for doc in patients]
        return json_util.dumps({'patientsList': documents})

    @app.route("/patients/<string:id>", methods=["GET"])
    @cross_origin()
    def getPatientByID(id):
        patient = mongo.db.patients.find_one_or_404(
            {"id": PydanticObjectId(id)})
        return Patient(**patient).to_json()

    @app.route("/patients/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientByIDint(id):
        patient = mongo.db.patients.find_one_or_404(
        {"id": PydanticObjectId(id)})
        return Patient(**patient).to_json()

    @app.route("/patients/byidint/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientByID_int(id):
        patient = mongo.db.patients.find_one_or_404({"id_int": id})
        return Patient(**patient).to_json()

    @app.route("/patients/pictures/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientImgByIDint(id):
        imgdata = mongo.db.patients.find_one_or_404({"id_int": id})
        imgjson = json.loads(json_util.dumps(imgdata))
        img = imgjson["image"]["$binary"]["base64"]
        return img

    @app.route("/patients/pictures/<int:id>", methods=["POST"])
    @cross_origin()
    def postPatientImgByIDint(id):
        img = request.get_data()
        print(img)
        mongo.db.patients.update_one({"id_int":id},{ "$set": { "image":img } })
        return "done"
    
    @cross_origin()
    def post(self):
        patient = request.get_json()
        return patientAPI.postFinal(patient)

    @cross_origin()
    def postFinal(raw_patient):
        patient = Patient(**raw_patient)
        patients = mongo.db.patients.find().sort('id_int', -1);
        if patients[0] is not None:
            lastPatient = Patient(**patients[0])
            patient.id_int = lastPatient.id_int + 1
        else : patient.id_int = 1;
        insert_result = mongo.db.patients.insert_one(patient.to_bson())
        print(patient)
        return patient.to_json()

    @app.route("/patients/<int:id>", methods=["DELETE"])
    @cross_origin()
    def deletePatientByIDint(id):
        mongo.db.patients.delete_one({"id_int": id})
        return "Patient id " + str(id) + " deleted"

#Methods to get and post values to get degrees for the sent values
class checkVitalsAPI(Resource):

    @app.route("/checkGlasgow/<int:glasgow>", methods=["GET"])
    @cross_origin()
    def checkGlasgow(glasgow):
        if glasgow <= 8: 
            return jsonify({"degree": 1})
        elif glasgow in range(8, 12): 
            return jsonify({"degree": 2})
        elif glasgow in range(13, 16): 
            return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkPulse/<int:pulse>", methods=["GET"])
    @cross_origin()
    def checkPulse(pulse):
        if pulse <= 40 or pulse >= 150: return jsonify({"degree": 1})
        elif pulse in range(39, 51) or pulse in range(130,150): return jsonify({"degree": 2})
        elif pulse in range(50,130): return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    @app.route("/checkTAS/<int:tas>", methods=["GET"])
    @cross_origin()
    def checkTAS(tas):
        if tas >= 230 or tas <= 70: return jsonify({"degree": 1})
        elif tas in range(180,230) or tas in range(71,90): return jsonify({"degree": 2})
        elif tas in range(90,181): return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
        
    
    @app.route("/checkTAD/<int:tad>", methods=["GET"])
    @cross_origin()
    def checkTAD(tad):
        if tad >= 130: return jsonify({"degree": 1})
        elif tad in range(114,130): return jsonify({"degree": 2})
        elif tad <= 115: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
        
    @app.route("/checkIDC/<int:pulse>/<float:tas>", methods=["GET"])
    @cross_origin()
    def checkIDC(pulse, tas):
        if pulse > tas: return jsonify({"degree": 2})
        elif pulse <= tas: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkFR/<int:fr>", methods=["GET"])
    @cross_origin()
    def checkFR(fr):
        if fr >= 35: 
            return jsonify({"degree": 1})
        elif fr in range(24,34) or fr in range(9,12): 
            return jsonify({"degree": 2})
        elif fr in range(13,25): 
            return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkCYANOSE/<string:cyanose>", methods=["GET"])
    @cross_origin()
    def checkCYANOSE(cyanose):
        if cyanose == 'TRUE': return jsonify({"degree": 2})
        else: return jsonify({"degree": 3})

    @app.route("/checkPUPILLES/<string:pupilles>", methods=["GET"])
    @cross_origin()
    def checkPUPILLES(pupilles):
        if pupilles == 'NORMALES': return jsonify({"degree": 4})
        else: return jsonify({"degree": 2})

    @app.route("/checkSPO2/<int:spo2>", methods=["GET"])
    @cross_origin()
    def checkSPO2(spo2):
        if spo2 < 90 : return jsonify({"degree": 1})
        elif spo2 in range(89,94): return jsonify({"degree": 2})
        elif spo2 in range(93,101): return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkPEAKFL/<int:peakfl>", methods=["GET"])
    @cross_origin()
    def checkPEAKFL(peakfl):
        if peakfl <= 50 : return jsonify({"degree": 2})
        elif peakfl >= 50 : return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkTEMP/<float:temp>", methods=["GET"])
    @cross_origin()
    def checkTEMP(temp):
        if temp < 32.0 : return jsonify({"degree": 1})
        elif temp in np.arange(31,36, 0.01) or temp > 40.0: return jsonify({"degree": 2})
        elif temp in np.arange(35.0,40.1, 0.01): return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkSUGAR/<float:sugar>", methods=["GET"])
    @cross_origin()
    def checkSUGAR(sugar):
        if sugar < 4.0 or sugar > 25.0 : return jsonify({"degree": 2})
        elif sugar in np.arange(3.9,25.0, 0.01): return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})

    @app.route("/checkACENTONURIA/<float:acen>", methods=["GET"])
    @cross_origin()
    def checkACENTONURIA(acen):
        if acen > 0.6: return jsonify({"degree": 2})
        elif acen < 0.6: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})

    @app.route("/checkDEP/<string:gender>/<int:age>/<int:size>", methods=["GET"])
    @cross_origin()
    def checkDEP(gender, age, size):
        dep = 0
        if gender == "m":
            dep = math.exp((0.544*math.log(age))-(0.0151*age)-(74.7/size)+5.48)
        if gender == "w":
            dep = math.exp((0.376*math.log(age))-(0.0120*age)-(58.8/size)+5.63)
        return jsonify({"dep": int(dep)})


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
    app.run()