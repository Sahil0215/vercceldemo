"""
URL configuration for instabill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from bill import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name="main"),
    path('login_page/', views.login_page, name="login_page"),
    path('logout_page/', views.logout_page, name="logout_page"),
    path('register/', views.register, name="register"),
    path('registersuccess/', views.registersuccess, name="registersuccess"),
    path('home/', views.home, name="home"),
    path('manage/', views.manage, name="manage"),
    path('manage_buyer/', views.manage_buyer, name="manage_buyer"),
    path('add_buyer/', views.add_buyer, name="add_buyer"),
    path('delete_buyer/<int:buyer_id>/', views.delete_buyer, name="delete_buyer"),
    path('manage_seller/', views.manage_seller, name="manage_seller"),
    path('add_seller/', views.add_seller, name="add_seller"),
    path('delete_seller/<int:seller_id>/', views.delete_seller, name="delete_seller"),
    path('manage_employee/', views.manage_employee, name="manage_employee"),
    path('add_employee/', views.add_employee, name="add_employee"),
    path('delete_employee/<int:employee_id>/', views.delete_employee, name="delete_employee"),
    path('manage_item/', views.manage_item, name="manage_item"),
    path('add_item/', views.add_item, name="add_item"),
    path('delete_item/<int:item_id>/', views.delete_item, name="delete_item"),
    path('manage_invoice/', views.manage_invoice, name="manage_invoice"),
    path('add_invoice/', views.add_invoice, name="add_invoice"),
    path('delete_invoice/<int:invoice_id>/', views.delete_invoice, name="delete_invoice"),
    path('print_invoice/<int:invoice_id>/', views.print_invoice, name="print_invoice"),
    path('generate/', views.generate, name="generate"),
    path('view/', views.view, name="view"),
    path('entry/', views.entry, name="entry"),
    path('deleteallusers/', views.deleteallusers, name="deleteallusers"),
    path('generatesuccess/', views.generatesuccess, name="generatesuccess"),
]
