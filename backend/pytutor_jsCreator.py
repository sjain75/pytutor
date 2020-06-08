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
        codeList = generateTrace(py, EMBEDDING)
        generateInitialPage(codeList, 1, True, "templateFile.html")

        # Checking to see if the file exists within the pages directory.
        print("*******CREATING/ADDING TO FILE*******")
        fileName = input("What is the file name?") + ".html"
        files = os.listdir()
        for file in files:
            if str(file) == fileName:
                userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                if userChoice.lower().strip() == "y":
                    addToFile(codeList, fileName, True)
                    return
                else:
                    userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                    if userChoice.lower().strip() == "n":
                        sys.exit(1)

        # Deleting old file, then creating the new one by just renaming the templateFile.
        os.remove(fileName)
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
        codeList = generateTrace(py, EMBEDDING)
        generateInitialPage(codeList, 1, True, "templateFile.html")
        os.chdir("../backend/")
        generateInitialPage(codeList, 2, True, "templateFile.html")

        # Creating actual file.
        print("*******CREATING/ADDING TO FILE*******")
        fileName = input("What is the file name?") + ".html"
        os.chdir("../pages/")
        files = os.listdir()
        for file in files:
            if str(file) == fileName:
                userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                if userChoice.lower().strip() == "y":
                    for py in sys.argv[2:]:
                        codeList = generateTrace(py, EMBEDDING)
                        addToFile(codeList, fileName, True)
                    return
                else:
                    userChoice = input("Are you sure? By selecting yes, you will overwrite the pre-existing file. (Y/N)")
                    if userChoice.lower().strip() == "n":
                        sys.exit(1)

        # Deleting old file, then creating the new one by just renaming the templateFile.
        os.remove(fileName)
        os.rename("templateFile.html", fileName)
    
# TODO figure out better name, clean this method up cuz its disgusting.
def generateInitialPage(codeList, inputs, headers, fileName, embedding=EMBEDDING):
    if inputs == 1:
        py = sys.argv[1]
        print("Check " + fileName + "...")
        os.chdir("../pages/")
        print("Working on file " + py + "...")
        createNewFile(codeList, fileName, headers)
    else:
        # Adding on to the end of the template file.
        for py in sys.argv[2:]:
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
        start = "startingInstruction:" + str((int(input("What step do you want the trace to begin at (an integer)?")) - 1))
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
        if x == "<h1>Template File, title would appear here!</h1>":
            break
        i += 1

    header = input("What would you like to name your worksheet?")
    header = "<h1 class = \"problem\">" + header + "</h1>"
    lines[i] = header

    # Update the problem number.
    problemNumber = input("What worksheet problem is this (an integer value)?")
    title = "<h2 class=\"my-3 problem\">Worksheet Problem " + problemNumber + "</h2>"
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
        # codeList[0] is always an empty line character.
        codeList[0] = "<h2 class = \"problem\">Worksheet Problem " + input("What worksheet problem is this (an integer value)?") + "</h2>"

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
        lines[len(lines) - 3 - len(listQuestions)] = "<!--###-->"
        addManualQuestions(lines, listQuestions)

    with open(fileName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def generateManualQuestion():
    question = input("What is the manual question?")

    stepNumber = input("What step will this question apply to?")
    # Do we want the stepNumber in quotations? TODO

    question = "<div step = " + stepNumber + " class = \"manualQuestion\">" + question + "</div>"
    return question

def generateListQuestions():
    numQuestions = input("How many manual questions do you want (an integer)?")
    listQuestions = [None] * int(numQuestions)
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

