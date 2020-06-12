# Copyright 2018 Tyler Caraza-Harter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random
import time


'''
structure of student record
{
    "studentID":id,
    "numberOfWorksheetAttempted":2,
    "WorksheetCode1":{
        questionsAttempted: ,
        questionCorrectlyAttempted: ,
        q1:{
            numAttempts:    [numAttemptsTIllCorrect, totalNumAttempts]
            isCorrect:  False/True #once they have correctly attempted becomes True,
                                                else False
            attemts:[
                        [timeStamp, attemptedAnswer],
                        [timeStamp, attemptedAnswer],
                        [timeStamp, attemptedAnswer]                                
                    ]
            },
        q2:{
                 ...
            },
                   
            ....
        }
    "WorksheetCode2":{
            .....
        }
    } 
'''
'''
TODO: add report function
'''
@route
@user
def addNewAnswer(user, event):
    result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
        }
    student=Student(event,s3(),BUCKET)
    student.getFile()
    errorCode,isCorrect=student.upload()
    if errorCode!=None:
        result["success"]=False
        result["errorCode"]=errorCode
        return result
    result["isCorrect"].append({
                    "questionCode":student.questionCode,
                    "isCorrect":isCorrect
                    })
    report=Report(event,s3(),BUCKET)
    report.getFile()
    report.upload(student.student,student.questionCode)
    return result

'''
This function is to reload the record of one worksheet of the user
'''
@route
@user
def reload(user, event):
    result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"reload",
            "isCorrect": []   
        }
    student=Student(event,s3(),BUCKET)
    errorCode,answerList= student.reload()
    if errorCode!=None:
        result["success"]=False
        result["errorCode"]=errorCode
        return result
    result["isCorrect"]=answerList
    return result

'''
This function is to reload the report
'''
@route
@user
def getReport(user,event):
    result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"getReport",
            "report":{}
        }
    report=Report(event)
    errorCode=report.getFile()
    if errorCode!=None:
        result["success"]=False
        result["errorCode"]=errorCode
        return result

    result["report"]=report.getReport()
    return result

class Student(object):
    def __init__(self, event,s3,bucket):
        self.username = event["netId"]
        self.worksheetCode = event['worksheetCode']
        self.questionCode=event["questionCode"]
        self.response = event["response"]
        self.path = 'student/' + self.username + '.json'
        self.localTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.student={}
        self.s3=s3
        self.bucket=bucket

    def getFile(self):
        try:
            self.student=(self.s3).read_json_default(self.path, default={})  
        except:
            self.student = {"studentID":self.username,
                    "numberOfWorksheetAttempted":0
                    }


    def upload(self):
       
        errorCode,isCorrect=self.checkAnswer()
        if errorCode!=None:
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
    example of answer :
    {
    worksheetCode: [WorksheetCode],
    totalNumOfQuestions:  #,    
    q1:Answer,
    q2:Answer,
    ...
    }
    '''
    def checkAnswer(self):
        path="worksheets/answers/"+ self.worksheetCode+".json"
        try:
            self.worksheet=self.s3.read_json_default(path, default={})
        except:
            return ("Wrong WorksheetCode",None)

        if self.questionCode not in self.worksheet.keys():
            return ("Wrong QuestionCode",None)

        if self.worksheet[self.questionCode]==self.response:
            return (None,True)
        else:
            return (None,False)

    def reload(self):
        answerList=[]        
        try:
            self.student=self.s3.read_json_default(self.path, default={})
        except:
            return (None,answerList)
        if self.worksheetCode not in self.student.keys():
            return ("Wrong WorksheetCode",anwerList)

        for key in self.student[self.worksheetCode].keys():
            if key != "questionsAttempted" and key !="questionCorrectlyAttempted":
                answerList.append({"questionCode":key,
                                        "isCorrect":self.student[self.worksheetCode][key]["isCorrect"]})

        return (None,answerList)

'''
//NewReportForEveryWorksheet
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


    def getFile(self):
        try:
            self.report=(self.s3).read_json_default(self.path, default={})  
        except:
            self.report = {
                "WorksheetCode":self.worksheetcode,
                "attemptedBy":[] , //attempted at least 1 question
                "completedBy": [], //studentWho attempted all questions
                "questions":{}
            }
            try:
                worksheetPath="worksheets/answers/"+self.worksheetCode+".json"
                worksheet=(self.s3).read_json_default(worksheetPath, default={})  
            except:
                return "Wrong WorksheetCode"
            for key in worksheet.keys():
                if key!= "worksheetCode" and key !="totalNumOfQuestions":
                    self.report["questions"][key]={"numberOfStudentAttempted":0,
                                        "numberOfStudentsCorrectlyAttmpted":0,
                                    "averageNumOfAttemptsToCorrectlyAttempt":0}
        return None

    def updateReport(self,student,questionCode):
        if student["studentID"] not in self.report["attemptedBy"]:
            self.report["attemptedBy"].append(student["studentID"])

        if student["worksheetCode"][questionCode]["numAttempts"][1]==1:
            self.report[questions][questionCode]["numberOfStudentAttempted"]+=1

        if student["worksheetCode"][questionCode]["numAttempts"][0]==student["worksheetCode"][questionCode]["numAttempts"][1]:
            self.report["questions"][questionCode]["averageNumOfAttemptsToCorrectlyAttempt"]=\
                (self.report["questions"][questionCode]["averageNumOfAttemptsToCorrectlyAttempt"]*\
                self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+\
                student["worksheetCode"][questionCode]["numAttempts"][0])/\
                (self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+1)
           
            self.report["questions"][questionCode]["numberOfStudentsCorrectlyAttmpted"]+=1

            if student["worksheetCode"]["questionCorrectlyAttempted"]==len(self.report["questions"]):
                self.report["completedBy"].append(student["studentID"])

        self.s3.put_object(Bucket=self.bucket,
                Key=self.path,
                Body=bytes(json.dumps(self.report, indent=2), 'utf-8'),
                ContentType='text/json')

        return 0


    def getReport(self):
        del self.report["worksheetCode"]
        return self.report
