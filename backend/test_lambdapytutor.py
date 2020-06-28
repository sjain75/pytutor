from moto import mock_s3
from lambda_pytutor import *
import boto3
import json


BUCKET="bucket"

def read_json_default(s3_client,path):
    response=s3.get_object(Bucket=BUCKET, Key=path)
    return json.loads(response['Body'].read().decode('utf-8'))

def set_up():
    mock = mock_s3()
    mock.start()
    resource = boto3.resource(
                        's3',
                         aws_access_key_id= "123",
                         aws_secret_access_key= "123" )
    resource.create_bucket(Bucket="bucket")
    s3 = boto3.client(
                's3',
                aws_access_key_id="123",
                aws_secret_access_key="123")
    testWorkSheet={
    "worksheetCode": "testWorkSheet",
    "totalNumOfQuestions":  4,  
    "q1": "A",
    "q2": "B",
    "q3": "C",
    "q4": 5
    }
    s3.put_object(Bucket="bucket",
        Key="worksheets/answers/testWorkSheet.json",
        Body=bytes(json.dumps(testWorkSheet, indent=2), 'utf-8'),
        ContentType='text/json')
    return s3

def test_addNewAnswer_1():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    result=addNewAnswer(user,event)

    assert result=={
            "fnExecuted":"addNewAnswer",
            "isCorrect": [
                    {"questionCode":"q1",
                    "isCorrect":True}]}
    student=read_json_default(s3,"student/xcai67@wisc.edu.json")
    print(student)
    assert student["studentID"]=="xcai67@wisc.edu"
    assert student["numberOfWorksheetAttempted"]==1
    assert student["testWorkSheet"]["questionsAttempted"]==1
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==1
    assert student["testWorkSheet"]["q1"]["numAttempts"]==[1,1]
    assert student["testWorkSheet"]["q1"]["isCorrect"]==True
    assert len(student["testWorkSheet"]["q1"]["attempts"])==1


def test_addNewAnswer_2():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q2",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    result=addNewAnswer(user,event)

    assert result=={
            "fnExecuted":"addNewAnswer",
            "isCorrect": [
                    {"questionCode":"q2",
                    "isCorrect":False}]  
        }
    student=read_json_default(s3,"student/xcai67@wisc.edu.json")    
    print(student["testWorkSheet"])
    assert student["studentID"]=="xcai67@wisc.edu"
    assert student["numberOfWorksheetAttempted"]==1
    assert student["testWorkSheet"]["questionsAttempted"]==1
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==0
    assert student["testWorkSheet"]["q2"]["numAttempts"]==[-1,1]
    assert student["testWorkSheet"]["q2"]["isCorrect"]==False
    assert len(student["testWorkSheet"]["q2"]["attempts"])==1

def test_addNewAnswer_3():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    event["response"]="A"
    addNewAnswer(user,event)
    student=read_json_default(s3,"student/xcai67@wisc.edu.json")    
    assert student["testWorkSheet"]["q1"]["numAttempts"] == [2,2]
    assert student["testWorkSheet"]["q1"]["isCorrect"]==True
    assert len(student["testWorkSheet"]["q1"]["attempts"])==2
    addNewAnswer(user,event)
    student=read_json_default(s3,"student/xcai67@wisc.edu.json")    
    assert student["testWorkSheet"]["q1"]["numAttempts"]==[2,3]
    assert len(student["testWorkSheet"]["q1"]["attempts"])==3

    event["questionCode"]="q2"
    event["response"]="B"
    addNewAnswer(user,event)
    student=read_json_default(s3,"student/xcai67@wisc.edu.json")    
    assert student["testWorkSheet"]["questionsAttempted"]==2
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==2

def test_addNewAnswer_4():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWrongWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    result=addNewAnswer(user,event)
    assert result=={
            "errorCode": "Wrong WorksheetCode",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
    }
    event["worksheetCode"]="testWorkSheet"
    event["questionCode"]="wrongQuestionCode"
    result=addNewAnswer(user,event)
    assert result=={
            "errorCode": "Wrong QuestionCode",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []
    }

def test_reload_1():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "reload",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    result=reload(user,event)
    assert result=={
            "fnExecuted":"reload",
            "isCorrect": []
    }
    
def test_reload_2():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    event["fn"]="reload"
    event["worksheetCode"]="wrong WorksheetCode"
    result=reload(user,event)
    assert result=={
            "errorCode": "Wrong WorksheetCode",
            "fnExecuted":"reload",
            "isCorrect": [] 
    }

def test_reload_3():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    event["questionCode"]="q2"
    addNewAnswer(user,event)
    event["fn"]="reload"
    result=reload(user,event)
    assert result=={
            "fnExecuted":"reload",
            "isCorrect": [{"questionCode":"q1",
                            "isCorrect":True},
                            {"questionCode":"q2",
                            "isCorrect":False}],
            }

def test_report_1():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["WorksheetCode"]=="testWorkSheet"
    assert report["attemptedBy"]==["xcai67@wisc.edu"]
    assert report["completedBy"]==[]
    assert report["questions"]["q1"]=={
                "numberOfStudentAttempted":1,
                "numberOfStudentsCorrectlyAttmpted" :1,
                "averageNumOfAttemptsToCorrectlyAttempt":1}

def test_report_2():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    user["email"]="xliu89@wisc.edu"
    addNewAnswer(user,event)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["attemptedBy"]==["xcai67@wisc.edu","xliu89@wisc.edu"]
    assert report["questions"]["q1"]=={
                "numberOfStudentAttempted":2,
                "numberOfStudentsCorrectlyAttmpted":2,
                "averageNumOfAttemptsToCorrectlyAttempt":1}

def test_report_3():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    event["questionCode"]="q2"
    event["response"]="B"
    addNewAnswer(user,event)
    event["questionCode"]="q3"
    event["response"]="C"
    addNewAnswer(user,event)
    event["questionCode"]="q4"
    event["response"]=5
    addNewAnswer(user,event)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["completedBy"]==["xcai67@wisc.edu"]

def test_getReport_1():
    s3=set_up()
    def s3():
        return s3
    event={
        "fn": "addNewAnswer",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    user={
        "email":"xcai67@wisc.edu",
        "hd":"wisc.edu"
    }
    addNewAnswer(user,event)
    event["fn"]="getReport"
    report=getReport(user,event)
    assert len(report["report"]["questions"])==4
