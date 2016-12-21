from django.conf.urls import url
from . import views

app_name = 'host'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'gethostitems/', views.gethostitems, name='hostitems'),
    url(r'create/', views.create, name='createhost'),
    url(r'delete/', views.delete, name='deletehost'),
    url(r'update/', views.update, name='updatehost'),
]

