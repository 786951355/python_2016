from django.shortcuts import render
from django.http import HttpResponse
from zabbix import zapi, ZabbixAPIException


def index(request):
    return HttpResponse('graph index')

def get(request):
    if request.method == 'POST':
        hostid = request.POST.get('hostid', None)
        if hostid is None:
            return HttpResponse('hostid is not none')
        items = zapi.item.get(output="extend", hostids=hostid, sortfield="name")
        return render(request, 'item/items.html', {'items': items, 'hostid': hostid})
    else:
        return render(request, 'item/get.html')


def create(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname')
        itemname = request.POST.get('itemname')
        type = int(request.POST.get('type', '0'))
        keyname = request.POST.get('keyname', '')
        keyvalue = request.POST.get('keyvalue','')
        valuetype = request.POST.get('valuetype', 3)
        delay = int(request.POST.get('delay', 30))
        startkeyvalue = int(request.POST.get('startkeyvalue'))
        endkeyvalue = int(request.POST.get('endkeyvalue'))

        hosts = zapi.host.get(filter={"host": hostname}, selectInterfaces=["interfaceid"])
        if hosts:
            host_id = hosts[0]["hostid"]
            print("Found host id {0}".format(host_id))

            try:
                for i in range(startkeyvalue, endkeyvalue+1):
                    item = zapi.item.create(
                        hostid=host_id,
                        name='{}{}'.format(itemname, i),
                        key_='{}[{}{}]'.format(keyname, keyvalue, i),
                        type=type,
                        value_type=valuetype,
                        interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
                        delay=delay
                    )
            except ZabbixAPIException as e:
                print(e)
                return HttpResponse('数据有错误，请检查后重新提交')
            return HttpResponse("Added item with itemid {0} to host: {1} success".format(item["itemids"][0], hostname))
        else:
            return HttpResponse("没有查找到相关主机")
    else:
        return render(request, 'item/create.html')


def delete(request):
    if request.method == 'POST':
        items = request.POST.get('itemlist', None)
        if items is None:
            return HttpResponse('item列表不能为空')
        try:
            zapi.item.delete(*items.split(','))
            return HttpResponse('删除成功')
        except ZabbixAPIException as e:
            print(e)
            return HttpResponse('删除失败')
    else:
        return render(request, 'item/delete.html')

def update(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'item/update.html')
# Create your views here.
