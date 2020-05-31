import os, sys, json, subprocess
from subprocess import check_output

PYTUTOR = "../resources/OnlinePythonTutor/v5-unity/generate_json_trace.py"
# User path dependent. Had to change my name and my path to get to here. Only the OnlinePythonTutor stuff is
# the same, but even so that is just because its path dependent.

# Depends on location as well now. 
# General format: (have to be within the Pytutor/backend directory)
# python pytutor_jsCreator.py (directory name, should be within the document. See calendars.py for example)


EMBEDDING = """
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
        codeList = generateTrace(py)

        # Template file creation.
        print("Creating a template file...")
        os.chdir("../pages/")
        print("Working on file " + py + "...")
        createNewFile(codeList, "templateFile.html")
        print("Check templateFile.html in the pages file to see an example")

        # Checking to see if the file exists within the pages directory.
        print("*******CREATING/ADDING TO FILE*******")
        fileName = input("What is the file name?") + ".html"
        files = os.listdir()
        for file in files:
            if str(file) == fileName:
                userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                if userChoice.lower().strip() == "y":
                    addToFile(codeList, fileName)
                    return

        # Else, will print to existing file.
        print("Printing/Overwriting to a new file...")
        createNewFile(codeList, fileName)
    
    # More than 1 input file.
    else:
        # Creating initial template file.
        py = sys.argv[1]
        codeList = generateTrace(py)
        print("Creating a template file...")
        os.chdir("../pages/")
        print("Working on file " + py + "...")
        createNewFile(codeList, "templateFile.html")
        os.chdir("../backend/")

        # Adding on to the end of the template file.
        for py in sys.argv[2:]:
            print("Working on file " + py + "...")
            codeList = generateTrace(py)
            os.chdir("../pages/")
            addToFile(codeList, "templateFile.html")
            os.chdir("../backend/")

        # Creating actual file.
        print("*******CREATING/ADDING TO FILE*******")
        fileName = input("What is the file name?") + ".html"
        os.chdir("../pages/")
        files = os.listdir()
        os.chdir("../backend/")
        for file in files:
            if str(file) == fileName:
                userChoice = input("This file already exists. Would you like to append it to the already existing file? (Y/N)")
                if userChoice.lower().strip() == "y":
                    for py in sys.argv[1:]:
                        print("Working on file " + py + "...")
                        codeList = generateTrace(py)
                        os.chdir("../pages/")
                        addToFile(codeList, fileName)
                        os.chdir("../backend/")
                    return
        

        # If we need to overwrite/create a new file, this runs.
        print("Printing/Overwriting to a new file...")
        
        os.chdir("../backend/")
        py = sys.argv[1]
        codeList = generateTrace(py)
        os.chdir("../pages/")
        createNewFile(codeList, fileName)
        os.chdir("../backend/")

        for py in sys.argv[2:]:
            print("Working on file " + py + "...")
            codeList = generateTrace(py)
            os.chdir("../pages/")
            addToFile(codeList, fileName)
            os.chdir("../backend/")
    

def generateTrace(py):
    js = run_pytutor(py)
    div = py.replace(".", "_").replace("/", "_")
    code = EMBEDDING.replace("DIV", div).replace("TRACE", js)
    codeList = code.split("\n")

    # Allocating space for the manual answer.
    newList = [""] * (len(codeList) + 1)
    limit = len(codeList) - 2
    i = 0
    for x in codeList:
        if i == limit:
            i += 1
            break
        else:
            newList[i] = x
            i += 1
    
    # Adding last script tag at end.    
    newList[len(newList) - 2] = "</script>"
    codeList = newList
    return codeList

def updateFileHeader(lines):
    # We are updating the title header.
    i = 0
    for x in lines:
        if x == "<h1>Template File, title would appear here!</h1>":
            break
        i += 1

    header = input("What would you like to name your worksheet?")
    header = "<h1>" + header + "</h1>"
    lines[i] = header

    # Updating the problem number.
    # i = 0
    # for x in lines:
    #     if x.encode('unicode_escape').decode() == "<h2 class=\"my-3\">Worksheet Problem 404</h2>":
    #         break
    #     i += 1
    problemNumber = input("What worksheet problem is this (an integer value)?")
    title = "<h2 class=\"my-3\">Worksheet Problem " + problemNumber + "</h2>"
    lines[134] = title

def createNewFile(codeList, codeName):
    with open("defaultPageLayout.html") as file:
        lines = file.read().splitlines()

    updateFileHeader(lines)
    
    i = 135
    for x in codeList:
        lines[i] = x
        i += 1

    # Create prompts TODO
    generateManualQuestion(lines)

    with open(codeName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def addToFile(codeList, fileName):
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

    # codeList[0] is always an empty line character.
    codeList[0] = "<h2>Worksheet Problem " + input("What worksheet problem is this (an integer value)?") + "</h2>"

    # Copies over codeList items into lines.
    for x in codeList:
        lines[i] = x
        i += 1

    generateManualQuestion(lines)

    # Add end tags
    lines[len(lines) - 1] = "</html>"
    lines[len(lines) - 2] = "</body>"
    lines[len(lines) - 3] = "<!--###-->"


    with open(fileName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def generateManualQuestion(lines):
    question = "<div class = \"manualQuestion\">" + input("What is the manual question?") + "</div>"
    stepNumber = input("What step will this question apply to?")
    # Do we want the stepNumber in quotations? TODO
    question = "<div step = " + stepNumber + " class = \"manualQuestion\">" + question + "</div>"
    lines[len(lines)-4] = question

    answer = input("What is the answer to the question?")
    lines[len(lines) - 6] = "  manualAnswer=\"" + answer + "\";"

if __name__ == '__main__':
     main()

