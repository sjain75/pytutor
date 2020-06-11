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

# from lambda_framework import *

# #!/usr/bin/env python
# import cgitb
# cgitb.enable()
# #from flask import Flask, escape, request
# import json
# try:
#         task = requests.GET('task')
# except:
#         print("task was not completed!")
# if(task=="newAnswer"):
#         username = requests.GET('netID')
#         questionCode = requests.GET('questionCode')
#         activityNum = questionCode.strip()[4:6]
#         questionNum = questionCode.strip()[-4:-2]
#         addNewAnswer(username, activityNum, questionNum)
#         return json.dumps(True)
# elif(task=="studentResults"):
#         username = requests.POST['username']
# else:
#         return json.dumps(False)


# dict_ID = {}

def pytutor_test(user, event):
        path = 'pytutor/dev-test.json'
        count = s3().read_json_default(path, default=1)
        s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(count + 1, indent=2), 'utf-8'),
                    ContentType='text/json')
        return (200, "called %d times" % count)


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
    student=Student(event,s3(),BUCKET)
    student.getFile()
    return student.upload()

'''
This function is to reload the record of one worksheet of the user
'''
@route
@user
def reload(user, event):
    student=Student(event,s3(),BUCKET)
    return student.reload()

@route
@user
def isAnswered(user,event):
    student=Student(event,s3(),BUCKET)
    return student.isAnswered()

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
        result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
        }
        errorCode,isCorrect=self.checkAnswer()
        if errorCode!=None:
            result["success"]=False
            result["errorCode"]=errorCode
            return result
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

        result["isCorrect"].append({
                    "questionCode":self.questionCode,
                    "isCorrect":isCorrect
                    })
        return result

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
        result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"reload",
            "isCorrect": []   
        }
        try:
            self.student=self.s3.read_json_default(self.path, default={})
        except:
            return result
        if self.worksheetCode not in self.student.keys():
            result["success"]=False
            result["errorCode"]="Wrong WorksheetCode"
            return result

        for key in self.student[self.worksheetCode].keys():
            if key != "questionsAttempted" and key !="questionCorrectlyAttempted":
                result["isCorrect"].append({"questionCode":key,
                                        "isCorrect":self.student[self.worksheetCode][key]["isCorrect"]})

        return result

    def isAnswered(self):
        result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"isAnswered",
            "isCorrect": []   
        }
        try:
            path="worksheets/answers/"+ self.worksheetCode+".json"
            self.worksheet=self.s3.read_json_default(path, default={})
        except:
            result["success"]=False
            result["errorCode"]="Wrong WorksheetCode"
            return result
        questionList=[]
        for key in self.worksheet.keys():
            if key!="worksheetCode" and key!="totalNumOfQuestions":
                questionList.append(key)
            
        try:
            self.student=self.s3.read_json_default(self.path, default={})
            thisWorksheet=self.student[self.worksheetCode]
        except:
            for key in questionList:
                result["isCorrect"].append({"questionCode":key,
                    "isCorrect":False})
            return result

        for key in questionList:
            if key not in thisWorksheet.keys():
                result["isCorrect"].append({"questionCode":key,
                    "isCorrect":False})
            else if thisWorksheet[key]["isCorrect"]==False:
                result["isCorrect"].append({"questionCode":key,
                    "isCorrect":False})
            else:
                result["isCorrect"].append({"questionCode":key,
                    "isCorrect":True})
        return result

