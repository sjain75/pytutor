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
        # Commented this out since we are now just writing to the directory. Now, don't have to copy and paste it.
        # print(code)
        
        while(True):
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

# TODO consider if it is necessary to break this up into two separate methods. They are essentially doing the exact same thing..

def writeToExistingFile(code):
    os.chdir("../pages/")

    fileName = input("What is the file named?")
    fileName += ".html"
    files = os.listdir()
    for file in files:
        if str(file) == fileName:
            f = open(fileName, 'w')
            f.write(code)
            f.close()
            return
    print("Error! There is no file with your inputted name," + str(fileName))
    while(True):
        userChoice = input("Would you like to create a new file? (Y/N)").lower()
        if (userChoice.strip() == "y"):
            writeToNewFile(code)
            break
        elif (userChoice.strip() == "n"):
            return
        else:
            print("Error! Not a valid choice.")
    


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

