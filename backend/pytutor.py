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

import json, random, time

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


#dict_ID = {}

@route
@user
def pytutor_test(user, event):
        path = 'pytutor/dev-test.json'
        count = s3().read_json_default(path, default=1)
        s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(count+1, indent=2), 'utf-8'),
                    ContentType='text/json')
        return (200, "called %d times" % count)

@route
@user
def addNewAnswer(user,event):
        '''Records answers using student ID as key and sections with answers as values.
       Ideally would give a list of the questions each person answered correctly.
       example: {studentID: {A: [Q1, ..., Qn], B: ... } } '''
        username=user['email']
        questionCode = event['questionCode']
        activityNum = questionCode.strip()[4:6]
        questionNum = questionCode.strip()[-4:-2]
        answerDict = {}
        questionList = []
        path = 'pytutor/data.json'
        data = s3().read_json_default(path, default={})
        #return (200, "%s" % data)
#        with open('data.txt') as json_file:
#               data = json.load(json_file)
        if username not in data:
                data[username]={activityNum:[questionNum]}
        else:
                if activityNum not in data[username]:
                        data[username][activityNum] = [questionNum]
                else:
                        data[username][activityNum].append(questionNum)

        '''dict_ID[username] = answerDict
        for section in answerDict:
            answerDict[activityNum] = questionList.append(questionNum)'''
        s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(data, indent=2), 'utf-8'),
                    ContentType='text/json')
 
#        with open('data.txt', 'w') as outfile:
#                json.dump(data, outfile)
        return (200,"success")

@route
@user
def isAnswered(user,event):
        '''Records answers using student ID as key and sections with answers as values.
       Ideally would give a list of the questions each person answered correctly.
       example: {studentID: {A: [Q1, ..., Qn], B: ... } } '''
        username=user['email']
        questionCode = event['questionCode']
        activityNum = questionCode.strip()[4:6]
        questionNum = questionCode.strip()[-4:-2]
        answerDict = {}
        questionList = []
        path = 'pytutor/data.json'
        data = s3().read_json_default(path, default={})
        #return (200, "%s" % data)
#        with open('data.txt') as json_file:
#               data = json.load(json_file)
        if username not in data:
                return(200,"false")
                #data[username]={activityNum:[questionNum]}
        else:
                if activityNum not in data[username]:
                        return(200,"false")
                        #data[username][activityNum] = [questionNum]
                else:
                    if questionNum in data[username][activityNum]:
                        return (200, questionCode)
        return (200, "false")

#def deadlineFx():
#'''Checks for deadline errors'''
@route
@user
def feedback(studentTime, deadline):
        '''Worked, we put this in Json File, Try/Except on time/deadline,
       ask for data for a particular students data and form it as a string'''
        if studentTime <= deadline:
                return True
        else:
                strDeadline = (str(studentTime) + ' is past the deadline')
        return(False)

