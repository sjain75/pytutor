import os, sys, json, subprocess
from shutil import copyfile
from subprocess import check_output

PYTUTOR = "../resources/OnlinePythonTutor/v5-unity/generate_json_trace.py"

EMBEDDING = """
<div id="DIV" class=\"problem parentDiv\"></div>
<script type="text/javascript">
  var trace = TRACE;
  addVisualizerToPage(trace, 'DIV',  {START, hideCode: false, lang: "py3", disableHeapNesting: true, verticalStack: window.matchMedia("(max-width: 768px)").matches});
</script>
"""

answers = {}

py = ""

config = None

# Will load config that the user provides in the pytutor_worksheets. Stores it in global
# variable config as a dictionary.
def loadConfig():
    global config
    try:
        with open('./pytutor_worksheets/config.json') as file:
            config = json.load(file)
            return
    except OSError:
        print("Error! Make sure that ./pytutor_worksheets/config.json exists.")
        print("Creating pytutor_worksheets if the directory did not exist before in CWD...")
        print("To use config.json, add it to the new pytutor_worksheets folder in CWD")
        exit(1)
    

# Converts python code to JavaScript. 
# If the python file does not exist in specified file destination, will throw an error.
# py - the file path.
def run_pytutor(py):
    try:
        if os.path.exists(py):
            js = check_output(["python", PYTUTOR, py])
        else:
            print("Error! Check your paths to the python files (either in config or in command line)")
            exit(1)
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))

def main():
    if len(sys.argv) >= 2:
        # poop:)
        # Creates pytutor_worksheets directory in CWD.
        if not os.path.exists("./pytutor_worksheets"):
            try:
                os.mkdir("./pytutor_worksheets")
            except OSError:
                sys.exit(1)
        
        if "config.json" in sys.argv:
            loadConfig()

        createTracesPage()
        print("Creating your worksheet now...")

        # Prompts user for valid name. This code will only stop running when
        # the user has given an acceptable name or wants to append to a 
        # pre-existing file.
        append = False
        while(True):
            worksheetName = checkEmptyInput("What is the worksheet name?")
            # Removes all whitespace from worksheetName, stores it into fileName variable
            if " " in worksheetName:
                fileName = worksheetName.replace(" ", "")
            else:
                fileName = worksheetName

            # Just a little QOL thing... It's also cuz I'm lazy and forget to type .html lol
            if ".html" not in fileName:
                fileName += ".html"

            # Actual worksheet creation.
            if os.path.exists("./pytutor_worksheets/" + fileName):
                # check if config exists. If it does exist, we just overwrite previous files.
                if config != None:
                    userChoice = input("Warning! Since both the config and worksheet file already exist, we\n"
                    + " will delete the previous file and rewrite it with the given config and\n"
                    + " python files provided. Therefore, you may lose previous work if the config\n"
                    + " and python files differ from the first time you ran this command. Press\n"
                    + " (Y) if you want to confirm, and (N) if you want to stop.\n")
                    if userChoice.lower().strip() == "y":
                        os.remove("./pytutor_worksheets/" + fileName)
                        break
                    elif userChoice.lower().strip() == "n":
                        print("Cancelling request...")
                        sys.exit(1)
                    else:
                        print("Unknown command!")
                        continue
                else:
                    userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                    if userChoice.lower().strip() == "y":
                        append = True
                        break
                    elif userChoice.lower().strip() == "n":
                        userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                        if userChoice.lower().strip() == "y":
                            os.remove("./pytutor_worksheets/" + fileName)
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
            with open ("./pytutor_worksheets/" + fileName) as file:
                listOfFileLines = file.read().splitlines()
            
            with open("./pytutor_worksheets/" + fileName.replace(".html", ".json"), "r") as read_file:
                answers = json.load(read_file)

            listOfFileLines = generateScripts(forTracesPage=False, lines=listOfFileLines)
        else:
            open("./pytutor_worksheets/" + fileName, 'x')
            answers = {"worksheetCode": fileName.replace(".html", ""), "totalNumOfQuestions": 0}
            try:
                # MAKE SURE TO CHANGE THIS.
                copyfile("../pages/defaultPageLayout.html", "./pytutor_worksheets/" + fileName)
            except IOError:
                print("Error! Check to make sure \"defaultPageLayout.html\" exists within the pages directory")
                sys.exit(1)
            
            listOfFileLines = createWorksheetTitle(fileName, worksheetName, forTracesPage=False)
            listOfFileLines = generateScripts(forTracesPage=False, lines=listOfFileLines)
        
        # This will write to the original file.
        with open("./pytutor_worksheets/" + fileName, "w") as file:
            for item in listOfFileLines:
                file.write("%s\n" % item)

        with open("./pytutor_worksheets/" + fileName.replace(".html", ".json"), "w") as json_file:
            json.dump(answers, json_file)

    # If given no additional python files, will print this error. See README for more information.
    else:
        print("Error! How to run program: python pytutor_jsCreator.py [file_1.py] [file_2.py]...")

# Checks if given input string is empty. Will keep on prompting user to input a non-empty string
# until user enters one.
# inputString - input string that user provides.
def checkEmptyInput(inputString):
    temp = input(inputString)
    while temp == "":
        print("Please enter a valid string.")
        temp = input(inputString)
    return temp

# Will generate and essentially add the scripts to the html file.
# forTracesPage - boolean signaling if we are generating trace.html.
# lines - the html file in the form of a list (TODO, maybe remove if not necessary).
# Returns the updated file in a list.
def generateScripts(forTracesPage, lines):
    global py
    if config:
        pys = list(config.keys())
        if "wsTitle" in config:
            pys.remove("wsTitle")
    else:
        pys = sys.argv[1:]
    
    for py in pys:
        lines = addToFile([generateTrace(py, forTracesPage)], lines, not(forTracesPage))
    return lines

# Creates the initial traces page itself. 
# Will throw an error and exit if defaultPageLayout.html does not exist within the
# pages directory.
def createTracesPage():
    print("Generating ONLY story/trace questions in html/trace.html...")
    try:
        #MAKE SURE TO CHANGE THIS.
        copyfile("../pages/defaultPageLayout.html", "./pytutor_worksheets/trace.html")
    except IOError:
        print("Error! Check to make sure \"defaultPageLayout.html\" exists within the pages directory")
        sys.exit(1)

    listOfFileLines = createWorksheetTitle(fileName="trace.html", worksheetName="Trace File", forTracesPage=True)

    listOfFileLines = generateScripts(forTracesPage=True, lines=listOfFileLines)

    # Writes to the trace.html file.
    with open("./pytutor_worksheets/trace.html", "w") as file:
        for item in listOfFileLines:
            file.write("%s\n" % item)

# Creates the actual "trace"/div container for the html file. Uses the EMBEDDING and replaces
# specific keywords. Prompts user to input a valid initial step number.
# py - the file path to the python file
# forTracesPage - boolean signaling whether or not we are generating the trace.html page.
# return Code - returns the trace/div container.
def generateTrace(py, forTracesPage):
    global config
    js = run_pytutor(py)
    div = py.replace(".", "_").replace("/", "_")
    
    if not(forTracesPage):
        if config is not None and "stepNumber" in config[py]:
            try:
                numSteps = config[py]["stepNumber"] - 1
                if not isinstance(numSteps, int) or numSteps < 0:
                    raise ValueError
            except ValueError:
                print("Error! Not a valid number! The step number must be above 0 and must be an integer! Check the config.json...")
        else:
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
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js).replace("START", "startingInstruction: 0")

    return code
    
# Generates the worksheets <h1> by storing the defaultPageLayout.html into a list. Modifies
# specific index to create the header.
# fileName - the name of the file.
# forTracesPage - boolean signaling whether or not we are generating the trace.html page.
# return lines - returns the updated file in the form of a list.
def createWorksheetTitle(fileName, worksheetName, forTracesPage):
    global config
    with open (("./pytutor_worksheets/" if forTracesPage else "./pytutor_worksheets/") + fileName) as file:
        lines = file.read().splitlines()
    
    i = 0
    for x in lines:
        if x == "<h1 class=\"problem\">Template File, title would appear here!</h1>":
            break
        i += 1

    if not(forTracesPage):
        if config is not None and "wsTitle" in config:
            header = config["wsTitle"]
        else:
            header = worksheetName
            
        header = "<h1 class = \"problem\">" + header + "</h1>"
        lines[i] = header
    else:
        lines[i] = "<h1 class = \"problem\">Trace html File</h1>"
    
    return lines

# Adds to the file by locating a specific comment ("<!---###-->"). Upon identifying the location
# of the comment, appends the traces that we produced earlier to that location. Prompts for
# manual questions as well.
# codeList - the scripts themselves, stored in a list.
# listOfFileLines - the file that we are adding to in the form of a list.
# headers - boolean, telling the program if we want to add additional headers/manual questions.
def addToFile(codeList, listOfFileLines, headers):
    global py, config
    indexOfComment = 0
    endTags = []
    for x in listOfFileLines:
        if x == "<!---###-->":
            endTags = listOfFileLines[indexOfComment:]
            listOfFileLines = listOfFileLines[:indexOfComment]
            break
        else:
            indexOfComment += 1

    for index, script_code in enumerate(codeList):
        listOfFileLines.append("<div>\n")

    if headers:
        for scriptIndex in range(0, len(codeList)):
            # Config Option
            if config is not None and "problemName" in config[py]:
                wsProb = config[py]["problemName"]
            # Manual input option
            else:
                wsProb = checkEmptyInput("What is the problem title?")
            # Appending wsProblem
            listOfFileLines.append("<h2 class = \"problem\">Worksheet Problem " + str(wsProb) + "</h2>" + "\n")
            listOfFileLines.append(codeList[scriptIndex])
            # This prompts the user for manual questions (if any).
            if config is not None and "manualQuestion" in config[py]:
                listOfFileLines.append("\n" + generateQuestionStringConfig())
            else:
                listOfFileLines.append("\n" + generateQuestionString())
    else:
        for scriptIndex in range(0, len(codeList)):
            listOfFileLines.append(codeList[scriptIndex])

	# Copies everything over from the end Tags/static content to the end. less hardcoding now.
	# Adding closing div for each story problem. Will always be after all the manual questions.
    listOfFileLines.append("</div>\n")
    listOfFileLines.extend(endTags)
    return listOfFileLines

# Generates question strings if the config is specified/has manual questions to enter.
# Returns - string that contains all the questions.
def generateQuestionStringConfig():
    global config, answers, py
    divQuestions = ""
    for manualQuestions in config[py]["manualQuestion"]:
        question = manualQuestions["question"]
        stepNumber = manualQuestions["stepNumber"]
        answer = manualQuestions["answer"]

        # Check if question at this step already exists.
        if py.replace(".", "_") + "_" + str(stepNumber) in answers:
            print("Question already exists!")
            continue
        else:
            answers["totalNumOfQuestions"] += 1
            answers[py.replace(".", "_") + "_" + str(stepNumber)] = answer

        divQuestions += "\n<div step = " + str(stepNumber) + " class = \"manualQuestion\">" + question + "</div>"
     
    return divQuestions

# Prompts user for a question/answer to the trace. The answers are stored in a json file.
# returns question - returns the question and answer.
def generateManualQuestion():
    global answers, py
    question = checkEmptyInput("What is the manual question?")

    # Error checking to make sure the value is an integer.
    while(True):
        try:
            stepNumber = int(input("What step will this question apply to?"))
        except ValueError:
            print("Error! Step number must be an integer value!")
            continue
        
        if py.replace(".", "_") + "_" + str(stepNumber) in answers:
            print("Question already exists!")
            continue

        answer = checkEmptyInput("What is the answer to this question?")
        
        answers["totalNumOfQuestions"] += 1
        # Change this depending on what Sarwagya wants.
        answers[py.replace(".", "_") + "_" + str(stepNumber)] = answer
        break
    
    question = "<div step = " + str(stepNumber) + " class = \"manualQuestion\">" + question + "</div>"
    return question

# Prompting the user to give an integer representing how many manual questions they want for
# the trace page. Will take 0 as an input.
# return stringQuestions - returns the total number of questions (encompassed in their div)
#  as a string. 
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
