from django.shortcuts import render
from . import views
from django.contrib import admin
from django.urls import path, include


def index(request):
    return render(request, 'main/index.html', {'message': 'Hello, World!'})


urlpatterns = [
    path('', views.index, name='index'),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]
