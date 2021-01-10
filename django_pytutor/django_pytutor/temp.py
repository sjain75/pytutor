from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render
DEBUG = True
SECRET_KEY = '182@1c0_nk@)9k982u6afqf768f#6m5u6)vv-spjniwp3ynl-@'
ROOT_URLCONF = __name__

def home(request):
    return render(request, "index.html")

def template(request):

    return HttpResponse("1")

urlpatterns = [
    url(r'^$', home),
    url(r'^template$', template)
]
