import os, sys, json, subprocess
from subprocess import check_output

PYTUTOR = "../resources/OnlinePythonTutor/v5-unity/generate_json_trace.py"

EMBEDDING = """
<div id="DIV"></div>
<script type="text/javascript">
  var trace = TRACE;
  addVisualizerToPage(trace, 'DIV',  {START, hideCode: false, lang: "py3", disableHeapNesting: true});
</script>
"""

STORY_EMBEDDING = """
<div id="DIV"></div>
<script type="text/javascript">
  var trace = TRACE;
  addVisualizerToPage(trace, 'DIV',  {startingInstruction: 0, hideCode: false, lang: "py3", disableHeapNesting: true});
</script>
"""

def run_pytutor(py):
    try:
        js = check_output(["python", PYTUTOR, py])
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))

def main():
    if len(sys.argv) < 2:
        print("Usage: python pytutor.py file1.py [file2.py, ...]")
        sys.exit(1)

    # Only 1 input file
    elif len(sys.argv) == 2:
        py = sys.argv[1]

        # Generate only story/trace questions at first.
        print("Generating ONLY story/trace questions in trace.html...")
        codeList = generateTrace(py, STORY_EMBEDDING)
        generateInitialPage(codeList, 1, False, "trace.html")

        print("******TEMPLATEFILE CREATION******")
        # Change to original directory so that the python files can be located again
        os.chdir("../backend/")
        print("Working on file " + py + "...")
        codeList = generateTrace(py, EMBEDDING)
        generateInitialPage(codeList, 1, True, "templateFile.html")

        # Checking to see if the file exists within the pages directory.
        print("*******CREATING/ADDING TO FILE*******")

        while(True):
            fileName = input("What is the file name (.html extension not necessary)?") + ".html"
            if " " in fileName:
                print("Error! No spaces allowed in file name.")
            else:
                break

        files = os.listdir()
        for file in files:
            if str(file) == fileName:
                while(True):
                    userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                    if userChoice.lower().strip() == "y":
                        addToFile(codeList, fileName, True)
                        return
                    elif userChoice.lower().strip() == "n":
                        userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                        if userChoice.lower().strip() == "y":
                            os.remove(fileName)
                            break

        os.rename("templateFile.html", fileName)
    
    # More than 1 input file.
    else:
        py = sys.argv[1]
        # Generating ONLY trace/story questions
        print("Generating ONLY story/trace questions in trace.html...")
        codeList = generateTrace(py, STORY_EMBEDDING)
        generateInitialPage(codeList, 1, False, "trace.html", STORY_EMBEDDING)
        os.chdir("../backend/")
        generateInitialPage(codeList, 2, False, "trace.html", STORY_EMBEDDING)

        print("******TEMPLATEFILE CREATION******")
        # Creates template + adds first file.
        print("Working on file " + py + "...")
        codeList = generateTrace(py, EMBEDDING)
        generateInitialPage(codeList, 1, True, "templateFile.html")

        # Adds remaining files.
        os.chdir("../backend/")
        generateInitialPage(codeList, 2, True, "templateFile.html")

        # Creating actual file.
        print("*******CREATING/ADDING TO FILE*******")

        while(True):
            fileName = input("What is the file name (.html extension not necessary)?") + ".html"
            if " " in fileName:
                print("Error! No spaces allowed in file name.")
            else:
                break
        
        os.chdir("../pages/")
        files = os.listdir()
        for file in files:
            if str(file) == fileName:
                while(True):
                    userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                    if userChoice.lower().strip() == "y":
                        for py in sys.argv[1:]:
                            os.chdir("../backend/")
                            codeList = generateTrace(py, EMBEDDING)
                            os.chdir("../pages/")
                            addToFile(codeList, fileName, True)
                        return
                    elif userChoice.lower().strip() == "n":
                        userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                        if userChoice.lower().strip() == "y":
                            os.remove(fileName)
                            break
        
        os.rename("templateFile.html", fileName)
    
# TODO figure out better name, clean this method up cuz its disgusting.
def generateInitialPage(codeList, inputs, headers, fileName, embedding=EMBEDDING):
    if inputs == 1:
        py = sys.argv[1]
        os.chdir("../pages/")
        createNewFile(codeList, fileName, headers)
    else:
        # Adding on to the end of the template file.
        for py in sys.argv[2:]:
            if headers:
                print("Working on file " + py + "...")
            codeList = generateTrace(py, embedding)
            os.chdir("../pages/")
            addToFile(codeList, fileName, headers)
            os.chdir("../backend/")

def generateTrace(py, embedding):
    js = run_pytutor(py)
    div = py.replace(".", "_").replace("/", "_")
    
    # Checks if START is an existing keyword in the given embedding.
    if "START" in embedding:
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
        code = embedding.replace("DIV", div).replace("TRACE", js).replace("START", start)
    else:
        code = embedding.replace("DIV", div).replace("TRACE", js)

    codeList = code.split("\n")
    newDiv = "<div id=\"" + div + "\" class=\"problem\"></div>"
    codeList[1] = newDiv
    return codeList

def updateFileHeader(lines):
    # We are updating the title header.
    i = 0
    for x in lines:
        if x == "<h1 class=\"problem\">Template File, title would appear here!</h1>":
            break
        i += 1

    header = input("What would you like to name your worksheet?")
    header = "<h1 class = \"problem\">" + header + "</h1>"
    lines[i] = header

    # Update the problem number.
    while(True):
        try:
            problemNumber = float(input("What worksheet problem is this (an int or float)?"))
            break
        except ValueError:
            print("Error! The problem number is not an integer or float!")
    
    title = "<h2 class=\"my-3 problem\">Worksheet Problem " + str(problemNumber) + "</h2>"
    #TODO fix this hardcode.
    lines[134] = title

def createNewFile(codeList, codeName, headers):
    with open("defaultPageLayout.html") as file:
        lines = file.read().splitlines()

    # Generates headers ONLY if headers parameter is true.
    if headers:
        updateFileHeader(lines)
    
    i = 135
    for x in codeList:
        lines[i] = x
        i += 1

    # Generating number of questions list. Only occurs if headers is equal to true.
    if headers:
        listQuestions = generateListQuestions()
        newList = [""] * (len(listQuestions) + len(lines))

        # Copy over everything from lines into newList.
        i = 0
        for x in lines:
            newList[i] = x
            i += 1

        lines = newList

    # Add end tags.
    lines[len(lines) - 1] = "</html>"
    lines[len(lines) - 2] = "</body>"
    lines[len(lines) - 3] = "<!--###-->"
    
    # Only occurs if headers is equal to true.
    if headers:
        # If statement to check if there are any manual questions (can input 0 manual questions now)
        if len(listQuestions) > 0:
            addManualQuestions(lines, listQuestions)

    with open(codeName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def addToFile(codeList, fileName, headers):
    # Will detect <!--###-->, prompting the program to add new files here.
    with open (fileName) as file:
        lines = file.read().splitlines()
    
    # Locate the location of the comment <!--###-->
    i = 0
    for x in lines:
        if x == "<!--###-->":
            break
        else:
            i += 1

    # need to create a new list that has more space allocated for the new problem.
    newList = [None] * (len(codeList) + len(lines))

    j = 0
    # Copy over lines into newList.
    for x in lines:
        newList[j] = x
        j += 1

    lines = newList

    if headers:
        while(True):
            try:
                wsProb = float(input("What worksheet problem is this (an int or float)?"))
                break
            except ValueError:
                print("Error! Not a valid worksheet problem.")
            
        # codeList[0] is always an empty line character.
        codeList[0] = "<h2 class = \"problem\">Worksheet Problem " + str(wsProb) + "</h2>"

    # Enter new lines of code at that index found above.
    for x in codeList:
        lines[i] = x
        i += 1
    
    if headers:
        listQuestions = generateListQuestions()
        newList = [None] * (len(listQuestions) + len(lines))
        # Copy over everything from lines into newList.
        i = 0
        for x in lines:
            newList[i] = x
            i += 1
        lines = newList

    # Add end tags
    lines[len(lines) - 1] = "</html>"
    lines[len(lines) - 2] = "</body>"
    lines[len(lines) - 3] = "<!--###-->"

    if headers:
        if len(listQuestions) > 0:
            lines[len(lines) - 3 - len(listQuestions)] = "<!--###-->"
            addManualQuestions(lines, listQuestions)

    with open(fileName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def generateManualQuestion():
    question = input("What is the manual question?")

    # Error checking to make sure the value is an integer.
    while(True):
        try:
            stepNumber = int(input("What step will this question apply to?"))
            break
        except ValueError:
            print("Error! Step number must be an integer value!")

    question = "<div step = " + str(stepNumber) + " class = \"manualQuestion\">" + question + "</div>"
    return question

def generateListQuestions():
    while(True):
        try:
            numQuestions = int(input("How many manual questions do you want (an integer)?"))
            break
        except ValueError:
            print("Error! The number of questions must be an integer!")
    
    listQuestions = [None] * numQuestions
    for i in range(0,len(listQuestions)):
        print("Generating question " + str(i + 1) + "...")
        listQuestions[i] = generateManualQuestion()
        i += 1
    return listQuestions

# Check references TODO
def addManualQuestions(lines, listQuestions):
    i = 0
    for x in lines:
        if x == "<!--###-->":
            break
        i += 1
    # adding initial question to the list.
    lines[i] = listQuestions[0]
    i += 1
    
    # Will not check if the list of questions has more than just 1 question.
    if len(listQuestions) == 1:
        return
    else:
        for x in listQuestions[1:]:
            lines[i] = x
            i += 1


if __name__ == '__main__':
     main()

