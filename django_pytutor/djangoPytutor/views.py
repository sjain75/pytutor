from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def home(request):
    return render(request, "index.html")

@csrf_protect
def template(request):

    return HttpResponse("1")
