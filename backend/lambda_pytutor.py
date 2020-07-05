import boto3, traceback
import uuid
from urllib.parse import unquote_plus
import datetime
import json, urllib, boto3, botocore, base64, time, traceback, random, string, copy
from collections import defaultdict as ddict
import json, random, time

from lambda_framework import *

import json

def lambda_handler(event, context):
    try:
        event = eval(event["body"])
        # TODO: well need to specify this in all calls from the front end...
        course = event.get('course', 'a')
        if not course in ('a', 'b', 'c'):
            return error('invalid course ID: "%s"' % course)
        init_s3("pytutor")
    
        ts0 = datetime.datetime.utcnow().timestamp()
    
        # identify user
        try:
            user = get_user(event)
        except Exception as e:
            user = None
    
        # try to invoke the function
        fn = ROUTES.get(event['fn'], None)
        if fn != None:
            try:
                # if a check fails, it will raise an exception
                for checker in EXTRA_AUTH[event["fn"]]:
                    checker(user)
    
                return {
                        'statusCode': 200,
                        'headers': {
                                'Access-Control-Allow-Headers': 'Content-Type',
                                'Access-Control-Allow-Origin': 'http://pytutor.ddns.net',
                                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                            },
                        'body': json.dumps(fn(user, event))
                    }
                result = {
                    "isBase64Encoded": False,
                    "statusCode": code,
                    "headers": {},
                    "body": data
                }
            except Exception as e:
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': 'http://pytutor.ddns.net',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                    },
                    'body': json.dumps(['Test1 from Lambda!',str(e), str(event), str(traceback.format_exc())])
                }
                result = error('Exception: '+str(e) + ' '+traceback.format_exc())
        else:
            result = error('no route for '+event['fn'])
    
        # try to log the event
        ts1 = datetime.datetime.utcnow().timestamp()
    
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'http://pytutor.ddns.net',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(['Test1 from Lambda!',str(e), str(event), str(e)])
            }
    except Exception as e:
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Origin': 'http://pytutor.ddns.net',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(['Test1 from Lambda!',str(e), str(event), str(traceback.format_exc())])
            }

'''
This function is to check the answer and update the record of student and report

parameter  
    
    event={
        "fn": "addNewAnswer",
        "worksheetCode": worksheetCode,
        "questionCode":questionCode,
        "response":"student answer
    }
    user={
        "email":email,
        "hd":"wisc.edu"(optional, only appears when the email end with wisc.edu)
    }

return 
        
    {
        "errorCode": errCode(optional,only when error appears),
        "fnExecuted":"addNewAnswer",
        "isCorrect": {questionCode:True/False}(if error appears, this would be empty) 
    }  
'''
@route
@user
def addNewAnswer(user, event):
    result={
            "fnExecuted":"addNewAnswer",
            "isCorrect": {}
        }
    student=Student(event,s3(),BUCKET,user)
    if student.isWisconsin==True:
        student.getFile()
    else:
        result["incorrectDomain"]=True
    errorCode,isCorrect=student.upload()
    if errorCode!=None:
        result["errorCode"]=errorCode
        return result
    result["isCorrect"][student.questionCode]=isCorrect
    if student.isWisconsin==True:
        report=Report(event,s3(),BUCKET)
        report.getFile()
        report.updateReport(student.student,student.questionCode)
    return result


'''
This function is to reload the record of one worksheet of the user

parameter  
    
    event={
        "fn": "reload",
        "worksheetCode": worksheetCode,
    }
    user={
        "email":email,
        "hd":"wisc.edu"(optional, only appears when the email end with wisc.edu)
    }

return 

    {
        "errorCode": errCode(optional,only when error appears),
        "fnExecuted":"reload",
        "isCorrect": {questionCode1:True/False,
                      questionCode2:True/False,
                      ...
                    }(if error appears, this would be empty) 
    }
'''
@route
@user
def reload(user,event):
    result={
            "fnExecuted":"reload",
            "isCorrect": {}
    }
    student=Student(event,s3(),BUCKET,user)
    if student.isWisconsin==False:
        result["incorrectDomain"]=True
    errorCode,answerList= student.reload()
    if errorCode!=None:
        result["errorCode"]=errorCode
        return result
    result["isCorrect"]=answerList
    return result

'''
This function is to reload the report of one worksheet 

parameter  

    event={
        "fn": "getReport",
        "worksheetCode": worksheetCode,
    }
    user={
        "email":email,
        "hd":"wisc.edu"(optional, only appears when the email end with wisc.edu)
    }

return 
    
    {
        "errorCode": errCode(optional,only when error appears),
        "fnExecuted":"getReport",
        "report": {report}(if error appears, this would be empty) 
    }
'''
@route
@user
def getReport(user,event):
    result={
            "fnExecuted":"getReport",
            "report":{}
        }
    report=Report(event,s3(),BUCKET)
    errorCode=report.getFile()
    if errorCode!=None:
        result["errorCode"]=errorCode
        return result

    result["report"]=report.getReport()
    return result

'''
pytutor/student/username.json

    {
    "studentID":id,
    "numberOfWorksheetAttempted":2,
    "WorksheetCode1":{
        questionsAttempted: ,
        questionCorrectlyAttempted: ,
        q1:{
            numAttempts:    [numAttemptsTIllCorrect, totalNumAttempts]
            isCorrect:  False/True #once they have correctly attempted becomes true,
                                                else False
            attemts:[
                    [timeStamp, attemptedAnswer],
                    [timeStamp, attemptedAnswer],
                    [timeStamp, attemptedAnswer]                                
                    ]
            },
                    
            ....
        },
    "WorksheetCode2":{
            .....
        },
        .....
    }
'''
class Student(object):
    def __init__(self, event,s3,bucket,user):
        self.username = user["email"]
        if "hd" in user:
            self.isWisconsin=True
        else:
            self.isWisconsin=False
        self.worksheetCode = event['worksheetCode']
        self.questionCode=None if event["fn"]!="addNewAnswer" else event["questionCode"]
        self.response = None if event["fn"]!="addNewAnswer" else event["response"]
        self.path = 'student/' + self.username + '.json'
        self.localTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.student={}
        self.s3=s3
        self.bucket=bucket

    '''
    get the student record or if new, initial one
    '''
    def getFile(self):
        try:
            self.student=self.s3.read_json_default(self.path, default={})  
        except:
            self.student = {"studentID":self.username,
                    "numberOfWorksheetAttempted":0
                    }

    '''
    check the answer and update the record
    '''
    def upload(self):
        errorCode,isCorrect=self.checkAnswer()
        if errorCode!=None or self.isWisconsin==False:
            return (errorCode,isCorrect)

        if self.worksheetCode not in self.student.keys():
            self.student["numberOfWorksheetAttempted"]+=1
            self.student[self.worksheetCode]={"questionsAttempted": 0,
                                "questionCorrectlyAttempted":0
                            }
            
        if self.questionCode not in self.student[self.worksheetCode].keys():
            self.student[self.worksheetCode][self.questionCode]={
                "numAttempts":    [-1, 0],
                "isCorrect":  False,
                "attempts":[]
            }
            self.student[self.worksheetCode]["questionsAttempted"]+=1

        self.student[self.worksheetCode][self.questionCode]["attempts"].append([self.localTime,self.response])
        self.student[self.worksheetCode][self.questionCode]["numAttempts"][1]+=1

        if isCorrect==True and self.student[self.worksheetCode][self.questionCode]["isCorrect"]==False:
            self.student[self.worksheetCode][self.questionCode]["numAttempts"][0]=self.student[self.worksheetCode][self.questionCode]["numAttempts"][1]
            self.student[self.worksheetCode][self.questionCode]["isCorrect"]=True
            self.student[self.worksheetCode]["questionCorrectlyAttempted"]+=1
        
        self.s3.put_object(Bucket=self.bucket,
                Key=self.path,
                Body=bytes(json.dumps(self.student, indent=2), 'utf-8'),
                ContentType='text/json')

    
        return (errorCode,isCorrect)

    '''This function is to check if the response of the student is correct
    If correct , return True, else return False
    If there is some error, it would return errorcode
    '''
    def checkAnswer(self):
        path="worksheets/answers/"+ self.worksheetCode+".json"
        try:
            self.worksheet=self.s3.read_json_default(path, default={})
        except:
            return ("Wrong WorksheetCode"+str(path),None)

        if self.questionCode not in self.worksheet.keys():
            return ("Wrong QuestionCode",None)

        if self.worksheet[self.questionCode]==self.response:
            return (None,True)
        else:
            return (None,False)

    '''
    get the record and reload it
    '''
    def reload(self):
        answerList={}        
        try:
            self.student=self.s3.read_json_default(self.path, default={})
        except:
            return (None,answerList)
        if self.worksheetCode not in self.student.keys():
            return ("Wrong WorksheetCode",answerList)

        for key in self.student[self.worksheetCode].keys():
            if key != "questionsAttempted" and key !="questionCorrectlyAttempted":
                answerList[key]=self.student[self.worksheetCode][key]["isCorrect"]

        return (None,answerList)

        
        
'''

pytutor/worksheets/report/worksheetcode.json
{
    WorksheetCode:"a",
    "attemptedBy":[student1, student2, ...] , //attempted at least 1 question
    "completedBy": [], //studentWho attempted all questions
    questions:{
                questionCode1:{
                numberOfStudentAttempted:
                numberOfStudentsCorrectlyAttmpted:
                averageNumOfAttemptsToCorrectlyAttempt:},
                questionCode2:{
                numberOfStudentAttempted:
                numberOfStudentsCorrectlyAttmpted:
                averageNumOfAttemptsToCorrectlyAttempt:}, ...
            }
}
'''    
class Report:
    def __init__(self,event,s3,bucket):
        self.worksheetCode = event['worksheetCode']
        self.path="pytutor/worksheets/report/"+self.worksheetCode+".json"  
        self.report={}
        self.s3=s3
        self.bucket=bucket


'''
get the report file or if new, initial one
'''
    def getFile(self):
        try:
            self.report=self.s3.read_json_default(self.path, default={})  
        except:
            self.report = {
                "WorksheetCode":self.worksheetCode,
                "attemptedBy":[] ,
                "completedBy": [],
                "questions":{}
            }
            try:
                worksheetPath="worksheets/answers/"+self.worksheetCode+".json"
                worksheet=self.s3.read_json_default(worksheetPath, default={})  
            except:
                return "Wrong WorksheetCode"
            for key in worksheet.keys():
                if key!= "worksheetCode" and key !="totalNumOfQuestions":
                    self.report["questions"][key]={"numberOfStudentAttempted":0,
                                        "numberOfStudentsCorrectlyAttmpted":0,
                                    "averageNumOfAttemptsToCorrectlyAttempt":0}
        return None

'''
update the report file
'''
    def updateReport(self,student,questionCode):
        if student["studentID"] not in self.report["attemptedBy"]:
            self.report["attemptedBy"].append(student["studentID"])

        if student[self.worksheetCode][questionCode]["numAttempts"][1]==1:
            self.report["questions"][questionCode]["numberOfStudentAttempted"]+=1

        if student[self.worksheetCode][questionCode]["numAttempts"][0]==student[self.worksheetCode][questionCode]["numAttempts"][1]:
            self.report["questions"][questionCode]["averageNumOfAttemptsToCorrectlyAttempt"]=\
                (self.report["questions"][questionCode]["averageNumOfAttemptsToCorrectlyAttempt"]*\
                self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+\
                student[self.worksheetCode][questionCode]["numAttempts"][0])/\
                (self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+1)
           
            self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+=1

            if student[self.worksheetCode]["questionCorrectlyAttempted"]==len(self.report["questions"]):
                self.report["completedBy"].append(student["studentID"])

        self.s3.put_object(Bucket=self.bucket,
                Key=self.path,
                Body=bytes(json.dumps(self.report, indent=2), 'utf-8'),
                ContentType='text/json')

        return 0

'''
reload the report file
'''
    def getReport(self):
        del self.report["WorksheetCode"]
        return self.report
