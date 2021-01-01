from django.urls import path
from ..views import admin_views as views
urlpatterns = [
    path('', views.index, name='index'),
    # Path Người dùng
    path('them_nguoidung/', views.them_nguoidung, name='them_nguoidung'),
    path('xoa_nguoidung/<int:nguoidungID>', views.xoa_nguoidung, name='xoa_nguoidung'),
    path('sua_nguoidung/<int:nguoidungID>', views.sua_nguoidung, name='sua_nguoidung'),
    path('sinhvien/', views.quanly_sinhvien, name='quanly_sinhvien'),
    path('sinhvien/<trang>', views.quanly_sinhvien, name='quanly_sinhvien'),
    path('giangvien/', views.quanly_giangvien, name='quanly_giangvien'),
    path('giangvien/<trang>', views.quanly_giangvien, name='quanly_giangvien'),
    # Path thông báo
    path('thongbao/', views.quanly_thongbao, name='quanly_thongbao'),
    path('thongbao/<trang>', views.quanly_thongbao, name='quanly_thongbao'),
    path('import/<loai>', views.importExcel, name='importExcel'),
    path('xoa_thongbao/<int:idTB>', views.xoa_thongbao, name='xoa_thongbao'),
    path('chitiet_thongbao/<int:idTB>', views.chitiet_thongbao, name='chitiet_thongbao'),
    path('sua_thongbao/<int:idTB>', views.sua_thongbao, name='sua_thongbao'),
    path('them_thongbao', views.them_thongbao, name='them_thongbao'),
    # Path hoạt động
    path('dshoatdong/', views.quanly_hoatdong, name='quanlyhoatdong'),
    path('hoatdong/chitiet/<int:id>', views.chitiethoatdong, name='chitiethoatdong'),
    path('hoatdong/diemdanh/', views.diemdanh, name='diemdanh'),
    path('hoatdong/export/<int:id>', views.exportHoatDong, name='export'),
]