from moto import mock_s3
from pytutor import *
import boto3
import json


BUCKET="bucket"

def read_json_default(s3,path):
        try :
            response=s3.get_object(Bucket=BUCKET, Key=path)
            return json.loads(response['Body'].read().decode('utf-8'))
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "NoSuchKey":
                return default
            raise e

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
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    result=addNewAnswer("",event,s3)

    assert result=={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"addNewAnswer",
            "isCorrect": [
                    {"questionCode":"q1",
                    "isCorrect":True}]}
    student=read_json_default(s3,"student/xcai67.json")
    print(student)
    assert student["studentID"]=="xcai67"
    assert student["numberOfWorksheetAttempted"]==1
    assert student["testWorkSheet"]["questionsAttempted"]==1
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==1
    assert student["testWorkSheet"]["q1"]["numAttempts"]==[1,1]
    assert student["testWorkSheet"]["q1"]["isCorrect"]==True
    assert len(student["testWorkSheet"]["q1"]["attempts"])==1


def test_addNewAnswer_2():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q2",
        "response":"A"
    }
    result=addNewAnswer("",event,s3)

    assert result=={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"addNewAnswer",
            "isCorrect": [
                    {"questionCode":"q2",
                    "isCorrect":False}]   
        }
    student=read_json_default(s3,"student/xcai67.json")    
    print(student["testWorkSheet"])
    assert student["studentID"]=="xcai67"
    assert student["numberOfWorksheetAttempted"]==1
    assert student["testWorkSheet"]["questionsAttempted"]==1
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==0
    assert student["testWorkSheet"]["q2"]["numAttempts"]==[-1,1]
    assert student["testWorkSheet"]["q2"]["isCorrect"]==False
    assert len(student["testWorkSheet"]["q2"]["attempts"])==1

def test_addNewAnswer_3():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    addNewAnswer("",event,s3)
    event["response"]="A"
    addNewAnswer("",event,s3)
    student=read_json_default(s3,"student/xcai67.json")    
    assert student["testWorkSheet"]["q1"]["numAttempts"] == [2,2]
    assert student["testWorkSheet"]["q1"]["isCorrect"]==True
    assert len(student["testWorkSheet"]["q1"]["attempts"])==2
    addNewAnswer("",event,s3)
    student=read_json_default(s3,"student/xcai67.json")    
    assert student["testWorkSheet"]["q1"]["numAttempts"]==[2,3]
    assert len(student["testWorkSheet"]["q1"]["attempts"])==3

    event["questionCode"]="q2"
    event["response"]="B"
    addNewAnswer("",event,s3)
    student=read_json_default(s3,"student/xcai67.json")    
    assert student["testWorkSheet"]["questionsAttempted"]==2
    assert student["testWorkSheet"]["questionCorrectlyAttempted"]==2

def test_addNewAnswer_4():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWrongWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    result=addNewAnswer("",event,s3)
    assert result=={
            "statusCode": 200,
            "success": False,
            "errorCode": "Wrong WorksheetCode",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
    }
    event["worksheetCode"]="testWorkSheet"
    event["questionCode"]="wrongQuestionCode"
    result=addNewAnswer("",event,s3)
    assert result=={
            "statusCode": 200,
            "success": False,
            "errorCode": "Wrong QuestionCode",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
    }

def test_reload_1():
    s3=set_up()
    event={
        "fn": "reload",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    result=reload("",event,s3)
    assert result=={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"reload",
            "isCorrect": []   
    }
    
def test_reload_2():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"B"
    }
    addNewAnswer("",event,s3)
    event["fn"]="reload"
    event["worksheetCode"]="wrong WorksheetCode"
    result=reload("",event,s3)
    assert result=={
            "statusCode": 200,
            "success": False,
            "errorCode": "Wrong WorksheetCode",
            "fnExecuted":"reload",
            "isCorrect": []   
    }

def test_reload_3():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    addNewAnswer("",event,s3)
    event["questionCode"]="q2"
    addNewAnswer("",event,s3)
    event["fn"]="reload"
    result=reload("",event,s3)
    assert result=={
            "statusCode": 200,
            "success": True,
            "errorCode": "NoError",
            "fnExecuted":"reload",
            "isCorrect": [{"questionCode":"q1",
                            "isCorrect":True},
                            {"questionCode":"q2",
                            "isCorrect":False}]   
            }

def test_report_1():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    addNewAnswer("",event,s3)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["WorksheetCode"]=="testWorkSheet"
    assert report["attemptedBy"]==["xcai67"]
    assert report["completedBy"]==[]
    assert report["questions"]["q1"]=={
                "numberOfStudentAttempted":1,
                "numberOfStudentsCorrectlyAttmpted" :1,
                "averageNumOfAttemptsToCorrectlyAttempt":1}

def test_report_2():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    addNewAnswer("",event,s3)
    event["netId"]="xliu89"
    addNewAnswer("",event,s3)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["attemptedBy"]==["xcai67","xliu89"]
    assert report["questions"]["q1"]=={
                "numberOfStudentAttempted":2,
                "numberOfStudentsCorrectlyAttmpted":2,
                "averageNumOfAttemptsToCorrectlyAttempt":1}

def test_report_3():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    addNewAnswer("",event,s3)
    event["questionCode"]="q2"
    event["response"]="B"
    addNewAnswer("",event,s3)
    event["questionCode"]="q3"
    event["response"]="C"
    addNewAnswer("",event,s3)
    event["questionCode"]="q4"
    event["response"]=5
    addNewAnswer("",event,s3)
    report=read_json_default(s3,"pytutor/worksheets/report/testWorkSheet.json")
    assert report["completedBy"]==["xcai67"]

def test_getReport_1():
    s3=set_up()
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67",
        "worksheetCode": "testWorkSheet",
        "questionCode":"q1",
        "response":"A"
    }
    addNewAnswer("",event,s3)
    event["fn"]="getReport"
    report=getReport("",event,s3)
    print (report)
    assert len(report["report"]["questions"])==4

if __name__ == '__main__':
    test_getReport_1()