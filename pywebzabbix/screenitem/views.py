from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi, ZabbixAPIException


def index(request):
    pass


def get(request):
    if request.method == 'POST':
        screenitems = zapi.screenitem.get(output="extend")
        return render(request, 'screenitem/screenitem.html', {'screenitems' : screenitems})
    else:
        return render(request, 'screenitem/get.html')

def create(request):
    if request.method == 'POST':
        params = {}
        for k, v in request.POST.items():
            if k == 'csrfmiddlewaretoken':
                continue
            else:
                params[k] = v
        print(params)
        try:
            zapi.screenitem.create(params)
            return HttpResponse('创建成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
    else:
        return render(request, 'screenitem/form.html')

def delete(reqeust):
    return HttpResponse('todo')

def update(request):
    if request.method == 'POST':
        params = {}
        for k, v in request.POST.items():
            if v:
                params[k] = v
            if k == 'csrfmiddlewaretoken':
                continue
        try:
            zapi.screenitem.update(params)
            return HttpResponse('更新成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
    else:
        return render(request, 'screenitem/updateform.html')
# Create your views here.
