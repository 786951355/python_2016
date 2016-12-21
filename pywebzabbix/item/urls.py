from django.conf.urls import url,include
from . import views

app_name = 'item'
urlpatterns = [
    url(r'^get/$', views.get, name="get"),
    url(r'^create/$', views.create, name="create"),
    url(r'^update/$', views.update, name="update"),
    url(r'^delete/$', views.delete, name="delete"),
]