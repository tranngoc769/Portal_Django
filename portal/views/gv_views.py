from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from portal.models import NGUOIDUNG
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core import serializers
from portal.models import *
import hashlib
import math
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json
MoiTrang = 3
from . import chucnang as ChucNang
def index(request):
    return redirect('detai/')
# Hàm lấy danh sách đề tài của tôi phân trang
def danhSachDeTaiCuaToi(trang, moitrang, username,searchString =""):
    dsDetai = tatCaDeTaiCuaToi(username,searchString)
    tongDetai = len(dsDetai['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongDetai / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = """SELECT
                    portal_detai.IdDeTai,
                    portal_detai.TenDeTai,
                    portal_detai.IdUser,
                    portal_detai.ChiTiet,
                    portal_detai.NgayBD,
                    portal_detai.NgayKT,
                    portal_detai.SoLuong,
                    portal_detai.DaDangKi,
                    portal_detai.IdLoai,
                    portal_nguoidung.HoTen,
                    portal_nguoidung.TenNguoiDung,
                    portal_loaidetai.TenLoai,
                    portal_khoa.TenKhoa,
                    portal_detai.DangThucHien
                    FROM
                    portal_detai
                    JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                    JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                    JOIN portal_khoa ON portal_detai.IdKhoa = portal_khoa.IdKhoa
                    WHERE
                    portal_detai.HoatDong = 1 AND
                    portal_nguoidung.HoatDong = 1 AND 
                     portal_detai.TenDeTai LIKE '%{0}%' AND
                    portal_nguoidung.TenNguoiDung = '{1}'
            LIMIT {2} OFFSET {3}
            """.format(searchString, username, moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = ChucNang.TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsDetai['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
# Hàm lấy danh sách hoạt động của tôi phân trang
def danhSachHoaDongCuaToi(trang, moitrang, username,searchString =""):
    dsDetai = tatCaHoatDongCuaToi(username,searchString)
    tongDetai = len(dsDetai['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongDetai / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = """SELECT
                    portal_hoatdong.IdHoatDong,
                    portal_hoatdong.IdUser,
                    portal_hoatdong.ChiTiet,
                    portal_hoatdong.NgayBD,
                    portal_hoatdong.NgayKT,
                    portal_hoatdong.SoLuong,
                    portal_hoatdong.DiemRL,
                    portal_hoatdong.HoatDong,
                    portal_hoatdong.DaDangKi,
                    portal_hoatdong.DangThucHien,
                    portal_hoatdong.TenHoatDong,
                    portal_hoatdong.Ki,
                    portal_nguoidung.HoTen,
                    portal_nguoidung.TenNguoiDung
                    FROM
                    portal_hoatdong
                    JOIN portal_nguoidung ON portal_hoatdong.IdUser = portal_nguoidung.IdUser
                    WHERE
                    portal_hoatdong.HoatDong = 1 AND
                    portal_nguoidung.HoatDong = 1 AND
                    portal_nguoidung.TenNguoiDung = '{2}' AND 
                     portal_hoatdong.TenHoatDong LIKE '%{3}%'
            LIMIT {0} OFFSET {1}
            """.format(moitrang, (trang-1)*moitrang, username, searchString)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = ChucNang.TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsDetai['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
# Hàm lấy danh sách đề tài theo trang
def danhSachDeTai(trang, moitrang,search=""):
    dsDetai = tatCaDeTai(search)
    tongDetai = len(dsDetai['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongDetai / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = """SELECT
                    portal_detai.IdDeTai,
                    portal_detai.TenDeTai,
                    portal_detai.IdUser,
                    portal_detai.ChiTiet,
                    portal_detai.NgayBD,
                    portal_detai.NgayKT,
                    portal_detai.SoLuong,
                    portal_detai.DaDangKi,
                    portal_detai.IdLoai,
                    portal_nguoidung.HoTen,
                    portal_nguoidung.TenNguoiDung,
                    portal_loaidetai.TenLoai,
                    portal_khoa.TenKhoa,
                    portal_detai.DangThucHien
                    FROM
                    portal_detai
                    JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                    JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                    JOIN portal_khoa ON portal_detai.IdKhoa = portal_khoa.IdKhoa
                    WHERE
                    portal_detai.HoatDong = 1 AND
                    portal_nguoidung.HoatDong = 1 AND
                    portal_detai.TenDeTai LIKE '%{0}%'
            LIMIT {1} OFFSET {2}
            """.format(search,moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = ChucNang.TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsDetai['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
def danhSachHoatDong(trang, moitrang,search=""):
    dsHoatDong = tatCaHoatDong(search)
    tongDetai = len(dsHoatDong['data'])
    # Tổng số trang = tổng sinh viên / số sV mỗi trang , làm tròn lên
    tongTrang = math.ceil(tongDetai / moitrang)
    if (trang > tongTrang):
        trang = tongTrang  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    if (trang < 1):
        trang = 1  # VD : tổng 4 trang, yêu cầu trang 4 --> chỉ load tới trang 3
    sql = """SELECT
                    portal_hoatdong.IdHoatDong,
                    portal_hoatdong.IdUser,
                    portal_hoatdong.ChiTiet,
                    portal_hoatdong.NgayBD,
                    portal_hoatdong.NgayKT,
                    portal_hoatdong.SoLuong,
                    portal_hoatdong.DiemRL,
                    portal_hoatdong.HoatDong,
                    portal_hoatdong.DaDangKi,
                    portal_hoatdong.DangThucHien,
                    portal_hoatdong.TenHoatDong,
                    portal_hoatdong.Ki,
                    portal_nguoidung.HoTen,
                    portal_nguoidung.TenNguoiDung
                    FROM
                    portal_hoatdong
                    JOIN portal_nguoidung ON portal_hoatdong.IdUser = portal_nguoidung.IdUser
                    WHERE
                    portal_hoatdong.HoatDong = 1 AND
                    portal_nguoidung.HoatDong = 1  AND 
                    portal_hoatdong.TenHoatDong LIKE '%{0}%'
            LIMIT {1} OFFSET {2}
            """.format(search, moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = ChucNang.TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsHoatDong['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
# Hàm chuyển từ QuerySet --> JSON
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
# Hàm lấy tất cả đề tài (ko bị xóa)
def tatCaDeTai(search=""):
    danhSachDeTai = ChucNang.TruyVanDuLieu("""SELECT
                portal_detai.IdDeTai,
                portal_detai.TenDeTai,
                portal_detai.IdUser,
                portal_detai.ChiTiet,
                portal_detai.NgayBD,
                portal_detai.NgayKT,
                portal_detai.SoLuong,
                portal_detai.DaDangKi,
                portal_detai.IdLoai,
                portal_nguoidung.HoTen,
                portal_nguoidung.TenNguoiDung,
                portal_loaidetai.TenLoai,
                portal_detai.IdKhoa,
                portal_detai.DangThucHien
                FROM
                portal_detai
                JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                WHERE
                portal_detai.HoatDong = 1 AND
                portal_nguoidung.HoatDong = 1 AND
                portal_detai.TenDeTai LIKE '%{0}%'
            """.format(search))
    return danhSachDeTai
# Hàm lấy tất cả hoạt động (ko bị xóa)
def tatCaHoatDong(search=""):
    danhSachDeTai = ChucNang.TruyVanDuLieu("""SELECT
            portal_hoatdong.IdHoatDong,
            portal_hoatdong.IdUser,
            portal_hoatdong.ChiTiet,
            portal_hoatdong.NgayBD,
            portal_hoatdong.NgayKT,
            portal_hoatdong.SoLuong,
            portal_hoatdong.DiemRL,
            portal_hoatdong.HoatDong,
            portal_hoatdong.DaDangKi,
            portal_hoatdong.DangThucHien,
            portal_hoatdong.TenHoatDong,
            portal_hoatdong.Ki,
            portal_nguoidung.HoTen,
            portal_nguoidung.TenNguoiDung
            FROM
            portal_hoatdong
            JOIN portal_nguoidung ON portal_hoatdong.IdUser = portal_nguoidung.IdUser
            WHERE
            portal_hoatdong.HoatDong = 1 AND
            portal_nguoidung.HoatDong = 1  AND 
            portal_hoatdong.TenHoatDong LIKE '%{0}%'
            """.format(search))
    return danhSachDeTai
# Hàm lấy tất cả đè tài theo userID
def tatCaDeTaiCuaToi(username,searchString=""):
    danhSachDeTai = ChucNang.TruyVanDuLieu("""SELECT
        portal_detai.IdDeTai,
        portal_detai.TenDeTai,
        portal_detai.IdUser,
        portal_detai.ChiTiet,
        portal_detai.NgayBD,
        portal_detai.NgayKT,
        portal_detai.SoLuong,
        portal_detai.DaDangKi,
        portal_detai.IdLoai,
        portal_nguoidung.HoTen,
        portal_nguoidung.TenNguoiDung,
        portal_loaidetai.TenLoai,
        portal_detai.IdKhoa,
        portal_detai.DangThucHien
        FROM
        portal_detai
        JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
        JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
        WHERE
        portal_detai.HoatDong = 1 AND
        portal_nguoidung.HoatDong = 1 AND
        portal_nguoidung.TenNguoiDung = '{0}' AND
        portal_detai.TenDeTai LIKE '%{1}%'
    """.format(username, searchString))
    return danhSachDeTai
# Hàm lấy tất cả đè tài theo userID
def tatCaHoatDongCuaToi(username,search=""):
    danhSachDeTai = ChucNang.TruyVanDuLieu("""SELECT
            portal_hoatdong.IdHoatDong,
            portal_hoatdong.IdUser,
            portal_hoatdong.ChiTiet,
            portal_hoatdong.NgayBD,
            portal_hoatdong.NgayKT,
            portal_hoatdong.SoLuong,
            portal_hoatdong.DiemRL,
            portal_hoatdong.HoatDong,
            portal_hoatdong.DaDangKi,
            portal_hoatdong.DangThucHien,
            portal_hoatdong.TenHoatDong,
            portal_hoatdong.Ki,
            portal_nguoidung.HoTen,
            portal_nguoidung.TenNguoiDung
            FROM
            portal_hoatdong
            JOIN portal_nguoidung ON portal_hoatdong.IdUser = portal_nguoidung.IdUser
            WHERE
            portal_hoatdong.HoatDong = 1 AND
            portal_nguoidung.HoatDong = 1 AND
        portal_nguoidung.TenNguoiDung = '{0}' AND 
                     portal_hoatdong.TenHoatDong LIKE '%{1}%'
    """.format(username,search))
    return danhSachDeTai
# Hàm tạo dữ liệu json để render quản lý đề tài
def taoJsonQLDeTai(dsDeTai, trangHienTai, loaiQL):
    tongSoTrang = int(dsDeTai['SoTrang'])  # Lấy tổng số trang
    if (tongSoTrang == 0):
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
    content = {
        'Flag' : loaiQL,
        'DS_DeTai': dsDeTai['data'],
        'TongDeTai': dsDeTai['SoDeTai'],
        'SoTrang': dsTrang,
        'TrangHienTai': trangHienTai,
        'TongTrang': tongSoTrang,
        'SoDeTai': len(dsDeTai['data']),
        'TrangSau':  trangSau,
        'TrangTruoc': trangTruoc
    }
    return content
# Hàm tạo dữ liệu json để render quản lý đề tài
def taoJsonQLHoatDong(dsDeTai, trangHienTai, loaiQL):
    tongSoTrang = int(dsDeTai['SoTrang'])  # Lấy tổng số trang
    if (tongSoTrang == 0):
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
    content = {
        'Flag' : loaiQL,
        'DS_DeTai': dsDeTai['data'],
        'TongDeTai': dsDeTai['SoDeTai'],
        'SoTrang': dsTrang,
        'TrangHienTai': trangHienTai,
        'TongTrang': tongSoTrang,
        'SoDeTai': len(dsDeTai['data']),
        'TrangSau':  trangSau,
        'TrangTruoc': trangTruoc
    }
    return content
# Handle route
def ds_detai(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    dsDeTai_phanTrang = None
    try:
        searchString = request.GET['search']
        dsDeTai_phanTrang = danhSachDeTai(trangHienTai, MoiTrang,searchString)
    except:
        dsDeTai_phanTrang = danhSachDeTai(trangHienTai, MoiTrang)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLDeTai(dsDeTai_phanTrang, trangHienTai, "detai")
    return render(request, 'portal/giangvien/ql_detai.html', content)
# Handle route
def ds_hoatdong(request, trang=1):  # Mặc định trang = 1
    trangHienTai = int(trang)
    dsHoatDong_phanTrang = None
    try:
        searchString = request.GET['search']
        dsHoatDong_phanTrang = danhSachHoatDong(trangHienTai, MoiTrang,searchString)
    except:
        dsHoatDong_phanTrang = danhSachHoatDong(trangHienTai, MoiTrang)
        # Lấy danh sách sinh viên theo trang / mỗi trang
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLDeTai(dsHoatDong_phanTrang, trangHienTai, "hoatdong")
    return render(request, 'portal/giangvien/ql_hoatdong.html', content)
# Quản lí link : /detaicuatoi
def my_detai(request, trang=1):  # Mặc định trang = 1
    userName = request.session.get('TenDangNhap')
    trangHienTai = int(trang)
    dsDeTaiCuaToi_phanTrang = None
    try:
        searchString = request.GET['search']
        dsDeTaiCuaToi_phanTrang = danhSachDeTaiCuaToi(trangHienTai, MoiTrang, userName, searchString)
    except:
        dsDeTaiCuaToi_phanTrang = danhSachDeTaiCuaToi(trangHienTai, MoiTrang, userName)
    # Lấy danh sách sinh viên theo trang / mỗi trang
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLDeTai(dsDeTaiCuaToi_phanTrang, trangHienTai,"detaicuatoi")
    return render(request, 'portal/giangvien/ql_detai.html', content)
def my_hoatdong(request, trang=1):  # Mặc định trang = 1
    userName = request.session.get('TenDangNhap')
    trangHienTai = int(trang)
    dsDeTaiCuaToi_phanTrang = None
    try:
        searchString = request.GET['search']
        dsDeTaiCuaToi_phanTrang = danhSachHoaDongCuaToi(trangHienTai, MoiTrang, userName,searchString)
    except:
    # Lấy danh sách sinh viên theo trang / mỗi trang
        dsDeTaiCuaToi_phanTrang = danhSachHoaDongCuaToi(trangHienTai, MoiTrang, userName)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    content = taoJsonQLHoatDong(dsDeTaiCuaToi_phanTrang, trangHienTai,"hoatdongcuatoi")
    return render(request, 'portal/giangvien/ql_hoatdong.html', content)
# Handle route
def chitiet_detai(request, detaiID):  # Mặc định trang = 1
    sql = """SELECT
                portal_detai.IdDeTai,
                portal_detai.TenDeTai,
                portal_detai.IdUser,
                portal_detai.ChiTiet,
                portal_detai.NgayBD,
                portal_detai.NgayKT,
                portal_detai.SoLuong,
                portal_detai.DaDangKi,
                portal_detai.IdLoai,
                portal_nguoidung.HoTen,
                portal_nguoidung.TenNguoiDung,
                portal_loaidetai.TenLoai,
                portal_detai.IdKhoa,
                portal_detai.DangThucHien
                FROM
                portal_detai
                JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                WHERE
                portal_detai.IdDeTai = {0} AND
                portal_detai.HoatDong = 1 AND
                portal_nguoidung.HoatDong = 1""".format(detaiID)
    queryData = ChucNang.TruyVanDuLieu(sql)
    if (len(queryData['data']))  < 1:
              return HttpResponse("không có dữ liệu")
    thongTinDeTai = queryData['data'][0] # Kết quả query là 1 mảng --> lấy phần tử đầu tiên cũng là duy nhất (id là duy nhất)
    return render(request, 'portal/giangvien/chitiet_detai.html', thongTinDeTai)
# Handle route
def chitiet_hoatdong(request, hoatdongID):
    sql = """SELECT
                    portal_hoatdong.IdHoatDong,
                    portal_hoatdong.IdUser,
                    portal_hoatdong.ChiTiet,
                    portal_hoatdong.NgayBD,
                    portal_hoatdong.NgayKT,
                    portal_hoatdong.SoLuong,
                    portal_hoatdong.DiemRL,
                    portal_hoatdong.HoatDong,
                    portal_hoatdong.DaDangKi,
                    portal_hoatdong.DangThucHien,
                    portal_hoatdong.TenHoatDong,
                    portal_hoatdong.Ki,
                    portal_nguoidung.HoTen,
                    portal_nguoidung.TenNguoiDung
                    FROM
                    portal_hoatdong
                    JOIN portal_nguoidung ON portal_hoatdong.IdUser = portal_nguoidung.IdUser
                    WHERE
                    portal_hoatdong.HoatDong = 1 AND
                portal_hoatdong.IdHoatDong = {0} AND
                portal_nguoidung.HoatDong = 1""".format(hoatdongID)
    queryData = ChucNang.TruyVanDuLieu(sql)
    print(queryData['data'])
    if (len(queryData['data']))  < 1:
              return HttpResponse("không có dữ liệu")
    thongTinDeTai = queryData['data'][0] # Kết quả query là 1 mảng --> lấy phần tử đầu tiên cũng là duy nhất (id là duy nhất)
    return render(request, 'portal/giangvien/chitiet_hoatdong.html', thongTinDeTai)
# Hàm lấy thông tin sinh viên đăng kí đề tài theo DeTaiID
def dsSinhVienDkDeTai(deTaiID):
    sinhVienDKDeTai = ChucNang.TruyVanDuLieu("""
    SELECT
        portal_detaidadangky.IdDTDDK,
        portal_detaidadangky.IdDeTai,
        portal_detaidadangky.IdUser,
        portal_detaidadangky.NgayDKDT,
        portal_nguoidung.HoTen,
        portal_nguoidung.TenNguoiDung,
        portal_nguoidung.Email,
        portal_nguoidung.NgaySinh,
        portal_nguoidung.GioiTinh
        FROM
        portal_detaidadangky
        JOIN portal_nguoidung ON portal_detaidadangky.IdUser = portal_nguoidung.IdUser
        WHERE
        portal_nguoidung.HoatDong = 1 AND
        portal_detaidadangky.IdDeTai = '{0}'
    """.format(deTaiID))
    return sinhVienDKDeTai
# Thêm đề tài
@csrf_exempt  # Tránh lỗi--CSRF token missing or incorrect
def them_detai(request):
    if request.method == "GET":
        khoaSql = "SELECT * FROM portal_khoa"
        khoaData = ChucNang.TruyVanDuLieu(khoaSql)
        loaiSql = "SELECT * FROM portal_loaidetai"
        loaiData = ChucNang.TruyVanDuLieu(loaiSql)
        if (len(khoaData['data']))  < 1:
            return HttpResponse("không có dữ liệu")
        if (len(loaiData['data']))  < 1:
            return HttpResponse("không có dữ liệu")
        jsonRender = {
            'title' : 'Thêm đề tài',
            'DsKhoa' : khoaData['data'],
            'DsLoai' : loaiData['data']
        }
        return render(request, 'portal/giangvien/them_detai.html', jsonRender)
    if request.method == "POST":
        tenDetai = request.POST['tenDeTai']
        khoaDeTai = request.POST['khoaDeTai']
        loaiDeTai = request.POST['loaiDeTai']
        soLuongDKDeTai = request.POST['soLuongDKDeTai']
        ngayBDDeTai = request.POST['ngayBDDeTai']
        ngayKTDeTai = request.POST['ngayKTDeTai']
        chiTiet = request.POST['chiTiet']
        userID = request.session.get('ID')
        jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Thêm đề tài thành công', 'backlink': '/'}
        themDetaiSql = "INSERT INTO portal_detai (IdUser ,  ChiTiet ,  NgayBD , NgayKT, SoLuong, IdLoai, HoatDong, TenDeTai, DaDangKi, DangThucHien, IdKhoa) VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, {6}, '{7}', {8}, {9}, {10})".format(userID, chiTiet,ngayBDDeTai, ngayKTDeTai,soLuongDKDeTai, loaiDeTai,1,tenDetai,0,0,khoaDeTai)
        try:
            ChucNang.UpdateDuLieu(themDetaiSql)
        except Exception as exc:
            jsonRender['ChiTiet'] = str(exc)
            jsonRender['ThongBao'] = str("Không thành công")
        return render(request, 'portal/giangvien/thongbao.html', jsonRender)
# Thêm đề tài
@csrf_exempt  # Tránh lỗi--CSRF token missing or incorrect
def them_hoatdong(request):
    if request.method == "GET":
        jsonRender = {
            'title' : 'Thêm hoạt động'
        }
        return render(request, 'portal/giangvien/them_hoatdong.html', jsonRender)
    if request.method == "POST":
        tenHoatDong = request.POST['tenHoatDong']
        kiHoatDong = request.POST['kiHoatDong']
        soLuongTGHD = request.POST['soLuongTGHD']
        diemHoatDong = request.POST['diemHoatDong']
        ngayBDHD = request.POST['ngayBDHD']
        ngayKTHD = request.POST['ngayKTHD']
        chiTietHD = request.POST['chiTietHD']
        userID = request.session.get('ID')
        jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Thêm đề tài thành công', 'backlink': '/'}
        themHDSql = "INSERT INTO portal_hoatdong (IdUser ,  ChiTiet ,  NgayBD , NgayKT, SoLuong, DiemRL, HoatDong, TenHoatDong, DaDangKi, DangThucHien, Ki) VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, {6}, '{7}', {8}, {9}, {10})".format(userID, chiTietHD,ngayBDHD, ngayKTHD,soLuongTGHD, diemHoatDong,1,tenHoatDong,0,0, kiHoatDong)
        try:
            ChucNang.UpdateDuLieu(themHDSql)
        except Exception as exc:
            jsonRender['ChiTiet'] = str(exc)
            jsonRender['ThongBao'] = str("Không thành công")
        return render(request, 'portal/giangvien/thongbao.html', jsonRender)
# Router /dangki
# Sua de tai
def xoa_detai(request, detaiID):
    sql = "UPDATE portal_detai SET HoatDong = 0 WHERE IdDeTai = {0}".format(detaiID)
    jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Xóa đề tài thành công', 'backlink': '../detaicuatoi/'}
    try:
        ChucNang.UpdateDuLieu(sql)
    except Exception as identifier:
        jsonRender['ChiTiet'] = str(identifier)
        jsonRender['ThongBao'] = str("Không thành công")
    return render(request, 'portal/giangvien/thongbao.html', jsonRender)
@csrf_exempt 
def sua_detai(request, detaiID):
    if request.method == "GET":
        sql = "Select * from portal_detai where IdDeTai = {0}".format(detaiID)
        hoatDong = ChucNang.TruyVanDuLieu(sql)
        sqlKhoa = "Select * from portal_khoa"
        DsKhoa = ChucNang.TruyVanDuLieu(sqlKhoa)
        sqlLoai = "Select * from portal_loaidetai"
        DsLoai = ChucNang.TruyVanDuLieu(sqlLoai)
        print(hoatDong['data'][0])
        jsonRender = {
            'title' : 'Sửa đề tài',
            'HoatDong' : hoatDong['data'][0],
            'DsKhoa' : DsKhoa['data'],
            'DsLoai' : DsLoai['data']
            
        }
        return render(request, 'portal/giangvien/sua_detai.html', jsonRender)
    if request.method == "POST":
        tenDeTai = request.POST['tenDeTai']
        khoaDeTai = request.POST['khoaDeTai']
        loaiDeTai = request.POST['loaiDeTai']
        soLuongDKDeTai = request.POST['soLuongDKDeTai']
        ngayBDDeTai = request.POST['ngayBDDeTai']
        ngayKTDeTai = request.POST['ngayKTDeTai']
        chiTiet = request.POST['chiTiet']
        userID = request.session.get('ID')
        jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Thêm đề tài thành công', 'backlink': '/'}
        themHDSql = "UPDATE portal_detai SET ChiTiet  = '{0}',  SoLuong = {1},  IdLoai = {2},   TenDeTai  = '{3}',  IdKhoa  = {4}, NgayBD = '{5}', NgayKT = '{6}' WHERE  IdDeTai  = {7}".format(chiTiet, soLuongDKDeTai,loaiDeTai, tenDeTai,khoaDeTai, ngayBDDeTai,ngayKTDeTai, detaiID)
        try:
            ChucNang.UpdateDuLieu(themHDSql)
        except Exception as exc:
            jsonRender['ChiTiet'] = str(exc)
            jsonRender['ThongBao'] = str("Không thành công")
        return render(request, 'portal/giangvien/thongbao.html', jsonRender)
# Sua de tai
def xoa_hoatdong(request, detaiID):
    sql = "UPDATE portal_hoatdong SET HoatDong = 0 WHERE IdHoatDong = {0}".format(detaiID)
    jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Xóa hoạt động thành công', 'backlink': '../hoatdongcuatoi/'}
    try:
        ChucNang.UpdateDuLieu(sql)
    except Exception as identifier:
        jsonRender['ChiTiet'] = str(identifier)
        jsonRender['ThongBao'] = str("Không thành công")
    return render(request, 'portal/giangvien/thongbao.html', jsonRender)
@csrf_exempt 
def sua_hoatdong(request, detaiID):
    if request.method == "GET":
        sql = "Select * from portal_hoatdong where IdHoatDong = {0}".format(detaiID)
        hoatDong = ChucNang.TruyVanDuLieu(sql)
        print(hoatDong['data'][0])
        jsonRender = {
            'title' : 'Sửa hoạt động',
            'HoatDong' : hoatDong['data'][0]
        }
        return render(request, 'portal/giangvien/sua_hoatdong.html', jsonRender)
    if request.method == "POST":
        tenHoatDong = request.POST['tenHoatDong']
        kiHoatDong = request.POST['kiHoatDong']
        soLuongTGHD = request.POST['soLuongTGHD']
        diemHoatDong = request.POST['diemHoatDong']
        ngayBDHD = request.POST['ngayBDHD']
        ngayKTHD = request.POST['ngayKTHD']
        chiTietHD = request.POST['chiTietHD']
        userID = request.session.get('ID')
        jsonRender = {'tieude' : 'Thành công', 'ThongBao' : 'Thành Công','ChiTiet' : 'Thêm đề tài thành công', 'backlink': '/'}
        themHDSql = "UPDATE portal_hoatdong SET ChiTiet  = '{0}',  SoLuong = {1},  Ki = {2},   TenHoatDong  = '{3}', NgayBD = '{4}', NgayKT = '{5}', DiemRL = {6} WHERE  IdHoatDong  = {7}".format(chiTietHD,soLuongTGHD,kiHoatDong,tenHoatDong, ngayBDHD, ngayKTHD,diemHoatDong, detaiID)
        try:
            ChucNang.UpdateDuLieu(themHDSql)
        except Exception as exc:
            jsonRender['ChiTiet'] = str(exc)
            jsonRender['ThongBao'] = str("Không thành công")
        return render(request, 'portal/giangvien/thongbao.html', jsonRender)
# Router /dangki