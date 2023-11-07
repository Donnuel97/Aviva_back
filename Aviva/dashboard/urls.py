from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
   
    path('Pending', PendingListView.as_view(), name='pending'),
    path('Analytics', AnalyticsView.as_view(), name='analytics'),
    
    
    path('', views.home, name='home'),

    path('login', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 

    path('reviewed', ReviewedListView.as_view(), name='reviewed'),
    path('cervic-data/<int:pk>', CervicDataDetailView.as_view(), name='cervic_data_detail'),
    
   
    path('report', CervicDataFilterView.as_view(), name='report'),
    path('get_facilities/',  GetFacilitiesView.as_view(), name='get_facilities'),
    
]

