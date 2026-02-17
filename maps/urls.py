from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.index, name='login'),
    path('portal/', views.portal, name='portal'),
    path('proxy/parcel/', views.parcel_proxy, name='parcel_proxy'),
    path('proxy/landinfo/', views.land_info_proxy, name='land_info_proxy'),
    path('proxy/building-detail/', views.building_detail_proxy, name='building_detail_proxy'),
    path('proxy/floor-info/', views.floor_info_proxy, name='floor_info_proxy'),
    path('proxy/real-price/', views.real_price_proxy, name='real_price_proxy'),
    path('proxy/wfs/', views.wfs_proxy, name='wfs_proxy'),
    path('proxy/warehouse/', views.warehouse_proxy, name='warehouse_proxy'),
    path('proxy/auction/', views.kamco_proxy, name='kamco_proxy'),
    path('proxy/hospital/', views.hospital_proxy, name='hospital_proxy'),
    path('proxy/hospital/detail/', views.hospital_detail_proxy, name='hospital_detail_proxy'),
    path('proxy/hospital/list/', views.hospital_list_proxy, name='hospital_list_proxy'),
]
