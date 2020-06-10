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

from lambda_framework import *

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

@route
@user
def pytutor_test(user, event):
        path = 'pytutor/dev-test.json'
        count = s3().read_json_default(path, default=1)
        s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(count + 1, indent=2), 'utf-8'),
                    ContentType='text/json')
        return (200, "called %d times" % count)



'''This function is to check if the response of the student is correct
    If correct , return True, else return False
    If there is some error, it would return errorcode
    '''
def checkAnswer(worksheetCode,questionCode,response):
    path="pytutor/worksheets/answers/"+ worksheetCode+".json"
    try:
        worksheet=s3().read_json_default(path, default={})
    except:
        return ("Wrong WorksheetCode",null)

    if questionCode not in worksheet.keys():
        return ("Wrong QuestionCode",null)

    if worksheet[questionCode]==response:
        return (null,True)
    else:
        return (null,False)


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
    username = event["netId"]
    worksheetCode = event['worksheetCode']
    questionCode=event["questionCode"]
    response = event["response"]
    path = 'pytutor/student/' + username + '.json'
    localTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result={
        "statusCode": 200,
        "success": True,
        "errorCode": "NoError",
        "fnExecuted":"addNewAnswer",
        "isCorrect": []   
    }
    errorCode,isCorrect=checkAnswer(worksheetCode,questionCode,response)
    if errorCode!=null:
        result["success"]=False
        result["errorCode"]=errorCode
        return result

    try:
        sturdent=s3().read_json_default(path, default={})   
    except:
        student = {"studentID":username,
                    "numberOfWorksheetAttempted":0
                    }
        with open("./templete.json", 'w') as f:
            f.write(json.dumps(student, indent=2)

        with open("./templete.json", 'rb') as f:
            s3.upload_fileobj(f, BUCKET, path)

    if worksheetCode not in student.keys():
        student["numberOfWorksheetAttempted"]+=1
        student[worksheetCode]={"questionsAttempted": 0,
                                "questionCorrectlyAttempted":0
                            }
            
    if questionCode not is student[worksheetCode].keys():
        student[worksheetCode][questionCode]={
            "numAttempts":    [-1, 0]
            "isCorrect":  False
            "attempts":[]
        }
        student[worksheetCode]["questionsAttempted"]+=1

    student[worksheetCode][questionCode]["attempts"].append([localTime,response])
    student[worksheetCode][questionCode]["numAttempts"][1]+=1

    if isCorrect==True and student[worksheetCode][questionCode]["isCorrect"]==False:
        student[worksheetCode][questionCode]["numAttempts"][0]=student[worksheetCode][questionCode]["numAttempts"][1]
        student[worksheetCode][questionCode]["isCorrect"]=True
        student[worksheetCode]["questionCorrectlyAttempted"]+=1
        
    s3().put_object(Bucket=BUCKET,
                Key=path,
                Body=bytes(json.dumps(data, indent=2), 'utf-8'),
                ContentType='text/json')

    result["isCorrect"].append({
                        "questionCode":questionCode,
                        "isCorrect":isCorrect
                    })
    return result
'''

'''
This function is to reload the record of one worksheet of the user
'''
@route
@user
def reload(user, event):
    username = event["netId"]
    worksheetCode = event['worksheetCode']
    path = 'pytutor/student/' + username + '.json'
    result={
        "statusCode": 200,
        "success": True,
        "errorCode": "NoError",
        "fnExecuted":"reload",
        "isCorrect": []   
    }
    try:
        sturdent=s3().read_json_default(path, default={})
    except:
        result["success"]=False
        result["errorCode"]="Wrong User"
        return result
    if worksheetCode not in student.keys():
        result["success"]=False
        result["errorCode"]="Wrong WorksheetCode"
        return result

    for key in student[worksheetCode].keys():
        if key != "questionsAttempted" and key !="questionCorrectlyAttempted":
            result["isCorrect"].append({"questionCode":key,
                                        "isCorrect":student[worksheetCode][key]["isCorrect"]})

    return result


class Student(object):
    def __init__(event,s3,bucket):
        self.username = event["netId"]
        self.worksheetCode = event['worksheetCode']
        self.questionCode=event["questionCode"]
        self.response = event["response"]
        self.path = 'pytutor/student/' + self.username + '.json'
        self.localTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.result={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
        }
        self.student={}
        self.s3=s3
        self.bucket=bucket

    def getFile(self):
        try:
            self.sturdent=s3().read_json_default(path, default={})   
        except:
            self.student = {"studentID":username,
                    "numberOfWorksheetAttempted":0
                    }
         '''
            with open("./templete.json", 'w') as f:
                f.write(json.dumps(self.student, indent=2)

            with open("./templete.json", 'rb') as f:
                s3.upload_fileobj(f, BUCKET, path)
        '''

    def upload(self):
        errorCode,isCorrect=self.checkAnswer()
        if errorCode!=null:
            result["success"]=False
            result["errorCode"]=errorCode
            return result
        if self.worksheetCode not in self.student.keys():
            self.student["numberOfWorksheetAttempted"]+=1
            self.student[self.worksheetCode]={"questionsAttempted": 0,
                                "questionCorrectlyAttempted":0
                            }
            
        if self.questionCode not is self.student[self.worksheetCode].keys():
            self.student[self.worksheetCode][self.questionCode]={
                "numAttempts":    [-1, 0]
                "isCorrect":  False
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
                Key=path,
                Body=bytes(json.dumps(data, indent=2), 'utf-8'),
                ContentType='text/json')

        self.result["isCorrect"].append({
                        "questionCode":self.questionCode,
                        "isCorrect":self.isCorrect
                    })
        return result

    '''This function is to check if the response of the student is correct
    If correct , return True, else return False
    If there is some error, it would return errorcode
    '''
    def checkAnswer(self):
        path="pytutor/worksheets/answers/"+ self.worksheetCode+".json"
        try:
            self.worksheet=self.s3.read_json_default(path, default={})
        except:
            return ("Wrong WorksheetCode",null)

        if self.questionCode not in self.worksheet.keys():
            return ("Wrong QuestionCode",null)

        if self.worksheet[questionCode]==response:
            return (null,True)
        else:
            return (null,False)
