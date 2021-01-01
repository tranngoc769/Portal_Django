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
      Khoa = models.IntegerField(null=False, default=0)
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
      DaDangKi = models.IntegerField(null=False, default=0)
      IdLoai = models.IntegerField(null=False)
      IdKhoa = models.IntegerField(null=False)
      HoatDong = models.BooleanField(default = True)
      DangThucHien = models.BooleanField(null=True, default = False)
# HOATDONG
class  HOATDONG(models.Model):
      IdHoatDong = models.IntegerField(primary_key=True,auto_created=True)
      TenHoatDong = models.CharField(max_length=1000)
      IdUser = models.IntegerField(null = False)
      ChiTiet = models.CharField(max_length=1000, null=False)
      NgayBD = models.DateTimeField(null=False)
      NgayKT = models.DateTimeField(null=False)
      SoLuong = models.IntegerField(null=False, default=50)
      DaDangKi = models.IntegerField(null=False, default=0)
      DiemRL = models.IntegerField(null=False,default=0)
      Ki = models.IntegerField(null=False, default= 1)
      HoatDong = models.BooleanField(default = True)
      Loai = models.IntegerField(default=1)
      DangThucHien = models.BooleanField(null=True, default = False)
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
      DaChamDiem = models.IntegerField(default=0)
      NgayDKHD = models.DateTimeField(null=False)
# LOAIDETAI
class  LOAIDETAI(models.Model):
      IdLoai = models.IntegerField(primary_key=True,auto_created=True)
      TenLoai = models.CharField(max_length=100, null=False)
# KHOA
class  KHOA(models.Model):
      IdKhoa = models.IntegerField(primary_key=True,auto_created=True)
      TenKhoa = models.CharField(max_length=100, null=False)
# GIAITHUONG
class  GIAITHUONG(models.Model):
      IdGiaiThuong = models.IntegerField(primary_key=True,auto_created=True)
      TenGiaiThuong= models.CharField(max_length=100, null=False)
      ChiTiet = models.CharField(max_length=1000)
# THONGBAO
class  THONGBAO(models.Model):
      IdThongBao = models.IntegerField(primary_key=True,auto_created=True)
      ChiTiet = models.CharField(max_length=1000)
      TieuDe = models.CharField(max_length=200)
      NgayThongBao = models.DateTimeField(null=False)
# DieuKienDK
class DIEUKIENDANGKY(models.Model):
      Id = models.IntegerField(primary_key=True,auto_created=True)
      IdLoai = models.IntegerField(null= False)
      IdKhoa = models.IntegerField(null= False)
      Diem = models.FloatField(default=0)
class DIEMTRUNGBINH(models.Model):
      userID = models.IntegerField(primary_key=True)
      Diem = models.FloatField(default=0)
class DIEMRENLUYEN(models.Model):
      idDiem = models.IntegerField(primary_key=True,auto_created=True)
      hoatDongId = models.IntegerField(default=0)
      userID = models.IntegerField()
      Diem = models.FloatField(default=0)
      Ki = models.IntegerField(default=1)
# LOAIHOATDONG
class LOAIHD(models.Model):
      idLoaiHD = models.IntegerField(primary_key=True, auto_created=True)
      TenLoaiHD = models.CharField(max_length=1000)