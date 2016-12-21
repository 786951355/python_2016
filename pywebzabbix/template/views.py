from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi



def index(request):
    return HttpResponse('template index page')

def get(request):
    templates = zapi.template.get(output="extend")
    return render(request, 'template/templateitems.html', {'templates': templates})


def create(request):
    return render(request, 'template/createtemplate.html')

def delete(request):
    return render(request, 'template/deltemplate.html')

def update(request):
    return render(request, 'template/updatetemplate.html')



# Create your views here.
