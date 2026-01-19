"""
URL configuration for tdist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('log/<int:batch_id>/', views.log, name='log'),
    path('create-batch/', views.create_batch, name='create_batch'),
    path('batch/<int:batch_id>/record/create/<str:section>/<int:index>/', views.create_record, name='create_record'),
    path('batch/<int:batch_id>/record/edit/<int:record_id>/', views.edit_record, name='edit_record'),
    path('batch/<int:batch_id>/export/', views.export_batch_csv, name='export_batch_csv'),
    path('full-log/', views.full_log, name='full_log'),
    path('admin/', admin.site.urls),
]
