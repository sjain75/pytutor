<div align="center"><img src="http://pytutor.ddns.net/logo.svg" width="500"></img></div>  

# Pytutor 
Pytutor is a tool to allow python coders to do interactive exercises and collaborate. It aims to help teachers create interactive particpation activities and collect information about the students' level of understanding. 


## Setup and testing

0. Download release

1. Get in touch with us to be assigned an IAM user and for us to create appropriate directories for hosting you

        (*) Test if http://pytutor.ddns.net/[username]/worksheet/html/pytutor-demo.html
        (*) Install awscli (https://aws.amazon.com/cli/) if you would like to be able to upload files from cli
                Alternatively new worksheets and other files can always be uploaded vai AWS management console.

2. Use the `aws configure` command to add your aws credentials to access the bucket from your CLI.

3. Create a worksheet using the Worksheet Creator (refer Worksheet Creator Usage section below).

4. Upload .json file for answers and html file for the worksheet to the s3
  * Manually upload files to s3 using AWS management console using </br>
	https://s3.console.aws.amazon.com/s3/buckets/pytutor.ddns.net/[username]/?region=us-east-2 <b>OR</b>
  * Use `aws s3 cp [filepath] s3://pytutor.ddns.net/[username]/[path]/` with the appropriate paths. 

5. Test out the worksheet here: http://pytutor.ddns.net/[username]/worksheets/html/[worksheetFileName].html

## Worksheet Creator Usage

Tutorial for using WorksheetCreator/pytutor_jsCreator.py with no config file

- run in command line: "python3 pytutor_jsCreator.py [file1.py] [file2.py]..."
- file1.py, file2.py can be path locations to the python file.
- can input as many python file as necessary.
    Example: python pytutor_jsCreator.py ../testPyFile.py ../testPyFile2.py

- Immediately after running the python command, you can see a page that has only the traces in:
    ./pytutor_worksheets/trace.html
- We can use this only trace page to help us create story questions and where to begin the trace itself.

- Upon following guided prompts in command line, you can check your worksheet in:
    ./pytutor_worksheets/[worksheetName].html
- To check answers, you can find them in:
    ./pytutor_worksheets/[worksheetName].json

Example:
- if we input our file name to be "ws1", our worksheet will be:
    ./pytutor_worksheets/ws1.html
- Our answers will be in:
    ./pytutor_worksheets/ws1.json

Tutorial for using WorksheetCreator/pytutor_jsCreator.py with config file
- We assume that we have a pytutor_worksheets directory in CWD (./pytutor_worksheets exists)
- Config file should match the template in the pytutor/WorksheetCreator/configFormat, save as json
file titled "config.json"

- Template:
{
    "wsTitle": "[titleName]",
    "[pathToPyFile.py]": {
        "stepNumber": [intToBeginTrace],
        "problemName": "[problemName]",
        "manualQuestion": [{
            "question": "[manualQuestionProblem]",
            "stepNumber": [beginningStepNumber],
            "answer": "[manualQuestionAnswer]"
        }, {
            "question": "[manualQuestionProblem]",
            "stepNumber": [beginningStepNumber],
            "answer": "[manualQuestionAnswer]"
        }]
    }
}
- Note: you do not need manual questions. If no manual questions, don't set manualQuestion as a
key.

- Config file is then located in ./pytutor_worksheets directory
- run in command line: "python3 pytutor_jsCreator.py config.json"

- Will prompt for worksheet title/name. Upon doing so, if config information is put in correctly,
the worksheet should be created successfully with the config file info.

## Attempting worksheets

1. http://pytutor.ddns.net/[username]/pages/[WorksheetCode].html
2. Login with a google account.
3. Click on the number in the stories to move ahead.
4. Attempt manual questions which appear before moving forward (the story remains disabled until manual question is attempted).
5. Attempt all manual questions to get participation points 
(correctness is not important, only requirement is attempting the questions.)
(every question allow infinite attempts)

## Checking reports

1. Go to http://pytutor.ddns.net/[username]/pages/report.html
2. Login with email id with privileges to view the report.
3. Try getting a report with student's user id, worksheet code or get the master report. (it might take a second to load) (This updates the reports on S3)
4. <B>View the json visually using pythonTutor [Experimental]</B> </br>
   *Move the slider on the story to go to the next step. </br>
  
      <B>OR</B></br>
  
   <B>Downloading .json files </B></br>
   *Download the appropriate report.json file from the student/ or worksheets/report/ folder in the S3.

## Appendix

<b>Bucket Structure</b>  
* pytutor.ddns.net  
  * userDirectory //tyler, meena, ... //everything inside only accessible by user  
    * worksheets  
      * report  
      * html //public  
      * answers  
      * masterReport.json  
    * student  
        * username.json  
    * pages  
        * home.html //allows users to create a home page //other sample page //public   
        * report.html  //Template, makes users login from front-end using GAPI and then loads data through ajax request to lamdba  
  * js   
  * styles   
  * user-permission for requests directed in through lambda //for example request for report from front end to lambda //super-private  

<b>Github repo Sturcutre on User computers</b>  
* pytutor [repo folder]  
  * WorksheetCreator  
    * creator.py file  
    * test Py files  
  * pages  
    * home.html //can be pushed up to s3 bucket  
    * defaultPageLayout.html //used by worksheetCreator
  * worksheets //can be pushed up to s3 bucket  
    * html  
    * answers    
  * resources  

## Glossary
Two types of questions: Story questions and manual questions

Story questions: The user is required to navigate through a segment of Python code by clicking on the line that is
to be executed next in the control flow. These test the users understandings of if/else statements, function calls,
and loops

Manual questions: The user is required to enter a value or answer to a question that is asking about the code
segment at a particular point in time

Structure of each question: <i>The WorksheetCreator abstracts this really well.</i>
Outer div, no class or id is needed
    h2 tag with the problem number/title, class=my-3 problem
    div, id="testPyFile2_py" class="problem parentDiv" (Nothing is in this div)
    script tag with the generated js code, last bit includes the addVisualizerToPage
    div tags, class="manualQuestion" step="(step number the question is supposed to appear at)"

*Our users are Professors

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

