from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import json
import os, sys, json, subprocess
from subprocess import check_output

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
def convert(request):
	return HttpResponse(run_pytutor(json.loads(request.POST.get('code', None))))

@csrf_protect
def saveJson(request):
	rootPath = "../WorksheetCreator/"
	with open("config.json", "w") as configFile:
		confRec = request.POST.get('confJson', None)
		confRec =(json.loads(confRec))
		for pyFileName in confRec:
			if pyFileName!="wsTitle":
				with open(pyFileName, "w") as pyFile:
					pyFile.write(confRec[pyFileName]["trace"])
			else:
				wsName = confRec[pyFileName].replace(" ","")+".html"
		configFile.write(json.dumps(confRec))

	print(check_output("echo Y | python3 "+rootPath+"pytutor_jsCreator.py -c config.json", shell=True))
	return HttpResponse(json.dumps({"WsPath":"/pytutor_worksheets/"+wsName}))

# Converts python code to JavaScript.
# If the python file does not exist in specified file destination, will throw an error.
# py - the file path.
def run_pytutor(py):
    try:
        js = check_output(["python", "./jsCreator/generate_json_trace.py", "--code", py])
    except subprocess.CalledProcessError as e:
        js = e.output
    return json.dumps(json.loads(js))
