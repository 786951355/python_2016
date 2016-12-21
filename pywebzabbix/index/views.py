from django.shortcuts import render
from collections import OrderedDict

url = 'http://192.168.1.48:8000'
menus = OrderedDict(
    {
            '主机组': [{'获取所有主机组': url + '/hostgroup/gethostgroup'}, {'获取组中所有主机': url + '/hostgroup/gethosts'}, {'创建主机组': url + '/hostgroup/creategroup'}, {'删除主机组': url + '/hostgroup/delgroup'}],
            '主机': [{'获取主机items': url + '/host/gethostitems'}, {'创建主机': url + '/host/create'}, {'删除主机': url + '/host/delete'}, {'更新主机': url + '/host/update'}],
            '图像': [{'创建图像': url + '/graph/create'}, {'删除图像': url + '/graph/delete'}, {'更新图像': url + '/graph/update'}, {'查询图像': url + '/graph/get'}],
            '屏幕': [{'创建屏幕': url + '/screen/create'}, {'删除屏幕': url + '/screen/delete'},{ '更新屏幕': url + '/screen/update'}, {'查询屏幕': url + '/screen/get'} ],
            '屏幕item' : [{'创建': url + '/screenitem/create'}, {'删除': url + '/screenitem/delete'}, {'查询': url + '/screenitem/get'}, {'更新': url + '/screenitem/update'}],
            '模板': [{'查询': url + '/template/get'}, {'创建': url + '/template/create'}, {'删除': url + '/template/delete'},{'更新': url + '/template/update'} ],
            'Item': [{'查询': url + '/item/get'}, {'创建': url + '/item/create'}, {'删除': url + '/item/delete'},{'更新': url + '/item/update'}]
    })

def index(request):
    return render(request, 'index/index.html')

def nav(request):
    return render(request, 'index/nav.html', {'menus': menus, 'header': '菜单列表'})

# Create your views here.
