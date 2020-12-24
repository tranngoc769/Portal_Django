
import openpyxl
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
from . import chucnang as ChucNang
MoiTrang = 3
def kiemTraCookie(request):
    print(request)
def index(request):
    return redirect('sinhvien/')
@csrf_exempt
def xoa_nguoidung(request, nguoidungID):
      if (request.method== "POST"):
            try:
                NGUOIDUNG.objects.filter(pk=nguoidungID).update(HoatDong=False)  
                return HttpResponse(json.dumps({'code': 200, 'msg': 'success'}))
            except:
                return HttpResponse(json.dumps({'code': 403, 'msg': 'Không thể xóa người dùng'}))
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
# 
@csrf_exempt
def sua_nguoidung(request, nguoidungID):
    # Giống hệt đăng ký
    if request.method == "GET":
        thongTinNguoiDungList = NGUOIDUNG.objects.filter(pk=nguoidungID).values()
        if (len(thongTinNguoiDungList)< 1):
            return HttpResponse(json.dumps({'code': 404, 'msg': 'User not found'}))
        thongTinNguoiDung = thongTinNguoiDungList[0]
        print(thongTinNguoiDung)
        return render(request, 'portal/admin/sua_nguoidung.html', thongTinNguoiDung)
    if request.method == "POST":
        thongTinUpdate = json.loads(request.body)
        try:
            NGUOIDUNG.objects.filter(pk=nguoidungID).update(Email =thongTinUpdate.get('Email') ,GioiTinh= thongTinUpdate.get('GioiTinh') ,HoTen= thongTinUpdate.get('HoTen') ,NgaySinh= thongTinUpdate.get('NgaySinh') ,Quyen= thongTinUpdate.get('Quyen') ,SDT= thongTinUpdate.get('SDT'))  
            if (thongTinUpdate.get('MatKhau')!=""):
                NGUOIDUNG.objects.filter(pk=nguoidungID).update(MatKhau = hashlib.md5(thongTinUpdate.get('MatKhau').encode()).hexdigest()) # Mã hóa mật khẩu md5
        except Exception as insertErr:
            resp = {"code": 404}
            resp['msg'] = str(insertErr)
            return HttpResponse(json.dumps(resp))
        resp = {"code": 200}
        resp['msg'] = "success"
        return HttpResponse(json.dumps(resp))
    return HttpResponse(json.dumps({'code': 403, 'msg': 'Not allow method'}))
# 
def quanly_sinhvien(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    dsSinhVien_phanTrang = danhSachNguoiDung(trangHienTai, MoiTrang, 3)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLNguoiDung(dsSinhVien_phanTrang, trangHienTai, 'sinhvien')
    return render(request, 'portal/admin/ql_nguoidung.html', content)
def quanly_giangvien(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    dsGiangVien_phanTrang = danhSachNguoiDung(trangHienTai, MoiTrang, 2)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLNguoiDung(dsGiangVien_phanTrang, trangHienTai, 'giangvien')
    return render(request, 'portal/admin/ql_nguoidung.html', content)

def quanly_thongbao(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    dsThongBao_phanTrang = danhSachThongBao(trangHienTai, MoiTrang)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLNguoiDung(dsThongBao_phanTrang, trangHienTai, 'thongbao')
    return render(request, 'portal/admin/ql_thongbao.html', content)

def danhSachThongBao(trang, moitrang,search=""):
    dsDetai = tatCaThongBao(search)
    tongDetai = len(dsDetai['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongDetai / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = """SELECT * from portal_thongbao where portal_thongbao.ChiTiet LIKE '%{0}%' OR portal_thongbao.TieuDe LIKE '%{1}%'
            LIMIT {2} OFFSET {3}
            """.format(search,search,moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = ChucNang.TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsDetai['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
def tatCaThongBao(search=""):
    danhSachDeTai = ChucNang.TruyVanDuLieu("""SELECT * from portal_thongbao where portal_thongbao.ChiTiet LIKE '%{0}%' OR portal_thongbao.TieuDe LIKE '%{1}%'""".format(search,search))
    return danhSachDeTai
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
    sql = "SELECT * FROM `portal_nguoidung` WHERE Quyen = {0} AND HoatDong = 1 LIMIT {1} OFFSET {2}".format(
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
        'SELECT * FROM `portal_nguoidung` WHERE Quyen = {0}  AND HoatDong = 1'.format(quyen)))
    return danhSachNguoiDung
# Hàm tạo dữ liệu json để render vào quanli_nguoidung.html (dùng chung cho cả 3 loại người dùng)
def taoJsonQLNguoiDung(dsNguoiDung, trangHienTai, loaiNguoiDung):
    tongSoTrang = int(dsNguoiDung['SoTrang'])  # Lấy tổng số trang
    if (tongSoTrang ==0):
              tongSoTrang = 1
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
    if loaiNguoiDung == 'thongbao':
              tenLoai = "thông báo"
    tongso = 0
    try:
        tongso = dsNguoiDung['SoNguoiDung']
    except:
        tongso = dsNguoiDung['SoDeTai']
    content = {
        'NguoiDung': loaiNguoiDung,
        'LoaiNguoiDung': tenLoai,
        'DS_NguoiDung': dsNguoiDung['data'],
        'TongNguoiDung': tongso,
        'SoTrang': dsTrang,
        'TrangHienTai': trangHienTai,
        'TongTrang': tongSoTrang,
        'SoNguoiDung': len(dsNguoiDung['data']),
        'TrangSau':  trangSau,
        'TrangTruoc': trangTruoc
    }
    return content
# 
@csrf_exempt
def importExcel(request, loai):
    if request.method == "POST":
        if (len(request.FILES) < 1):
            return HttpResponse(json.dumps({'code': 403, 'msg': 'No file'}))
        
        try:
            excel_file = request.FILES["file"]
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb.worksheets[0]
            excel_data = list()
            count = 0
            for row in worksheet.iter_rows():
                if (count == 0):
                    count = 1
                    continue
                sql = ""
                checksql = "SELECT IdUser FROM portal_nguoidung WHERE TenNguoiDung='{0}' LIMIT 1 ".format(row[1].value)
                temp = ChucNang.TruyVanDuLieu(checksql)
                if (len(temp['data']) == 1):
                    sql = """
                    UPDATE portal_nguoidung SET HoTen = '{0}', Email= '{1}' ,SDT= '{2}',    GioiTinh= {3},  Khoa= '{4}',     NgaySinh = '{5}', HoatDong = {6} WHERE TenNguoiDung='{7}'
                    """.format(                 row[2].value,   row[3].value,row[4].value,  row[7].value,   row[5].value,       row[6].value,  row[8].value,        row[1].value)
                else:
                    sql = """ 
                    INSERT INTO portal_nguoidung(HoTen,MatKhau,Email,Quyen,SDT,NgaySinh,GioiTinh,TenNguoiDung,HoatDong,Khoa) VALUES ('{0}', '{1}', '{2}', {3}, '{4}', '{5}', {6}, '{7}', 1, {8})
                    """.format(row[2].value, row[1].value, row[3].value, 3, row[4].value,  row[6].value, row[7].value, row[1].value,1,  row[8].value)
                ChucNang.UpdateDuLieu(sql)
                checksql = "SELECT * FROM portal_diemtrungbinh WHERE userID='{0}' LIMIT 1 ".format(row[1].value)
                temp = ChucNang.TruyVanDuLieu(checksql)
                if (len(temp['data']) == 1):
                          sql = """
                    UPDATE portal_diemtrungbinh SET Diem = '{0}' WHERE userID='{1}'
                    """.format(row[9].value, row[1].value)
                else:
                    sql = """ 
                    INSERT INTO portal_diemtrungbinh(userID,Diem) VALUES ('{0}', {1})
                    """.format(row[0].value,row[9].value)
                ChucNang.UpdateDuLieu(sql)
                # Id,  1                  2             3         4             5         6                  7            8         9
                # Id,  TenNguoiDung     HoTen       Email       SDT         Khoa         NgaySinh           GioiTinh  HoatDong   Diem
            #    ['2', '2033172027', 'Võ Phú Hải', 'phuhai113@gmail.com', 'None', '08', '1998-10-10 00:00:00', 'None', '1', '9.33']
        except Exception as insertErr:
            resp = {"code": 404}
            resp['msg'] = str(insertErr)
            return HttpResponse(json.dumps(resp))
        resp = {"code": 200}
        resp['msg'] = "success"
        return HttpResponse(json.dumps(resp))
    return HttpResponse(json.dumps({'code': 403, 'msg': 'Not allow method'}))
# 
# Chi tiet thong bao 
def chitiet_thongbao(request, idTB):
    sql = "SELECT * FROM portal_thongbao WHERE IdThongBao={0}".format(idTB)
    data = ChucNang.TruyVanDuLieu(sql)
    chitiet = data['data'][0]
    return render(request, 'portal/admin/chitiet_thongbao.html', {'ThongBao':chitiet})
# Chi tiet thong bao 

@csrf_exempt
def sua_thongbao(request, idTB):
    if request.method == "GET":
        sql = "SELECT * FROM portal_thongbao WHERE IdThongBao={0}".format(idTB)
        data = ChucNang.TruyVanDuLieu(sql)
        chitiet = data['data'][0]
        return render(request, 'portal/admin/sua_thongbao.html', {'ThongBao':chitiet})
    else:
        tenHoatDong = request.POST['tenThongBao']
        Ngay = request.POST['ngayKTHD']
        ChiTiet = request.POST['chiTietHD']
        jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Sửa thông báo thành công', 'backlink': '/admin/sua_thongbao/{0}'.format(idTB)}
        updatesql = "UPDATE portal_thongbao SET ChiTiet  = '{0}',  TieuDe = '{1}',  NgayThongBao = '{2}' WHERE  IdThongBao  = {3}".format(ChiTiet,tenHoatDong, Ngay,idTB)
        try:
            ChucNang.UpdateDuLieu(updatesql)
        except Exception as exc:
            jsonRender['ChiTiet'] = str(exc)
            jsonRender['ThongBao'] = str("Không thành công")
        return render(request, 'portal/giangvien/thongbao.html', jsonRender)