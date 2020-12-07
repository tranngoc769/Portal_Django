from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from portal.models import NGUOIDUNG
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.core import serializers
from portal.models import  *
import  hashlib
import math
from django.core.serializers.json import DjangoJSONEncoder
import json
MoiTrang = 3
def kiemTraCookie(request):
      print(request)
      
def index(request):
      return redirect('sinhvien/')

def quanly_sinhvien(request, trang = 1): # Mặc định trang = 1
      trangHienTai = int(trang)
      dsSinhVien_phanTrang = danhSachSinhVien(trangHienTai,MoiTrang) #Lấy danh sách sinh viên theo trang / mỗi trang 
      tongSoTrang = int(dsSinhVien_phanTrang['SoTrang']) #Lấy tổng số trang
      if trangHienTai > tongSoTrang: #Nếu trang yêu cầu > tổng số --> Quay về trang 1
            return redirect('/')
      dsTrang = range(trangHienTai - 5, trangHienTai +5) #Chỗ này hiển thị mấy nút đến trang  1 2 3 4 5 Cuối
      if (trangHienTai-5 < 1):
            dsTrang = range(1, 11)
      if (trangHienTai + 5 > tongSoTrang):
            dsTrang = range(tongSoTrang-10, tongSoTrang+1)
      if (tongSoTrang < 10):
            dsTrang = range(1, tongSoTrang+1)
      trangSau = trangHienTai + 1
      if trangHienTai > tongSoTrang:
            trangHienTai = tongSoTrang
      trangTruoc = trangHienTai - 1
      if trangTruoc < 1:
            trangTruoc = 1
      # Tạo Json để render ra HTML 
      content = {
        'DS_SinhVien' : dsSinhVien_phanTrang['data'],
        'TongSinhVien' : dsSinhVien_phanTrang['SoSinhVien'],
        'SoTrang' : dsTrang,
        'TrangHienTai' : trangHienTai,
        'TongTrang' : tongSoTrang,
        'SoSinhVien' : len(dsSinhVien_phanTrang['data']),
        'TrangSau' :  trangSau,
        'TrangTruoc' : trangTruoc
       }
      return render(request,'portal/admin/ql_sinhvien.html',content)


# Hàm logic 

def danhSachSinhVien(trang, moitrang):
      dsSinhVien = tatCaSinhVien()
      tongSV = len(dsSinhVien['data'])
      tongTrang = math.ceil(tongSV / moitrang)# Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
      if (trang > tongTrang):
            trang = tongTrang #VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
      if (trang < 1):
            trang = 1 #VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
      sql = "SELECT * FROM `portal_nguoidung` WHERE Quyen = 3 LIMIT {0} OFFSET {1}".format(moitrang, (trang-1)*moitrang) # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
      dsSinhVien_phanTrang = querySetToJson(NGUOIDUNG.objects.raw(sql))
      dsSinhVien_phanTrang['SoSinhVien'] = len(dsSinhVien['data'])
      dsSinhVien_phanTrang['SoTrang'] = tongTrang
      return dsSinhVien_phanTrang
def querySetToJson(rawquerySet):
      data = serializers.serialize('json', rawquerySet) #Chuyển rawQuerySet thành dạng Json với các phần tử là các fields 
      listData = json.loads(data) #Chuyển sang JSON
      jsonData = {}
      mangPhanTu = []
      for phanTu in listData:
            # Với mỗi field --> lấy đoạn json chứa thông tin (rows) của tables, lưu vào mảng
            try:
                  phanTu['fields']['id'] = phanTu['pk']
                  # thêm id vô fields
            except:
                  pass
            mangPhanTu.append(phanTu['fields'])
      jsonData['data'] = mangPhanTu #Lưu vào JSON để trả về
      return jsonData   #Trả về  JSON
      # return json.dumps(jsonData)   #Trả về string JSON
def tatCaSinhVien():
      danhSachSinhVien = querySetToJson(NGUOIDUNG.objects.raw('SELECT * FROM `portal_nguoidung` WHERE Quyen = 3'))
      return danhSachSinhVien