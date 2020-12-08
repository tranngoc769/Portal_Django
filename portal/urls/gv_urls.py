from django.urls import path
from ..views import gv_views as views
urlpatterns = [
    path('', views.index, name='index'),
    # Path Người dùng
    # path('them_nguoidung/', views.them_nguoidung, name='them_nguoidung'),
    # path('xoa_nguoidung/<int:nguoidungID>', views.xoa_nguoidung, name='xoa_nguoidung'),
    # path('sua_nguoidung/<int:nguoidungID>', views.sua_nguoidung, name='sua_nguoidung'),
    # path('sinhvien/', views.quanly_sinhvien, name='quanly_sinhvien'),
    # path('sinhvien/<trang>', views.quanly_sinhvien, name='quanly_sinhvien'),
    # path('giangvien/', views.quanly_giangvien, name='quanly_giangvien'),
    # path('giangvien/<trang>', views.quanly_giangvien, name='quanly_giangvien'),

    # Path đề tài
    path('detai/', views.ds_detai, name='ds_detai'),
    path('detai/<trang>', views.ds_detai, name='ds_detai'),
    path('detai/chitiet/<int:detaiID>', views.chitiet_detai, name='chitiet_detai'),
]