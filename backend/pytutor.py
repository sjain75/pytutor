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


'''
The data structure of student
    {
        "studentID":id,
        "numberOfWorksheet":n,
        "numberOfSubmission":n,
        "a":{
            "submissionTime":m,
            "lastGrade":n,
            "wrongA":[], #this is the answer which is not correct till now
            submissionTime1:{
                "grade":"10/20",
                "wrongQ":["Q1","Q3",..."Qn"]
                "totalTime":xxx
            },
            submissionTime2{
                ...
            }
        "b":{
            .....
        }
    }
while each submission, the data in the report would change.
data structure of the report
    {
        "a":{
            "submissionN": 55 #this is the total number of submission for this course
            # the first else is the number of students have done this worksheet
            "submissionS":[30,29,28...]
                                        # The following element is the number of students get the correct answer of each question
            "averageFGrade":10 #this is the average grade of the first attempt of the worksheet
            "averageLGrade":20 #this is the average grade of the last attempt of the worksheet
            "fullGrade":20 #this is the full mark of the worksheet
            "averageFirstCorrect":{
                "Q1":5,
                ...
                "Qn":10,
            },#this should be the average attempt to make each question correct
        "b":{
            ...
        }
        }
    }
'''


@route
@user
def addNewAnswer(user, event):
        # this should be a unique identity of the user, maybe its email
        username = event['user']
        worksheet = event['worksheetNo']  # This is the worksheet No.
        time = event['timelog']
        '''this would be a dict contains the time when students begin answer the worksheet and
        the time used for each question
        for example
        {
            "beginTime":xxxx,
            "totalTime":xxxx,(I would only use these two info)
            other info
        }'''
        response = event["response"]
        '''
        this should be a dict contains the answer the students made
        which is similar to the correct answer
        for example
        {
            "Q1":xxx,
            "Q2":xxx,
            ...
            "Qn":xxx
        }
        '''
        path = 'pytutor/student/' + username + '.json'
        answer = s3().read_json_default(worksheet + ".json", default={})

        report = s3().read_json_default("report.json", default={})
        if worksheet not in report.keys():
            report[worksheet] = {
                "submissionN": 0
                "submissionS": [0]
                # this is the number of students have done this woeksheet
                "averageFGrade": 0
                # the average grade of the first attempt of the worksheet
                "averageLGrade": 0
                # the average grade of the last attempt of the worksheet
                "fullGrade": len(response)
                "averageFirstCorrect": {}
            }
            for key in response.keys():
                report[worksheet]["averageFirstCorrect"][key] = 0
                report[worksheet]["submissionS"].append(0)

        report[worksheet][submissionN] += 1

        try:
            data = s3().read_json_default(path, default={})
        except:
            data = {"studentID": username,
                    "numberOfWorksheet": 0,
                    "numberOfSubmission": 0
                    }
            with open("./templete.json", 'w') as f:
                f.write(json.dumps(data, indent=2)

            with open("./templete.json", 'rb') as f:
                s3.upload_fileobj(f, BUCKET, path)


        data["numberOfSubmission"] += 1
        if worksheet not in data.keys():
            data["numberOfSubmission"] += 1
            data[worksheet]={"submissionTime": 0,
                                "lastGrade": null,
                                "wrongA": []
                            }
            for key in response.keys():
                data[worksheet]["wrongA"].append(key)


        fullGrade=len(response)
        grade=0
        wrongAnswer=[]
        i=0
        for key in response.keys:
            i += 1
            if response[key] == answer[key]:
                grade += 1
                if key in data[worksheet]["wrongA"]:
                    data[worksheet]["wrongA"].remove(key)
                    report[worksheet]["averageFirstCorrect"][key]=(report[worksheet]["averageFirstCorrect"][key] * report[worksheet]["submissionS"][i] +
                        len(data[worksheet]) - 2) / (report[worksheet]["submissionS"][i] + 1)
                report[worksheet]["submissionS"][i] += 1
            else:
                wrongAnswer.append(key)
        # To calculate the grade



        if len(data[worksheet]) == 3:
            # only if is it the first attempt of this worksheet, length is 3
            report[worksheet]["averageFGrade"]=(report[worksheet]["averageFGrade"] * report[worksheet]["submissionS"][0] +\
                grade) / (report[worksheet]["submissionS"][0] + 1)
            report[worksheet]["submissionS"][0] += 1


        report[worksheet]["averageLGrade"]=(report[worksheet]["averageLGrade"] * (report[worksheet]["submissionS"][0] - 1) +\
                grade) / (report[worksheet]["submissionS"][0])
        # update the report info

        data[worksheet]["submissionTime"] += 1
        data[worksheet]["lastGrade"]=str(grade) + "/" + str(fullGrade)
        data[worksheet][timelog["beginTime"]]={
            "grade": str(grade) + "/" + str(fullGrade),
            "wrongQ": wrongAnswer,
            "totalTime": timelog["totalTime"]
        }
        s3().put_object(Bucket=BUCKET,
                    Key=path,
                    Body=bytes(json.dumps(data, indent=2), 'utf-8'),
                    ContentType='text/json')

        s3().put_object(Bucket=BUCKET,
                    Key="report.json",
                    Body=bytes(json.dumps(report, indent=2), 'utf-8'),
                    ContentType='text/json')

        return (200,"success")




# def deadlineFx():
#'''Checks for deadline errors'''
@ route
@ user
def feedback(studentTime, deadline):
        '''Worked, we put this in Json File, Try/Except on time/deadline,
       ask for data for a particular students data and form it as a string'''
        if studentTime <= deadline:
                return True
        else:
                strDeadline=(str(studentTime) + ' is past the deadline')
        return(False)






'''
After input the userID, the getTimeLog would return the timelog like
{
    courseID:{
        "totalSubmission"
    }
    ....
}
'''
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



The detail would like
    {
        "courseID":"a",
        "correctAnswers"=[Q1,...,Qn],
        "Time":submissionTime
        }


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
'''