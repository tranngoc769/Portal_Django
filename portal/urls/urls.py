from django.urls import path
from ..views import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dsdetai/', views.dsDetai, name='dsDetai'),
    path('dangnhap/',views.dangnhap, name="dangnhap"),
    path('dangki/',views.dangki, name="dangki"),
    path('dangxuat/',views.dangxuat, name="dangxuat"),
    path('chitietdetai/<int:detaiID>', views.chitietdetai, name='chitietdetai'),
    path('dkdetai/<int:detaiID>', views.dkdetai, name='dkdetai'),
   


]