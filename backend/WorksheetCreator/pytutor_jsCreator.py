
import os, sys, json, subprocess
from shutil import copyfile
from subprocess import check_output

PYTUTOR = "../../resources/OnlinePythonTutor/v5-unity/generate_json_trace.py"

EMBEDDING = """
<div id="DIV" class=\"problem parentDiv\"></div>
<script type="text/javascript">
  var trace = TRACE;
  addVisualizerToPage(trace, 'DIV',  {START, hideCode: false, lang: "py3", disableHeapNesting: true});
</script>
"""

answers = {}

py = ""

def run_pytutor(py):
    try:
        js = check_output(["python", PYTUTOR, py])
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))

def main():
    if len(sys.argv) >= 2:
        createTracesPage()
        print("Creating your worksheet now...")

        # Prompts user for valid name. This code will only stop running when
        # the user has given an acceptable name or wants to append to a 
        # pre-existing file.
        append = False
        while(True):
            fileName = checkEmptyInput("What is the file name?")
            # Just a little QOL thing... It's also cuz I'm lazy and forget to type .html lol
            if ".html" not in fileName:
                fileName += ".html"
            if " " in fileName:
                print("Error! No spaces allowed in file name.")
            else:
                if os.path.exists("../../worksheets/HTML/" + fileName):
                    userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                    if userChoice.lower().strip() == "y":
                        append = True
                        break
                    elif userChoice.lower().strip() == "n":
                        userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                        if userChoice.lower().strip() == "y":
                            os.remove("../../worksheets/HTML/" + fileName)
                            break
                        else:
                            print("Unknown command!")
                            continue
                    else:
                        print("Unknown command!")
                        continue
                else:
                    break
        
        # Actual part of worksheet creation
        global answers
        if append:
            with open ("../../worksheets/HTML/" + fileName) as file:
                listOfFileLines = file.read().splitlines()
            
            with open("../../worksheets/answers/" + fileName.replace(".html", ".json"), "r") as read_file:
                answers = json.load(read_file)

            listOfFileLines = generateScripts(forTracesPage=False, lines=listOfFileLines)
        else:
            open("../../worksheets/HTML/" + fileName, 'x')
            answers = {"worksheetCode": fileName.replace(".html", ""), "totalNumOfQuestions": 0}
            try:
                copyfile("../../pages/defaultPageLayout.html", "../../worksheets/HTML/" + fileName)
            except IOError:
                print("Error! Check to make sure \"defaultPageLayout.html\" exists within the pages directory")
                sys.exit(1)
            
            listOfFileLines = createWorksheetTitle(fileName, forTracesPage=False)
            listOfFileLines = generateScripts(forTracesPage=False, lines=listOfFileLines)
        
        # This will write to the original file.
        with open("../../worksheets/HTML/" + fileName, "w") as file:
            for item in listOfFileLines:
                file.write("%s\n" % item)

        with open("../../worksheets/answers/" + fileName.replace(".html", ".json"), "w") as json_file:
            json.dump(answers, json_file)

    else:
        print("Error! How to run program: python pytutor_jsCreator.py [file_1.py] [file_2.py]...")

def checkEmptyInput(inputString):
    temp = input(inputString)
    while temp == "":
        print("Please enter a valid string.")
        temp = input(inputString)
    return temp

def generateScripts(forTracesPage, lines):
    global py
    for py in sys.argv[1:]:
        lines = addToFile([generateTrace(py, forTracesPage)], lines, not(forTracesPage))
    return lines

def createTracesPage():
    print("Generating ONLY story/trace questions in HTML/trace.html...")
    try:
        copyfile("../../pages/defaultPageLayout.html", "../../pages/trace.html")
    except IOError:
        print("Error! Check to make sure \"defaultPageLayout.html\" exists within the pages directory")
        sys.exit(1)

    listOfFileLines = createWorksheetTitle(fileName="trace.html", forTracesPage=True)

    listOfFileLines = generateScripts(forTracesPage=True, lines=listOfFileLines)

    with open("../../pages/trace.html", "w") as file:
        for item in listOfFileLines:
            file.write("%s\n" % item)

def generateTrace(py, forTracesPage):
    js = run_pytutor(py)
    div = py.replace(".", "_").replace("/", "_")
    
    if not(forTracesPage):
        print("Working on file " + py + "...")
        while(True):
            try:
                numSteps = (int(input("What step do you want the trace to begin at (an integer)?")) - 1)
                if not isinstance(numSteps, int) or numSteps < 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("Error! Not a valid number! The step number must be above 0 and must be an integer!")
        
        start = "startingInstruction:" + str(numSteps)
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js).replace("START", start)
    else:
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js).replace("START", "startingInstruction: 1")

    return code
    
def createWorksheetTitle(fileName, forTracesPage):
    with open (("../../pages/" if forTracesPage else "../../worksheets/HTML/") + fileName) as file:
        lines = file.read().splitlines()
    
    i = 0
    for x in lines:
        if x == "<h1 class=\"problem\">Template File, title would appear here!</h1>":
            break
        i += 1
    
    if not(forTracesPage):
        header = checkEmptyInput("What would you like to name your worksheet?")
        header = "<h1 class = \"problem\">" + header + "</h1>"
        lines[i] = header
    else:
        lines[i] = "<h1 class = \"problem\">Trace HTML File</h1>"
    
    return lines

def addToFile(codeList, listOfFileLines, headers):
    indexOfComment = 0
    for x in listOfFileLines:
        if x == "<!--###-->":
            break
        else:
            indexOfComment += 1

    if headers:
        fileNumber = 1
        for scriptIndex in range(0, len(codeList)):
            # Sort of a bad way of doing this... Find a better way to only put <h2 class>Worksheet Title</h2> etc.
            if "<div id=" not in codeList[scriptIndex]:
                continue
            while(True):
                try:
                    wsProb = float(input("What worksheet problem is this (an int or float)?"))
                except ValueError:
                    print("Error! Not a valid worksheet problem.")
                break
            codeList[scriptIndex] = "<h2 class = \"problem\">Worksheet Problem " + str(wsProb) + "</h2>" + "\n" + codeList[scriptIndex]

            for scriptTagIndex in range(scriptIndex, len(codeList)):
                if "</script>" not in codeList[scriptTagIndex]:
                    continue
                codeList[scriptTagIndex] += "\n" + generateQuestionString()
                break

            fileNumber += 1

    newList = [""] * (len(codeList) + len(listOfFileLines))

    j = 0
    # Copy over lines into newList.
    for x in listOfFileLines:
        newList[j] = x
        j += 1
    
    listOfFileLines = newList

    for x in codeList:
        listOfFileLines[indexOfComment] = x
        indexOfComment += 1

    # Add end tags
    listOfFileLines[len(listOfFileLines) - 1] = "</html>"
    listOfFileLines[len(listOfFileLines) - 2] = "</body>"
    listOfFileLines[len(listOfFileLines) - 3] = "<!--###-->"

    return listOfFileLines

def generateManualQuestion():
    global answers
    question = checkEmptyInput("What is the manual question?")

    # Error checking to make sure the value is an integer.
    while(True):
        try:
            stepNumber = int(input("What step will this question apply to?"))
        except ValueError:
            print("Error! Step number must be an integer value!")

        if py[:-3] + "_" + str(stepNumber) in answers:
            print("Question already exists!")
            continue

        answer = checkEmptyInput("What is the answer to this question?")
        
        answers["totalNumOfQuestions"] += 1
        answers[py[:-3] + "_" + str(stepNumber)] = answer
        break

    question = "<div step = " + str(stepNumber) + " class = \"manualQuestion\">" + question + "</div>"
    return question
    
def generateQuestionString():
    while(True):
        try:
            numQuestions = int(input("How many manual questions do you want (an integer)?"))
            break
        except ValueError:
            print("Error! The number of questions must be an integer!")
        
    stringQuestions = ""
    for q in range(0, numQuestions):
        print("Generating question " + str(q + 1) + "...")
        stringQuestions += generateManualQuestion() + "\n"
    
    return stringQuestions

if __name__ == '__main__':
     main()