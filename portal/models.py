from django.db import models
from django.contrib.auth.models import AbstractUser
# NGUOIDUNG
class  NGUOIDUNG(models.Model):
      IdUser = models.IntegerField(primary_key=True,auto_created=True)
      TenNguoiDung = models.CharField(max_length=20, null=False)
      HoTen = models.CharField(max_length=200, null=False)
      MatKhau = models.CharField(max_length=200, null=False)
      Email = models.CharField(max_length=200, null=False)
      SDT = models.CharField(max_length=200, null=True)
      Quyen = models.IntegerField(null=False)
      SDT = models.CharField(max_length=15, null=True)
      # 
      NgaySinh = models.DateTimeField(null=True)
      GioiTinh = models.IntegerField(default=1)
      HoatDong = models.BooleanField(default = True)
# DETAI
class  DETAI(models.Model):
      IdDeTai = models.IntegerField(primary_key=True,auto_created=True)
      IdUser = models.IntegerField(null = False)
      TenDeTai = models.CharField(max_length=1000, null=False, default="")
      ChiTiet = models.CharField(max_length=1000, null=False)
      NgayBD = models.DateTimeField(null=False)
      NgayKT = models.DateTimeField(null=False)
      SoLuong = models.IntegerField(null=False, default=2)
      IdLoai = models.IntegerField(null=False)
      HoatDong = models.BooleanField(default = True)
# HOATDONG
class  HOATDONG(models.Model):
      IdHoatDong = models.IntegerField(primary_key=True,auto_created=True)
      IdUser = models.IntegerField(null = False)
      ChiTiet = models.CharField(max_length=1000, null=False)
      NgayBD = models.DateTimeField(null=False)
      NgayKT = models.DateTimeField(null=False)
      SoLuong = models.IntegerField(null=False, default=50)
      IdDiaDiem = models.IntegerField(null=False)
      IdGiaiThuong = models.IntegerField(null=False)
      HoatDong = models.BooleanField(default = True)
# DETAIDADANGKY
class  DETAIDADANGKY(models.Model):
      IdDTDDK = models.IntegerField(primary_key=True,auto_created=True)
      IdDeTai = models.IntegerField(null = False)
      IdUser = models.IntegerField(null = False)
      NgayDKDT = models.DateTimeField(null=False)
# HOATDONGDADANGKY
class  HOATDONGDADANGKY(models.Model):
      IdHDDDK = models.IntegerField(primary_key=True,auto_created=True)
      IdHoatDong = models.IntegerField(null = False)
      IdUser = models.IntegerField(null = False)
      NgayDKHD = models.DateTimeField(null=False)
# LOAIDETAI
class  LOAIDETAI(models.Model):
      IdLoai = models.IntegerField(primary_key=True,auto_created=True)
      TenLoai = models.CharField(max_length=100, null=False)
      DiemSan = models.FloatField(null=False)
# DIADIEM
class  DIADIEM(models.Model):
      IdDiaDiem = models.IntegerField(primary_key=True,auto_created=True)
      TenDiaDiem= models.CharField(max_length=100, null=False)
      ChiTiet = models.CharField(max_length=1000)
# GIAITHUONG
class  GIAITHUONG(models.Model):
      IdGiaiThuong = models.IntegerField(primary_key=True,auto_created=True)
      TenGiaiThuong= models.CharField(max_length=100, null=False)
      ChiTiet = models.CharField(max_length=1000)
# THONGBAO
class  THONGBAO(models.Model):
      IdThongBao = models.IntegerField(primary_key=True,auto_created=True)
      IdUser = models.IntegerField(null = False)
      ChiTiet = models.CharField(max_length=1000)
      NgayThongBao = models.DateTimeField(null=False)

