from django.conf.urls import url
from django.http import HttpResponse

DEBUG = True
SECRET_KEY = '182@1c0_nk@)9k982u6afqf768f#6m5u6)vv-spjniwp3ynl-@'
ROOT_URLCONF = __name__

def home(request):
    return HttpResponse(template)

def template(request):
    return HttpResponse("1")

urlpatterns = [
    url(r'^$', home),
    url(r'^template$', template)
]

template = '''
<html>
    <head>
        <title>An example</title>
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script>
            function call_counter() {
                $.get('template', function (data) {
                    alert(data);
                });
            }
        </script>
    </head>
    <body>
        <button onclick="call_counter();">
            I update object 12345
        </button>
        <button onclick="call_counter();">
            I update object 999
        </button>
    </body>
</html>
'''