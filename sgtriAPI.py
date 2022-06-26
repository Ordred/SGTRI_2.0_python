import json
import math
import string
from tabnanny import check
from flask import Flask, jsonify, request
from flask_cors import cross_origin
from flask_restful import Api, Resource
from motif import Motif
from patient import Patient
from question import Question
from user import User
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
#app.config["MONGO_URI"] = "mongodb+srv://hesso:LrnKxTD4CMngTQph@cluster0.jaajphx.mongodb.net/?retryWrites=true&w=majority"
mongo = PyMongo(app)
api = Api(app)


    
#Methods to get and post question data
class questionAPI(Resource):
    @app.route("/questions", methods=["GET"])
    @cross_origin()
    def getAll137Questions():
        questions = mongo.db.questions.find()
        documents = [doc for doc in questions]
        return json_util.dumps({'questionsList': documents})
        
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
        if mongo.db.questions:
            questions = list(mongo.db.questions.find().sort('No_Controle', -1))
        question = Question(**raw_question)
        if questions: 
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

    def postFinal(raw_tag):
        tags = list(mongo.db.tags.find().sort('id_int', -1))
        tag = Tag(**raw_tag)
        if tags is not []:
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

    def postFinal(raw_motif):
        motif = Motif(**raw_motif)
        motifs = list(mongo.db.motifs.find().sort('id_int', -1))
        if motifs:
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
    #Get All Patients
    @app.route("/patients", methods=["GET"])
    @cross_origin()
    def getAllPatients():
        patients = mongo.db.patients.find()
        documents = [doc for doc in patients]
        return json_util.dumps({'patientsList': documents})
    #Get patient by id (string)
    @app.route("/patients/<string:id>", methods=["GET"])
    @cross_origin()
    def getPatientByID(id):
        patient = mongo.db.patients.find_one_or_404(
            {"id": PydanticObjectId(id)})
        return Patient(**patient).to_json()
    #Get patient by id (int)
    @app.route("/patients/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientByIDint(id):
        patient = mongo.db.patients.find_one_or_404(
        {"id_int": id})
        return Patient(**patient).to_json()
    #Get patient by id (string)
    @app.route("/patients/byidint/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientByID_int(id):
        patient = mongo.db.patients.find_one_or_404({"id_int": id})
        return Patient(**patient).to_json()
    #GetPicture of patient
    @app.route("/patients/pictures/<int:id>", methods=["GET"])
    @cross_origin()
    def getPatientImgByIDint(id):
        imgdata = mongo.db.patients.find_one_or_404({"id_int": id})
        imgjson = json.loads(json_util.dumps(imgdata))
        img = imgjson["image"]["$binary"]["base64"]
        return img
    #Set Picure for one patient
    @app.route("/patients/pictures/<int:id>", methods=["POST"])
    @cross_origin()
    def postPatientImgByIDint(id):
        img = request.get_data()
        print(img)
        mongo.db.patients.update_one({"id_int":id},{ "$set": { "image":img } })
        return "done"
    
    #test get questions
    @app.route("/patients/questions/<string:id>", methods=["GET"])
    @cross_origin()
    def getQuestionByIDstringFromPatient(id):
        patinetInt = int(id.split('p')[0])
        patient = mongo.db.patients.find_one_or_404({"id_int": patinetInt})
        questionsjson = json.loads(json_util.dumps(patient))
        print("questionJson:",questionsjson["questions"])
        documents = [doc for doc in questionsjson["questions"]]
        return json_util.dumps({'questionsList': documents})
        #question = patient.find({"questions":{"No_Controle":questionInt}})
        #return Question(**question).to_json()
       
    
    #Create new Vignette
    @cross_origin()
    def post(self):
        patient = request.get_json()
        return patientAPI.postFinal(patient)

    @cross_origin()
    def postFinal(raw_patient):
        patient = Patient(**raw_patient)
        print(patient.to_json(),"ID_int", patient.id_int)
        patients = list(mongo.db.patients.find().sort('id_int', -1))
        if patients:
            lastPatient = Patient(**patients[0])
            patient.id_int = lastPatient.id_int + 1
        else : patient.id_int = 1
        insert_result = mongo.db.patients.insert_one(patient.to_bson())
        return patient.to_json()
    
    #Replace Vignette by #Get patient by id (string)
    @app.route("/patients/modify", methods=["Post"])
    @cross_origin()
    def post(self):
        patient = request.get_json()
        return patientAPI.postModifyFinal(patient)
    @cross_origin()
    def postModifyFinal(raw_patient):
        patient = Patient(**raw_patient)
        print(patient.to_json(),"ID_int", patient.id_int)
        patients = list(mongo.db.patients.find().sort('id_int', -1))
        if patients:
            lastPatient = Patient(**patients[0])
            patient.id_int = lastPatient.id_int + 1
        else : patient.id_int = 1
        insert_result = mongo.db.patients.insert_one(patient.to_bson())
        return patient.to_json()
        
    #Delete Vignette by Id
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
    
    @app.route("/checkTEMP/<string:temp>", methods=["GET"])
    @cross_origin()
    def checkTEMP(temp):
        tempfloat = float(temp)
        if tempfloat < 32.0 : return jsonify({"degree": 1})
        elif tempfloat >= 32.0 and tempfloat <= 35.0 or tempfloat > 40.0: return jsonify({"degree": 2})
        elif tempfloat >= 35.1 and tempfloat <= 40.0: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})
    
    @app.route("/checkSUGAR/<string:sugar>", methods=["GET"])
    @cross_origin()
    def checkSUGAR(sugar):
        sugarfloat = float(sugar)
        if sugarfloat < 4.0 or sugarfloat >= 25.0: return jsonify({"degree": 2})
        elif sugarfloat >= 4.0 and sugarfloat <= 24.9: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})

    @app.route("/checkACENTONURIA/<string:acen>", methods=["GET"])
    @cross_origin()
    def checkACENTONURIA(acen):
        acenfloat = float(acen)
        if acenfloat >= 0.6: return jsonify({"degree": 2})
        elif acenfloat < 0.6: return jsonify({"degree": 3})
        else: return jsonify({"degree": 4})

    @app.route("/checkDEP/<string:gender>/<int:age>/<int:size>", methods=["GET"])
    @cross_origin()
    def checkDEP(gender, age, size):
        dep = 0
        if gender == "m":
            dep = math.exp((0.544*math.log(age))-(0.0151*age)-(74.7/size)+5.48)
        if gender == "f":
            dep = math.exp((0.376*math.log(age))-(0.0120*age)-(58.8/size)+5.63)
        return jsonify({"dep": int(dep)})

#Methods to get and post values user account
class loginAPI(Resource) :
    #Get All Users #works
    @app.route("/logins/users", methods=["GET"])
    @cross_origin()
    def getAllUsers():
        users = mongo.db.users.find()
        documents = [doc for doc in users]
        print("GetAllUser:", json_util.dumps({'userlist': documents}))
        return json_util.dumps({'userlist': documents})

    #Get user by id_int:Work
    @app.route("/logins/users/<int:id>", methods=["GET"])
    @cross_origin()
    def getUsertByInt(id):
        print("GetUsenameIsCalled:",id)
        user = mongo.db.users.find_one_or_404({"id_int": id})
        print(User(**user).to_json())
        return User(**user).to_json()
    
    #Get User by username:Work
    @app.route("/logins/username/<string:name>", methods=["GET"])
    @cross_origin()
    def getUsertByUsername(name):
        print("GetUsenameIsCalled:",name)
        user = mongo.db.users.find_one_or_404({"username": name})
        print(User(**user).to_json())
        return User(**user).to_json()
    
    #Check if Username exist
    #@app.route("/logins/checkusername/<string:name>", methods=["GET"])
    #@cross_origin()
    #def CheckUsername(name):
        print("GetUsenameIsCalled:",name)
        user = mongo.db.users.find_one_or_404({"username": name})
        print(User(**user).to_json())
        users = list(mongo.db.users.find())
        print("list of uers:", users)
        for _user in users:
            #print("user of list:", _user.username, " == ", user.username)
            print("username to check:",User(**user).username)
            print("user of list:", User(**_user).username)
            if User(**_user).username != User(**user).username :
                return "true"
            else :
                return "false"
    
    #Create new User working
    @cross_origin()
    def post(self):
        user = request.get_json()
        return loginAPI.postNewUser(user)

    @cross_origin()
    def postNewUser(raw_user):
        user = User(**raw_user)
        print(user.to_json(),"ID_int", user.id_int)
        users = list(mongo.db.users.find().sort('id_int', -1))
        if users:
            lastUser = User(**users[0])
            user.id_int = lastUser.id_int + 1
        else : user.id_int = 1
        insert_result = mongo.db.users.insert_one(user.to_bson())
        return user.to_json()
    
    #Delete Users
    @app.route("/logins/username/<string:id>", methods=["DELETE"])
    @cross_origin()
    def deleteUserByUsername(id):
        user = mongo.db.users.find_one_or_404({"username": id})
        print("user to delete :",User(**user).to_json())
        mongo.db.users.delete_one({"username": id})
        return "Patient " + str(id) + " deleted"
    


# '/motifquestions' is our entry point for the questions for different motifs
api.add_resource(motifquestionAPI, '/motifquestions')
 # '/tags' is our entry point for tags
api.add_resource(tagAPI, '/tags') 
# '/questions' is our entry point for questions
api.add_resource(questionAPI, '/questions')
# '/motifs' is our entry point for motifs
api.add_resource(motifAPI, '/motifs')
# '/patients' is our entry point for patients
api.add_resource(patientAPI, '/patients')
# '/login' is our entry point for patients
api.add_resource(loginAPI, '/logins')

if __name__ == '__main__':
    app.run(host="127.0.0.1")
