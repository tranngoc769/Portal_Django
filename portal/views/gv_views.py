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


def index(request):
    return redirect('detai/')
# Hàm lấy danh sách đề tài


def danhSachDeTai(trang, moitrang):
    dsDetai = tatCaDeTai()
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
                    portal_loaidetai.DiemSan,
                portal_detai.DangThucHien
                    FROM
                    portal_detai
                    JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                    JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                    WHERE
                    portal_detai.HoatDong = 1 AND
                    portal_nguoidung.HoatDong = 1
            LIMIT {0} OFFSET {1}
            """.format(moitrang, (trang-1)*moitrang)  # Offset bắt đầu từ 0 --> trang - 1, công thức phân trang sql
    dsDeTai_PhanTrang = TruyVanDuLieu(sql)
    dsDeTai_PhanTrang['SoDeTai'] = len(dsDetai['data'])
    dsDeTai_PhanTrang['SoTrang'] = tongTrang
    return dsDeTai_PhanTrang
def TruyVanDuLieu(sql):
    with connection.cursor() as cursor:
        # Data mẫu khi cursor : (('Tuyen', 8.5),('Phuc', 8.5)) : tức kết quả truy vấn được 2 dòng, mỗi dòng có 2 giá trị
        # Mong muốn đầu ra JSON : 'data' : [{'HoTen' : 'Tuyen' , 'Diem' : 8.5}, {'HoTen' : 'Phuc' , 'Diem' : 8.5}]
        cursor.execute(sql)
        data = cursor.fetchall()
        ketqua = {}
        mangPhanTu = []
        for dong in data:  # Lặp từng dòng : ('Tuyen', 8.5) --> ('Phuc', 8.5)
            jsonData = {}
            for giaTri in enumerate(dong):  # enumerate: thêm số thứ tự cho mảng
                # VD : (0, ('Tuyen', 8.5)) , A[0] là 0, A[1] là ('Tuyen', 8.5)
                # Vòng lặp này lặp các giá trị của từng dòng : 'Tuyen' --> 8,5

                viTri = giaTri[0]  # 1, 2, 3,...
                # cursor.description là mảng 2 chiều, mỗi phần tử là mảng thông tin của từng cột . VD : (('Hoten',1,2,4), ('Diem',23,5,6)
                # Chỉ cần lấy [0] là tên của cột đó như dưới, giá trị vị trí mấy thì tương ứng tên cột thứ mấy. VD 'Tuyen' vị trị 0 --> Cột 0 là HoTen
                tenCot = cursor.description[viTri][0]
                # Gán vào JSON  {TenCot : GiaTri}
                jsonData[tenCot] = giaTri[1]  # Kết quả : {'Hoten' : 'Tuyen}
            mangPhanTu.append(jsonData)  # Thêm vô mảng các kết quả dòng
        # Kết thúc vòng lặp thu được các JSON kết quả có tên cột của từng dòng
        # Gán vào JSON kết quả , tức biến ketqua có thuộc tính data chứa mảng các dòng
        ketqua['data'] = mangPhanTu
        return ketqua
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
# Hàm lấy tất cả đề tài (ko bị x)
def tatCaDeTai():
    danhSachDeTai = TruyVanDuLieu("""SELECT
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
                portal_loaidetai.DiemSan,
                portal_detai.DangThucHien
                FROM
                portal_detai
                JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                WHERE
                portal_detai.HoatDong = 1 AND
                portal_nguoidung.HoatDong = 1
            """)
    return danhSachDeTai
# Hàm tạo dữ liệu json để render quản lý đề tài
def taoJsonQLDeTai(dsDeTai, trangHienTai):
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
    # Lấy danh sách sinh viên theo trang / mỗi trang
    dsDeTai_phanTrang = danhSachDeTai(trangHienTai, MoiTrang)
    # Tạo JSON để render --> chứa phân trang, ds người dùng
    print(dsDeTai_phanTrang)
    content = taoJsonQLDeTai(dsDeTai_phanTrang, trangHienTai)
    return render(request, 'portal/giangvien/ql_detai.html', content)
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
                portal_loaidetai.DiemSan,
            portal_detai.DangThucHien
                FROM
                portal_detai
                JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                JOIN portal_loaidetai ON portal_loaidetai.IdLoai = portal_detai.IdLoai
                WHERE
                portal_detai.IdDeTai = {0} AND
                portal_detai.HoatDong = 1 AND
                portal_nguoidung.HoatDong = 1""".format(detaiID)
    queryData = TruyVanDuLieu(sql)
    if (len(queryData['data']))  < 1:
              return HttpResponse("không có user")
    thongTinDeTai = queryData['data'][0] # Kết quả query là 1 mảng --> lấy phần tử đầu tiên cũng là duy nhất (id là duy nhất)
    return render(request, 'portal/giangvien/chitiet_detai.html', thongTinDeTai)
