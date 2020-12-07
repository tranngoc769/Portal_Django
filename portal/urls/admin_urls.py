from django.urls import path
from ..views import admin_views as views
urlpatterns = [
    path('', views.index, name='index'),
    path('them_nguoidung/', views.them_nguoidung, name='them_nguoidung'),
    path('xoa_nguoidung/<int:nguoidungID>', views.xoa_nguoidung, name='xoa_nguoidung'),
    path('sinhvien/', views.quanly_sinhvien, name='quanly_sinhvien'),
    path('sinhvien/<trang>', views.quanly_sinhvien, name='quanly_sinhvien'),
    path('giangvien/', views.quanly_giangvien, name='quanly_giangvien'),
    path('giangvien/<trang>', views.quanly_giangvien, name='quanly_giangvien'),
    
]