from django.urls import path
from . import views

urlpatterns = [

path('', views.home, name='home'),

path('lost-items/', views.lost_items, name='lost_items'),

path('found-items/', views.found_items, name='found_items'),

path('report-lost/', views.report_lost_item, name='report_lost'),

path('report-found/', views.report_found, name='report_found'),

]