from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('dangnhap/',views.dangnhap, name="dangnhap"),
    path('dangki/',views.dangki, name="dangki"),
]