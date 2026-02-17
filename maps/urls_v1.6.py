from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('proxy/parcel/', views.parcel_proxy, name='parcel_proxy'),
    path('proxy/landinfo/', views.land_info_proxy, name='land_info_proxy'),
    path('proxy/building-detail/', views.building_detail_proxy, name='building_detail_proxy'),
    path('proxy/floor-info/', views.floor_info_proxy, name='floor_info_proxy'),

]

