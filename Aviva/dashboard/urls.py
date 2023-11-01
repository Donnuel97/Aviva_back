from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    #path('Reviewed', views.reviewed, name='reviewed'),
    path('Pending', PendingListView.as_view(), name='pending'),
    path('Analytics', views.dashboard, name='analytics'),
    path('report', views.dashboard, name='report'),
    path('home', views.home, name='home'),

    path('', views.login, name='login'),
    

    path('reviewed', ReviewedListView.as_view(), name='reviewed'),
    path('cervic-data/<int:pk>', CervicDataDetailView.as_view(), name='cervic_data_detail'),
   
    
    path('report', views.filter_cervic_data, name='report'),
   
    path('get_facilities/', views.get_facilities, name='get_facilities'),
]

 