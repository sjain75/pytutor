from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
import os, sys, json, subprocess
from subprocess import check_output

PATH = os.getcwd()

PYTUTOR = PATH + "/../../resources/OnlinePythonTutor/v5-unity/generate_json_trace.py"

EMBEDDING = """
<div id="DIV" class=\"problem parentDiv\"></div>
<script type="text/javascript">
var trace = TRACE;
addVisualizerToPage(trace, 'DIV',  {START, hideCode: false, lang: "py3", disableHeapNesting: true, verticalStack: window.matchMedia("(max-width: 768px)").matches});
</script>
"""

# Create your views here.
def home(request):
    return render(request, "index.html")

@csrf_protect
def template(request):
    return HttpResponse(json.dumps({"hi":1}))

@csrf_protect
def convert(request):
    return HttpResponse(run_pytutor("print('Hello')"))


# Converts python code to JavaScript. 
# If the python file does not exist in specified file destination, will throw an error.
# py - the file path.
def run_pytutor(py):
    try:
        if os.path.exists(py):
            js = check_output(["python", "C:\\Users\\Eric Zhou\\Documents\\Projects\\Pytutor\\pytutor\\resources\\OnlinePythonTutor\\v5-unity\\generate_json_trace.py", "--code", py])
        else:
            print("Error! Check your paths to the python files (either in config or in command line)")
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))
