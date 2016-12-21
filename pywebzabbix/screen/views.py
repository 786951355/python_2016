from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi, ZabbixAPIException


def index(request):
    pass


def get(request):
    if request.method == 'POST':
        screen_id = request.POST.get('screenid', '')
        if screen_id:
            screen_list = zapi.screen.get(output="extend", screenids=screen_id)
            return render(request, 'screen/screens.html', {'screen_list': screen_list})
        screen_list = zapi.screen.get(output="extend", screenids=screen_id)
        return render(request, 'screen/screens.html', {'screen_list': screen_list})
    else:
        return render(request, 'screen/get.html')

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
        print(params)
        try:
            zapi.screen.create(params)
            return HttpResponse('创建成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse(e)
        return HttpResponse('test')
    else:
        return render(request, 'screen/create.html')


def delete(request):
    return render(request, 'screen/delete.html')


def update(request):
    return render(request, 'screen/update.html')
