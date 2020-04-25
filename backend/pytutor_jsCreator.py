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
        js = run_pytutor(py)
        div = py.replace(".", "_").replace("/", "_")
        code = EMBEDDING.replace("DIV", div).replace("TRACE", js)  
        while(True):
            # for-loop to constantly prompt the user to enter in a valid choice, Y or N.
            userChoice = input("Are you writing to an existing file? (Y/N)").lower()
            if (userChoice.strip() == "y"):
                writeToExistingFile(code)
                print("File has been writen to!")
                break
            elif (userChoice.strip() == "n"):
                writeToNewFile(code)
                print("File has been written to!")
                break
            else:
                print("Error! Not a valid choice.")

def writeToExistingFile(code):
    # Switches current working directory to pages, so that it'll print it into the file.
    os.chdir("../pages/")

    fileName = input("What is the file named?")
    # Might need to write some error-checking, in case any non-valid characters are typed.
    fileName += ".html"
    files = os.listdir()
    # Checking if the file exists in the pages directory.
    for file in files:
        if str(file) == fileName:
            f = open(fileName, 'a')
            f.write(code)
            f.close()
            return
    print("Error! There is no file with your inputted name," + str(fileName))
    # This only occurs if there is no valid file.
    try:
        userChoice = input("Would you like to create a new file? (Y/N)").lower()
        if (userChoice.strip() == "y"):
            writeToNewFile(code)
        elif (userChoice.strip() == "n"):
            return
        else:
            raise NameError()
    except NameError:
        print("Invalid file!")

def writeToNewFile(code):
    # Switch to the pages directory, where we will save our information.
    os.chdir("../pages/")

    # Prompt to name the new file
    fileName = input("What would you like the new file to be named?")
    fileName += ".html"

    #TODO test for invalid characters, make sure the file has .html extension.
        
    # Testing to see if the code prints.
    f = open(fileName, 'w')
    f.write(code)
    f.close()
    # This functions. Now, have to find a way to store the new html pages to somewhere...

if __name__ == '__main__':
     main()

