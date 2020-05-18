import os, sys, json, subprocess
from subprocess import check_output

PYTUTOR = "/Users/ericz/Desktop/OnlinePythonTutor/v5-unity/generate_json_trace.py"
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

    for py in sys.argv[1:]:
        print("Working on file " + py + "...")
        js = run_pytutor(py)
        div = py.replace(".", "_").replace("/", "_")
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js)
        codeList = code.split("\n")
        print("Creating a template file...")
        os.chdir("../pages/")
        createNewFile(codeList, "templateFile.html")
        print("Check templateFile.html in the pages file to see an example")

        while(True):
            # for-loop to constantly prompt the user to enter in a valid choice, Y or N.
            userChoice = input("Are you writing to an existing file? (Y/N)").lower()
            if (userChoice.strip() == "y"):
                writeToExistingFile(codeList)
                print("File has been writen to!")
                break
            elif (userChoice.strip() == "n"):
                writeToNewFile(codeList)
                print("File has been written to!")
                break
            else:
                print("Error! Not a valid choice.")
        # Reset to original location so that if the user enters more than one file, will repeat the processs
        # without errors.
        os.chdir("../backend/")

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

    # This loop identifies where to insert code.
    i = 0
    for x in lines:
        if x == "<div id=\"lec-07_w19_py\"></div>":
            break
        i += 1

    for x in codeList:
        lines[i] = x
        i += 1

    with open(codeName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.

def createNewHeaders(lines):
    return 0
    # TODO figure this section out!

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

    createNewHeaders(lines)

    # codeList[0] is always an empty line character.
    codeList[0] = "<h2>Worksheet Problem " + input("What worksheet problem is this (an integer value)?") + "</h2>"

    # Enter new lines of code at that index found above.
    for x in codeList:
        lines[i] = x
        i += 1

    # Add end tags.
    lines[len(lines) - 1] = "</html>"
    lines[len(lines) - 2] = "</body>"
    lines[len(lines) - 3] = "<!--###-->"

    with open(fileName, 'w') as file:
        for item in lines:
            file.write("%s\n" % item)
    # copies all the lines over.
    
    

def writeToExistingFile(codeList):
    fileName = input("What is the file named?")
    # Might need to write some error-checking, in case any non-valid characters are typed.
    fileName += ".html"
    files = os.listdir()
    # Checking if the file exists in the pages directory.
    for file in files:
        if str(file) == fileName:
            f = open(fileName, 'a')
            addToFile(codeList, fileName)
            f.close()
            return
    
    print("Error! There is no file with your inputted name," + str(fileName))
    # This only occurs if there is no valid file.
    while(True):
        userChoice = input("Would you like to create a new file? (Y/N)").lower()
        if (userChoice.strip() == "y"):
            writeToNewFile(codeList)
        elif (userChoice.strip() == "n"):
            return
        else:
            print("Invalid choice!")


def writeToNewFile(codeList):
    # Prompt to name the new file
    fileName = input("What would you like the new file to be named?")
    fileName += ".html"

    #TODO test for invalid characters, make sure the file has .html extension.
        
    # Testing to see if the code prints.
    f = open(fileName, 'w')
    createNewFile(codeList, fileName)
    f.close()
    # This functions. Now, have to find a way to store the new html pages to somewhere...

if __name__ == '__main__':
     main()

