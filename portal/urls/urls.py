from django.urls import path
from ..views import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dsdetai/', views.dsDetai, name='dsDetai'),
    path('dshoatdong/', views.dshoatdong, name='dshoatdong'),
    path('dangnhap/',views.dangnhap, name="dangnhap"),
    path('dangki/',views.dangki, name="dangki"),
    path('dangxuat/',views.dangxuat, name="dangxuat"),
    path('chitietdetai/<int:detaiID>', views.chitietdetai, name='chitietdetai'),
    path('dkdetai/<int:detaiID>', views.dkdetai, name='dkdetai'),
    path('chitiethoatdong/<int:hoatdongID>', views.chitiethoatdong, name='chitiethoatdong'),
    path('dkhoatdong/<int:hoatdongID>', views.dkhoatdong, name='dkhoatdong'),

    path('dshoatdongcuatoi/', views.dshoatdongcuatoi, name='dshoatdongcuatoi'),
    path('dsdetaicuatoi/', views.dsdetaicuatoi, name='dsdetaicuatoi'),
    path('dsthongbao/', views.dsthongbao, name='dsthongbao'),
    path('chitietthongbao/<int:id>', views.chitietthongbao, name='chitietthongbao'),
]