"""Audio_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path

from audioapp import views

urlpatterns = [

    path('add_file/<str:audioFileType>/', views.add_file, name="add_file"),
    path('update_file/<str:audioFileType>/<int:audioFileID>/', views.update_file, name="update_file"),
    url(r'^get_file/(?P<audioFileType>\w{1,10})(?:/(?P<audioFileID>\d+))?/$', views.get_file, name="get_file"),
    path('delete_file/<str:audioFileType>/<int:audioFileID>/', views.delete_file, name="delete_file"),
]
