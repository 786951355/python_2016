from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi, ZabbixAPIException


def index(request):
    return render(request, 'hostgroup/index.html')

def nav(request):
    return render(request, 'hostgroup/nav.html')

def gethostgroup(request):
    groupinfo = zapi.hostgroup.get(output="extend")
    return render(request,'hostgroup/hostgroup.html', {'groupinfo': groupinfo})

def gethosts(request):
    if request.method == 'POST':
        groupid = request.POST.get('groupid',2)
        hostsinfo = zapi.host.get(output='extend', groupids=groupid)
        return render(request, 'host/hosts.html', {'hostsinfo': hostsinfo})
    else:
        return render(request, 'hostgroup/hostform.html')

def gethostitems(request):
    if request.method == 'POST':
        hostid = request.POST.get('hostid', None)
        items = zapi.item.get(output=["itemids", "key_"], hostids=hostid)
        return render(request, 'hostgroup/hostitems.html', {'items': items})
    else:
        return render(request, 'hostgroup/itemform.html')

def creategroup(request):
    if request.method == 'POST':
        name = request.POST.get('groupname', None)
        if name is None:
            return HttpResponse('组名不能为空')
        for g in zapi.hostgroup.get(output="extend"):
            if name in g.values():
                return HttpResponse('group exist')
        else:
            try:
                zapi.hostgroup.create(name=name)
                return HttpResponse('group create success')
            except ZabbixAPIException as e:
                print(e)
    return render(request, 'hostgroup/creategroup.html')

def delgroup(request):
    if request.method == 'POST':
        groupid = request.POST.get('groupid', None)
        if groupid is None:
            return HttpResponse('组ID不能为空')
        for g in zapi.hostgroup.get(output="extend"):
            if groupid in g.values():
                zapi.hostgroup.delete(groupid)
                return HttpResponse('delete group success, name {}, groupid {}'.format(g['name'], groupid))
        else:
            return HttpResponse('group not exist')
    return render(request, 'hostgroup/delgroup.html')

