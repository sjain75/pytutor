from moto import mock_s3
from pytutor import Student
import boto3
import json

def test_init_student():
    mock = mock_s3()
    mock.start()

    resource = boto3.resource(
                        's3',
                         aws_access_key_id= "123",
                         aws_secret_access_key= "123" )
    resource.create_bucket(Bucket="bucket")

    event={
		"fn": "addNewAnswer",
		"netId": "xcai67", 
		"worksheetCode": 1234,
		"questionCode": 22,
		"response":"c"
	}
    
    student_instance = Student(event,resource,"bucket")
    assert student_instance.bucket=="bucket"

def test_getFile_student():
    mock = mock_s3()
    mock.start()

    resource = boto3.resource(
                        's3',
                         aws_access_key_id= "123",
                         aws_secret_access_key= "123" )
    resource.create_bucket(Bucket="bucket")

    event={
        "fn": "addNewAnswer",
        "netId": "xcai67", 
        "worksheetCode": 1234,
        "questionCode": 22,
        "response":"c"
    }

    student_instance = Student(event,resource,"bucket")
    student_instance.getFile()
    assert student_instance.student=={"studentID":"xcai67",
                    "numberOfWorksheetAttempted":0}

    
def test_checkAnswer():
    mock = mock_s3()
    mock.start()

    resource = boto3.resource(
                        's3',
                         aws_access_key_id= "123",
                         aws_secret_access_key= "123" )
    resource.create_bucket(Bucket="bucket")
    
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67", 
        "worksheetCode": "1234",
        "questionCode": "22",
        "response":"c"
    }
    student_instance = Student(event,resource,"bucket")
    result=student_instance.checkAnswer()
    print(result)
    assert result==("Wrong WorksheetCode",None)
    

def test_upload():
    mock = mock_s3()
    mock.start()

    resource = boto3.resource(
                        's3',
                         aws_access_key_id= "123",
                         aws_secret_access_key= "123" )
    resource.create_bucket(Bucket="bucket")
    event={
        "fn": "addNewAnswer",
        "netId": "xcai67", 
        "worksheetCode": "1234",
        "questionCode": "22",
        "response":"c"
    }
    student_instance = Student(event,resource,"bucket")
    result=student_instance.upload()
    print(result)
    assert result=={
            "statusCode": 200,
            "success": False,
            "errorCode": "Wrong WorksheetCode",
            "fnExecuted":"addNewAnswer",
            "isCorrect": []   
        }