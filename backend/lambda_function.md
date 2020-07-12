# functions in lambda

## addNewAnswer

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

## reload

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

## getReport


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

# files store in s3 

## worksheet answer 

pytutor.ddns.net/userDirectory/worksheets/answers/Worksheetcode.json
	
	{
    "worksheetCode": worksheetCode,
    "totalNumOfQuestions":  number of questions,  
    questionCode1: answer1,
    questionCode2: answer2,
    ...
    }

## student record

pytutor.ddns.net/userDirectory/student/username.json

	{
    "studentID":id,
    "numberOfWorksheetAttempted":2,
    "WorksheetCode1":{
		questionsAttempted: ,
		questionCorrectlyAttempted: ,
        q1:{
			numAttempts:	[numAttemptsTIllCorrect, totalNumAttempts]
			isCorrect:	False/True #once they have correctly attempted becomes true,
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

## report

pytutor.ddns.net/userDirectory/worksheets/worksheets/report/worksheetcode.json 

	{
    WorksheetCode:"a",
    "attemptedBy":[student1, student2,I ...] , //attempted at least 1 question
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

# TODO

while two students get report and wants to update them at the same time, the report would only update one result

