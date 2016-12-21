from django.conf.urls import url
from . import views

app_name = 'graph'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'get/', views.get, name='get'),
    url(r'create/', views.create, name='create'),
    url(r'delete/', views.delete, name='delete'),
    url(r'update/', views.update, name='update'),
    url(r'getgraphitems/(?P<graphids>[0-9]+)', views.get_graph_item, name='getgraphitems'),
]
