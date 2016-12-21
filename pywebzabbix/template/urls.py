from django.conf.urls import url
from . import views

app_name = 'template'

urlpatterns = [
    url(r'get/', views.get, name='get'),
    url(r'create/', views.create, name='create'),
    url(r'delete/', views.delete, name='delete'),
    url(r'update/', views.update, name='update'),
]

