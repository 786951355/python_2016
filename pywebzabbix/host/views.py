from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi

def index(request):
    return HttpResponse('host index page')


def gethostitems(request):
    if request.method == 'POST':
        hostid = request.POST.get('hostid', None)
        items = zapi.item.get(output=["itemids", "key_"], hostids=hostid)
        return render(request, 'host/hostitems.html', {'items': items})
    elif request.is_ajax():
        return HttpResponse('Ajax')
    else:
        return render(request, 'host/itemform.html')


def create(request):
    return render(request, 'host/createhost.html')

def delete(request):
    return render(request, 'host/delhost.html')

def update(request):
    return render(request, 'host/updatehost.html')

