from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi, ZabbixAPIException
import json

def index(request):
    return HttpResponse('graph index')

def get(request):
    if request.method == 'POST':
        hostid = request.POST.get('hostid', None)
        if hostid is None:
            return HttpResponse('hostid is not none')
        items = zapi.graph.get(output=["name", "graphid"], hostids=hostid)
        return render(request, 'graph/graph.html', {'items': items, 'hostid': hostid})
    else:
        return render(request, 'graph/form.html')


def create(request):
    if request.method == 'POST':
        data = {}
        for k in request.POST:
            if k == 'csrfmiddlewaretoken':
                continue
            else:
                data[k] = request.POST.getlist(k)

        gitems = []
        for i in range(len(data.get('itemid'))):
            gitems.append(
                {
                    "itemid": data.get('itemid')[i],
                    "color": data.get('color')[i].strip('#'),
                    "drawtype": int(data.get('drawtype')[i]),
                    "sortorder": int(data.get('sortorder')[i])
                })

        params = {
            "name": data.get('graphname')[0],
            "width": int(data.get('width')[0]),
            "height": int(data.get('height')[0]),
            "gitems": gitems
        }
        try:
            zapi.graph.create(params)
            return HttpResponse('创建成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
        return HttpResponse('test')
    else:
        return render(request, 'graph/create.html')


def delete(request):
    if request.method == 'POST':
        graph_list = request.POST.get('graphid').split(',')
        print(graph_list)
        try:
            zapi.graph.delete(*graph_list)
            return HttpResponse('删除成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
    else:
        return render(request, 'graph/delete.html')

def update(request):
    if request.method == 'POST':
        data = {}
        for k in request.POST:
            if k == 'csrfmiddlewaretoken':
                continue
            else:
                data[k] = request.POST.getlist(k)

        gitems = []
        for i in range(len(data.get('itemid'))):
            gitems.append(
                    {
                        "itemid": data.get('itemid')[i],
                        "color": data.get('color')[i].strip('#'),
                        "drawtype": int(data.get('drawtype')[i]),
                        "sortorder": int(data.get('sortorder')[i])
            })

        params = {
                "graphid": data.get('graphid')[0],
                "width": int(data.get('width')[0]),
                "height": int(data.get('height')[0]),
                "gitems" : gitems
        }
        print(params)
        try:
            zapi.graph.update(params)
            return HttpResponse('更新成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
    else:
        return render(request, 'graph/update.html')


def get_graph_item(request, graphids):
    graph_items = zapi.graphitem.get(output="extend", graphids=graphids)
    graph_list = []
    for i in graph_items:
        graph_list.append(json.dumps(i))
    return HttpResponse(graph_list)
