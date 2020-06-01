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


'''
The data structure of student
    {
        "studentID":id,
        submissionTime1:{
            "courseID":"a"
            "correctAnswers"=[Q1,...,Qn]
        },
        submissionTime2{
            "courseID":"b"
            "correctAnswers"=[Q1,...,Qn]
        }
    }
while each submission, the data in the report would change. 
data structure of the report
    {
        "a":{
            "submissionN": 55 #this is the total number of submission for this course
            "correctTime":{
                "Q1":42,
                ...
                "Qn":33,
            },
        "b":{
            ...
        }
        }
    }
'''
@route
@user
def addNewAnswer(user,event):
        '''Records answers using student ID as key and sections with answers as values.
       Ideally would give a list of the questions each person answered correctly.
       example: {studentID: {A: [Q1, ..., Qn], B: ... } } '''
       '''change the data structure into each student a separated file,
       example:{"studentID":id,"submissionTime":{"courseID":A,"correctAnswers":[]}
       '''
        username=user['email']
        questionCode = event['questionCode']
        activityNum = questionCode.strip()[4:6]
        questionNum = questionCode.strip()[-4:-2]
        answerDict = {}
        questionList = []
        submissionTime=event['submissionTime']
        path = 'pytutor/student/'+username+'.json'
        try:
            data = s3().read_json_default(path, default={})
        except:
            data={"studentID":username}
            with open("./templete.json",'w') as f:
                f.write(json.dumps(data, indent=2)
            with open("./templete.json",'rb')as f:
                s3.upload_fileobj(f,BUCKET,path)
        report=s3().read_json_default("report.json", default={})
        if submissionTime not in data:
            data[submissionTime]={
                'courseID':activityNum,
                'correctQ'=[]
            }
            if activityNum not in report:
                report[activityNum]={
                        "submissionN":0,
                        "correctTime":{}
                }
            report[activityNum]["submissionN"]=report[activityNum]["submissionN"]+1
        if questionCode not in report[activityNum]['correctTime']:
            report[activityNum]['correctTime'][questions]=1
        else:
            report[activityNum]['correctTime'][questions]=report[activityNum]['correctTime'][questions]+1
        data[submissionTime]['correctQ'].append(questionCode)
        s3.put_object(Bucket=Bucket,Key="report.json",Body=bytes(json.dumps(report,indent=2),'utf-8'),ContentType='text/json')
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
        submissionTime=event['submissionTime']

        path = 'pytutor/student/'+username+'.json'
        try:
            data = s3().read_json_default(path, default={})
        expect:
            return(200,"false")
        #return (200, "%s" % data)
        '''
        with open('data.txt') as json_file:
               data = json.load(json_file)
        if username not in data:
                return(200,"false")
                #data[username]={activityNum:[questionNum]}
       else:
 '''

        for key in data.keys():
            if key!='studentID':
                if data[key]['courseID']==activityNum:
                    if questionNum in data[key][correctQ]:
                        return (200,questionCode)

        return (200,"false")


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

'''
After input the userID, the getTimeLog would return the timelog like
{
	submissionTime1: courseID,
	submissionTime2: courseID,
	....
}
'''

@route
@user
def getTimeLog(user):
    username=user['email']
    path = 'pytutor/student/'+username+'.json'
	try:
		data = s3().read_json_default(path, default={})
	except:
		return (200,"")
	timelog={}
	for key in data.keys():
		if key != "studentID":
			timelog[key]=data[key]["courseID"]
	timelogJson=json.dumps(timelog,indent=2)
	return (200,timelogJson)

'''
The detail would like
	{
        "courseID":"a",
        "correctAnswers"=[Q1,...,Qn],
        "Time":submissionTime
        }
'''
@route
@user
def getDetail(user,event):
	username=user['email']
    submissionTime=event['submissionTime']
    path = 'pytutor/student/'+username+'.json'
    try:
        data = s3().read_json_default(path, default={})
        detail=data[submissionTime]
        detail["Time"]=submissionTime
        return (200,json.dumps(detail,indent=2))
    except:
    	return (200,{})
