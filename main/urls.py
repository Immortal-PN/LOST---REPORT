from django.urls import path
from . import views


urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # ITEMS
    path('lost/', views.lost_items, name='lost_items'),
    path('found/', views.found_items, name='found_items'),
    path('lost/<int:item_id>/delete/', views.delete_lost_item, name='delete_lost_item'),
    path('found/<int:item_id>/delete/', views.delete_found_item, name='delete_found_item'),

    # REPORT
    path('report-lost/', views.report_lost, name='report_lost'),
    path('report-found/', views.report_found, name='report_found'),

    # USER
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # MESSAGES
    path('inbox/', views.inbox, name='inbox'),
    path('contact/<int:user_id>/', views.contact_user, name='contact_user'),

]
