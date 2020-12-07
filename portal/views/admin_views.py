from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from portal.models import NGUOIDUNG
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core import serializers
from portal.models import *
import hashlib
import math
from django.core.serializers.json import DjangoJSONEncoder
import json
MoiTrang = 3
def kiemTraCookie(request):
    print(request)
def index(request):
    return redirect('sinhvien/')
@csrf_exempt
def xoa_nguoidung(request, nguoidungID):
      if (request.method== "POST"):
            try:
                  # NGUOIDUNG.objects.filter(id=id).delete()      
                  return HttpResponse(json.dumps({'code': 200, 'msg': 'success'}))
            except:
                  pass
      return HttpResponse(json.dumps({'code': 403, 'msg': 'Not allow method'}))
@csrf_exempt
def them_nguoidung(request):
    # Giống hệt đăng ký
    if request.method == "GET":
        return render(request, 'portal/admin/them_nguoidung.html')
    if request.method == "POST":
        # Lấy dữ liệu đăng ký dưới dạng Objects
        thongTinTao = json.loads(request.body)
        # 'SDT': '123', 'Email': '1234@gmail.com', 'GioiTinh': '0', 'NgaySinh': '2020-12-10', 'MatKhau': 'password', 'Quyen': 3}
        maHoaMatKhau = hashlib.md5(thongTinTao.get(
            'MatKhau').encode()).hexdigest()  # Mã hóa mật khẩu md5
        # Các thao tác validate ở đây
        try:
            nguoiDungDk = NGUOIDUNG(TenNguoiDung=thongTinTao.get('TenNguoiDung'), HoTen=thongTinTao.get('HoTen'), SDT=thongTinTao.get(
                'SDT'), MatKhau=maHoaMatKhau, Email=thongTinTao.get('Email'), NgaySinh=thongTinTao.get('NgaySinh'), GioiTinh=thongTinTao.get('GioiTinh'), Quyen=thongTinTao.get('Quyen'))
            nguoiDungDk.save()
        except Exception as insertErr:
            resp = {"code": 404}
            resp['msg'] = str(insertErr)
            return HttpResponse(json.dumps(resp))
        resp = {"code": 200}
        resp['msg'] = "success"
        return HttpResponse(json.dumps(resp))
    return HttpResponse(json.dumps({'code': 403, 'msg': 'Not allow method'}))
def quanly_sinhvien(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    dsSinhVien_phanTrang = danhSachNguoiDung(trangHienTai, MoiTrang, 3)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLNguoiDung(dsSinhVien_phanTrang, trangHienTai, 'sinhvien')
    return render(request, 'portal/admin/ql_nguoidung.html', content)
# Hàm logic
def danhSachNguoiDung(trang, moitrang, quyen):
    dsNguoiDung = tatCaNguoiDung(quyen)
    tongNguoiDung = len(dsNguoiDung['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongNguoiDung / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = "SELECT * FROM `portal_nguoidung` WHERE Quyen = {0} LIMIT {1} OFFSET {2}".format(
        quyen, moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsNguoiDung_phanTrang = querySetToJson(NGUOIDUNG.objects.raw(sql))
    dsNguoiDung_phanTrang['SoNguoiDung'] = len(dsNguoiDung['data'])
    dsNguoiDung_phanTrang['SoTrang'] = tongTrang
    return dsNguoiDung_phanTrang
def querySetToJson(rawquerySet):
    # Chuyển rawQuerySet thành dạng Json với các phần tử là các fields
    data = serializers.serialize('json', rawquerySet)
    listData = json.loads(data)  # Chuyển sang JSON
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
    jsonData['data'] = mangPhanTu  # Lưu vào JSON để trả về
    return jsonData  # Trả về  JSON
    # return json.dumps(jsonData)   #Trả về string JSON
def tatCaNguoiDung(quyen):
    danhSachNguoiDung = querySetToJson(NGUOIDUNG.objects.raw(
        'SELECT * FROM `portal_nguoidung` WHERE Quyen = {0}'.format(quyen)))
    return danhSachNguoiDung
# Hàm tạo dữ liệu json để render vào quanli_nguoidung.html (dùng chung cho cả 3 loại người dùng)
def taoJsonQLNguoiDung(dsNguoiDung, trangHienTai, loaiNguoiDung):
    tongSoTrang = int(dsNguoiDung['SoTrang'])  # Lấy tổng số trang
    if trangHienTai > tongSoTrang:  # Nếu trang yêu cầu > tổng số --> Quay về trang 1
        return redirect('/')
    # Chỗ này hiển thị mấy nút đến trang  1 2 3 4 5 Cuối
    dsTrang = range(trangHienTai - 5, trangHienTai + 5)
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
    tenLoai = ""
    if loaiNguoiDung == 'admin':
        tenLoai = "admin"
    if loaiNguoiDung == 'giangvien':
        tenLoai = "giảng viên"
    if loaiNguoiDung == 'sinhvien':
        tenLoai = "sinh viên"
    content = {
        'NguoiDung': loaiNguoiDung,
        'LoaiNguoiDung': tenLoai,
        'DS_NguoiDung': dsNguoiDung['data'],
        'TongNguoiDung': dsNguoiDung['SoNguoiDung'],
        'SoTrang': dsTrang,
        'TrangHienTai': trangHienTai,
        'TongTrang': tongSoTrang,
        'SoNguoiDung': len(dsNguoiDung['data']),
        'TrangSau':  trangSau,
        'TrangTruoc': trangTruoc
    }
    return content
