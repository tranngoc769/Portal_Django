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
def kiemTraCookie(request):
      print(request)
      
def index(request):
      return redirect('sinhvien/')

def quanly_sinhvien(request):
      dsSinhVien_phanTrang = danhSachSinhVien(1,5)
      content = {
        'DS_SinhVien' : dsSinhVien_phanTrang['data'],
        'SoTrang' : dsSinhVien_phanTrang['SoTrang'],
        'TrangHienTai' : dsSinhVien_phanTrang['HienTai']
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
      dsSinhVien_phanTrang['SoTrang'] = len(dsSinhVien['data'])
      dsSinhVien_phanTrang['HienTai'] = trang
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