from django.conf.urls import url
from . import views

app_name = 'hostgroup'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'nav/', views.nav, name='nav'),
    url(r'gethostgroup/', views.gethostgroup, name='hostgroups'),
    url(r'gethosts/', views.gethosts, name='hosts'),
    url(r'creategroup/', views.creategroup, name='creategroup'),
    url(r'delgroup/', views.delgroup, name='delgroup'),
]
