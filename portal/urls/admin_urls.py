from django.urls import path
from ..views import admin_views as views
urlpatterns = [
    path('', views.index, name='index'),
    path('sinhvien/', views.quanly_sinhvien, name='quanly_sinhvien'),
]