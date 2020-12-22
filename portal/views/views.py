from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from portal.models import NGUOIDUNG
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from portal.models import *
import hashlib
import json
from . import chucnang as ChucNang


def kiemTraCookie(request):
    print(request)

# Danh sách đề tài
def dsDetai(request):
    sql = """
            SELECT
                  portal_detai.IdDeTai,
                  portal_detai.IdUser,
                  portal_detai.ChiTiet,
                  portal_detai.NgayBD,
                  portal_detai.NgayKT,
                  portal_detai.SoLuong,
                  portal_detai.IdLoai,
                  portal_detai.HoatDong,
                  portal_detai.TenDeTai,
                  portal_detai.DaDangKi,
                  portal_detai.DangThucHien,
                  portal_detai.IdKhoa,
                  portal_loaidetai.TenLoai,
                  portal_khoa.TenKhoa,
                  portal_nguoidung.HoTen,
                  portal_nguoidung.TenNguoiDung,
                  portal_dieukiendangky.Diem
                  FROM
                  portal_detai
                  JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                  JOIN portal_loaidetai ON portal_detai.IdLoai = portal_loaidetai.IdLoai
                  JOIN portal_khoa ON portal_khoa.IdKhoa = portal_detai.IdKhoa
                  JOIN portal_dieukiendangky ON portal_dieukiendangky.IdKhoa = portal_detai.IdKhoa AND portal_dieukiendangky.IdLoai = portal_detai.IdLoai
                  WHERE
                  portal_nguoidung.HoatDong = 1 AND
                  portal_detai.HoatDong = 1 AND
                  portal_detai.DangThucHien = 0
            ORDER BY
            portal_detai.NgayBD ASC
      """
    dsDetai = ChucNang.TruyVanDuLieu(sql)
    data = {
        "DsDetai": dsDetai['data']
    }
    print(dsDetai['data'][0])
    return render(request, 'portal/sinhvien/dsDetai.html', data)
# Danh sách hoạt động
def dshoatdong(request):
    sql = """
                        SELECT
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
                        portal_nguoidung.HoatDong = 1 AND
                        portal_hoatdong.HoatDong = 1 AND
                        portal_hoatdong.DangThucHien = 0
                        ORDER BY
                        portal_hoatdong.NgayBD ASC

      """
    dsHoatDong = ChucNang.TruyVanDuLieu(sql)
    data = {
        "DsHoatDong": dsHoatDong['data']
    }
    print(dsHoatDong['data'][0])
    return render(request, 'portal/sinhvien/dsHoatDong.html', dsHoatDong)
# Chi tiết đề tài
def chitietdetai(request, detaiID):
    sql = """
            SELECT
                  portal_detai.IdDeTai,
                  portal_detai.IdUser,
                  portal_detai.ChiTiet,
                  portal_detai.NgayBD,
                  portal_detai.NgayKT,
                  portal_detai.SoLuong,
                  portal_detai.IdLoai,
                  portal_detai.HoatDong,
                  portal_detai.TenDeTai,
                  portal_detai.DaDangKi,
                  portal_detai.DangThucHien,
                  portal_detai.IdKhoa,
                  portal_loaidetai.TenLoai,
                  portal_khoa.TenKhoa,
                  portal_nguoidung.HoTen,
                  portal_nguoidung.TenNguoiDung,
                  portal_dieukiendangky.Diem
                  FROM
                  portal_detai
                  JOIN portal_nguoidung ON portal_detai.IdUser = portal_nguoidung.IdUser
                  JOIN portal_loaidetai ON portal_detai.IdLoai = portal_loaidetai.IdLoai
                  JOIN portal_khoa ON portal_khoa.IdKhoa = portal_detai.IdKhoa
                  JOIN portal_dieukiendangky ON portal_dieukiendangky.IdKhoa = portal_detai.IdKhoa AND portal_dieukiendangky.IdLoai = portal_detai.IdLoai
                  WHERE
                  portal_nguoidung.HoatDong = 1 AND
                  portal_detai.HoatDong = 1 AND
                  portal_detai.DangThucHien = 0 AND
                  portal_detai.IdDeTai = {0}
            ORDER BY
            portal_detai.NgayBD ASC
      """.format(detaiID)
    chitietDetai = ChucNang.TruyVanDuLieu(sql)
    if (len(chitietDetai['data']) < 1):
        return "Không có đề tài"
    data = {
        'DeTai': chitietDetai['data'][0]
    }
    TenDangNhap = request.session['TenDangNhap']
    getUserIDSql = "select IdUser from portal_nguoidung where TenNguoiDung='{0}'".format(
        TenDangNhap)
    temp = ChucNang.TruyVanDuLieu(getUserIDSql)
    if (len(temp['data']) < 1):
        return redirect('/dangxuat')
    userId = temp['data'][0]['IdUser']
    checkDkSQL = "select * from portal_detaidadangky where IdUser='{0}' and IdDetai ={1}".format(
        userId, detaiID)
    temp = ChucNang.TruyVanDuLieu(checkDkSQL)
    daDangki = False
    if (len(temp['data']) > 0):
        daDangki = True
    DiemTrungBinhSQL = "SELECT Diem from portal_diemtrungbinh where userID='{0}'".format(
        userId)
    temp = ChucNang.TruyVanDuLieu(DiemTrungBinhSQL)
    if (len(temp['data']) < 1):
        data['ChoDK'] = False
    else:
        diemTB = temp['data'][0]['Diem']
        print(diemTB)
        if (diemTB < chitietDetai['data'][0]['Diem']):
            data['ChoDK'] = False
            data['Diem'] = diemTB
        else:
            data['ChoDK'] = True
            data['Diem'] = diemTB
    if (daDangki):
        data['ChoDK'] = False
    return render(request, 'portal/sinhvien/chitiet_detai.html', data)
# Chi tiết hoạt động
def chitiethoatdong(request, hoatdongID):
    sql = """
            SELECT
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
                  portal_nguoidung.HoatDong = 1 
                  AND portal_hoatdong.HoatDong = 1 
                  AND portal_hoatdong.DangThucHien = 0 AND portal_hoatdong.IdHoatDong = {0}
            ORDER BY
                  portal_hoatdong.NgayBD ASC
      """.format(hoatdongID)
    chitietHoatDong = ChucNang.TruyVanDuLieu(sql)
    if (len(chitietHoatDong['data']) < 1):
        return "Không có đề tài"
    data = {
        'HoatDong': chitietHoatDong['data'][0]
    }
    if (request.session['Quyen'] != 3):
        data['ChoDK'] = False
        return render(request, 'portal/sinhvien/chitiet_hoatdong.html', data)
    TenDangNhap = request.session['TenDangNhap']
    getUserIDSql = "select IdUser from portal_nguoidung where TenNguoiDung='{0}'".format(
        TenDangNhap)
    temp = ChucNang.TruyVanDuLieu(getUserIDSql)
    if (len(temp['data']) < 1):
        return redirect('/dangxuat')
    userId = temp['data'][0]['IdUser']
    checkDkSQL = "select * from portal_hoatdongdadangky where IdUser='{0}' and IdHoatDong ={1}".format(
        userId, hoatdongID)
    temp = ChucNang.TruyVanDuLieu(checkDkSQL)
    daDangki = False
    if (len(temp['data']) > 0):
        daDangki = True
    if (daDangki):
        data['ChoDK'] = False
    else:
        data['ChoDK'] = True
    return render(request, 'portal/sinhvien/chitiet_hoatdong.html', data)
# Trang chủ
def index(request):
    quyen = request.session.get('Quyen')
    if (quyen == 1):
        # admin
        return redirect('/admin')
    if (quyen == 2):
        return redirect('/gv')
    if (quyen == 3):
        # Sinh vien
        thongbaoSQL = "SELECT * from portal_thongbao ORDER BY NgayThongBao DESC"
        hoatDongSQL = """
                                    SELECT
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
                        portal_nguoidung.HoatDong = 1 AND
                        portal_hoatdong.HoatDong = 1 AND
                        portal_hoatdong.DangThucHien = 0
                        ORDER BY
                        portal_hoatdong.NgayBD ASC
            """
        dsThongBao = ChucNang.TruyVanDuLieu(thongbaoSQL)
        dsHoatDong = ChucNang.TruyVanDuLieu(hoatDongSQL)
        return render(request, 'portal/sinhvien/trangchu.html', {"ThongBao": dsThongBao['data'], "HoatDong": dsHoatDong['data']})
# Đăng kí đề tài
def dkdetai(request, detaiID):
    if request.method == "GET":
        ktDetaiSql = "Select * from portal_detai where IdDeTai='{0}'".format(
            detaiID)
        thongtindangkidetai = ChucNang.TruyVanDuLieu(ktDetaiSql)

        if (len(thongtindangkidetai['data']) < 1):
            return HttpResponse(json.dumps({"code": 403, "msg": "Không thấy đề tài"}, ensure_ascii=False))
        SoLuongSv = thongtindangkidetai['data'][0]['SoLuong']
        DaDangKi = thongtindangkidetai['data'][0]['DaDangKi']
        DangThucHien = thongtindangkidetai['data'][0]['DangThucHien']
        if (DangThucHien == 1 or SoLuongSv == DaDangKi):
            return HttpResponse(json.dumps({"code": 403, "msg": "Đề tài đã đủ số lượng"}, ensure_ascii=False))
        TenDangNhap = request.session['TenDangNhap']
        getUserIDSql = "select IdUser from portal_nguoidung where TenNguoiDung='{0}'".format(
            TenDangNhap)
        temp = ChucNang.TruyVanDuLieu(getUserIDSql)
        if (len(temp['data']) < 1):
            return HttpResponse(json.dumps({"code": 403, "msg": "Không thấy user"}, ensure_ascii=False))
        userId = temp['data'][0]['IdUser']
        # Kiểm tra người dùng đã đăng kí đề tài chưa
        checkDkSQL = "select * from portal_detaidadangky where IdUser='{0}' and IdDetai ={1}".format(
            userId, detaiID)
        temp = ChucNang.TruyVanDuLieu(checkDkSQL)
        if (len(temp['data']) > 0):
            return HttpResponse(json.dumps({"code": 403, "msg": "Đã đăng kí"}, ensure_ascii=False))
        today = date.today()
        # Đăng kí đề tài
        sql = "INSERT INTO portal_detaidadangky (IdDeTai, IdUser, NgayDKDT) VALUES ({0}, {1}, '{2}')".format(
            detaiID, userId, today.strftime('%Y-%m-%d %H:%M:%S'))
        ChucNang.UpdateDuLieu(sql)
        # Tăng số lượng đăng kí
        DaDangKi = DaDangKi + 1
        if (DaDangKi == SoLuongSv):
            DangThucHien = 1
        sql = "UPDATE portal_detai SET DaDangKi = {0}, DangThucHien={1} WHERE IdDeTai = {2}".format(
            DaDangKi, DangThucHien, detaiID)
        ChucNang.UpdateDuLieu(sql)
        return HttpResponse(json.dumps({"code": 200, "msg": "success"}, ensure_ascii=False))
    return HttpResponse(json.dumps({"code": 403, "msg": "method not allow"}))
# Đăng kí hoạt động
def dkhoatdong(request, hoatdongID):
      if request.method == "GET":
            ktHoatDongSql = "Select * from portal_hoatdong where IdHoatdong='{0}'".format(hoatdongID)
            thongtindangkiHoatDong = ChucNang.TruyVanDuLieu(ktHoatDongSql)
            if (len(thongtindangkiHoatDong['data']) < 1):
                  return HttpResponse(json.dumps({"code": 403, "msg": "Không thấy đề tài"}, ensure_ascii=False))
            SoLuongSv = thongtindangkiHoatDong['data'][0]['SoLuong']
            DaDangKi = thongtindangkiHoatDong['data'][0]['DaDangKi']
            DangThucHien = thongtindangkiHoatDong['data'][0]['DangThucHien']
            if (DangThucHien == 1 or SoLuongSv == DaDangKi):
                  return HttpResponse(json.dumps({"code": 403, "msg": "Đề tài đã đủ số lượng"}, ensure_ascii=False))
            TenDangNhap = request.session['TenDangNhap']
            getUserIDSql = "select IdUser from portal_nguoidung where TenNguoiDung='{0}'".format(TenDangNhap)
            temp = ChucNang.TruyVanDuLieu(getUserIDSql)
            if (len(temp['data']) < 1):
                  return HttpResponse(json.dumps({"code": 403, "msg": "Không thấy user"}, ensure_ascii=False))
            userId = temp['data'][0]['IdUser']
            # Kiểm tra người dùng đã đăng kí hoạt động chưa
            checkDkSQL = "select * from portal_hoatdongdadangky where IdUser='{0}' and IdHoatDong ={1}".format(userId, hoatdongID)
            temp = ChucNang.TruyVanDuLieu(checkDkSQL)
            if (len(temp['data']) > 0):
                  return HttpResponse(json.dumps({"code": 403, "msg": "Đã đăng kí"}, ensure_ascii=False))
            today = date.today()
            # Đăng kí đề tài
            sql = "INSERT INTO portal_hoatdongdadangky (IdHoatDong, IdUser, NgayDKHD) VALUES ({0}, {1}, '{2}')".format(hoatdongID, userId, today.strftime('%Y-%m-%d %H:%M:%S'))
            ChucNang.UpdateDuLieu(sql)
            # Tăng số lượng đăng kí
            DaDangKi = DaDangKi + 1
            if (DaDangKi == SoLuongSv):
                  DangThucHien = 1
            sql = "UPDATE portal_HoatDong SET DaDangKi = {0}, DangThucHien={1} WHERE IdHoatDong = {2}".format(DaDangKi, DangThucHien, hoatdongID)
            ChucNang.UpdateDuLieu(sql)
            return HttpResponse(json.dumps({"code": 200, "msg": "success"}, ensure_ascii=False))
      return HttpResponse(json.dumps({"code": 403, "msg": "method not allow"}))
# Router /dangnhap
@csrf_exempt  # Tránh lỗi--CSRF token missing or incorrect
def dangnhap(request):
    if request.method == "GET":
        return render(request, 'portal/dangnhap.html')
    if request.method == "POST":
        # Lấy dữ liệu đăng nhập dưới dạng Objects
        thongTinDN = json.loads(request.body)
        tenDangNhap = thongTinDN['TenDangNhap']
        matKhau = thongTinDN['MatKhau']
        maHoaMatKhau = hashlib.md5(
            matKhau.encode()).hexdigest()  # Mã hóa mật khẩu md5
        # Biến kết quả (Json), mặc định là thành công, xuống dưới kiểm tra có lỗi thì update, khỏi phải tạo biến mới
        resp = {"code": 200, "msg": "Đăng nhập thành công"}
        try:
            query_NguoiDung = NGUOIDUNG.objects.filter(
                TenNguoiDung=tenDangNhap, MatKhau=maHoaMatKhau)
            if (len(query_NguoiDung) < 1):  # Bé hơn 1 là ko có tài khoản có TenNguoiDung và MatKhau
                resp["code"] = 404
                resp['msg'] = "Tài khoản hoặc mật khẩu không đúng"
            else:
                # Thành công --> gán session
                request.session['DaDangNhap'] = True
                request.session['TenDangNhap'] = tenDangNhap
                # [0] vì chỉ có 1 nguoidung duy nhất (theo TenDangNhap)
                request.session['Quyen'] = query_NguoiDung[0].Quyen
                request.session['ID'] = query_NguoiDung[0].IdUser
        except Exception as query_erro:
            #   Có lỗi --> không có tài khoản
            resp["code"] = 404
            resp['msg'] = str(query_erro)
        # Trả về kết quả json (nếu không có lỗi gì+query có thông tin thì resp mặc định như khi khai báo do không bị update, ngược lại thì có code 404 và msg theo 2 trường hợp kia)
        return HttpResponse(json.dumps(resp, ensure_ascii=False))
# Router /dangki
@csrf_exempt  # Tránh lỗi--CSRF token missing or incorrect
def dangki(request):
    if request.method == "GET":
        sql = "SELECT * FROM portal_khoa"
        dsKhoa = ChucNang.TruyVanDuLieu(sql)
        return render(request, 'portal/dangki.html', dsKhoa)
    if request.method == "POST":
        # Lấy dữ liệu đăng ký dưới dạng Objects
        thongTinDK = json.loads(request.body)
        # 'SDT': '123', 'Email': '1234@gmail.com', 'GioiTinh': '0', 'NgaySinh': '2020-12-10', 'MatKhau': 'password', 'Quyen': 3}
        maHoaMatKhau = hashlib.md5(thongTinDK.get(
            'MatKhau').encode()).hexdigest()  # Mã hóa mật khẩu md5
        # Các thao tác validate ở đây
        try:
            nguoiDungDk = NGUOIDUNG(TenNguoiDung=thongTinDK.get('TenNguoiDung'), HoTen=thongTinDK.get('HoTen'), SDT=thongTinDK.get('SDT'), MatKhau=maHoaMatKhau, Email=thongTinDK.get(
                'Email'), NgaySinh=thongTinDK.get('NgaySinh'), GioiTinh=thongTinDK.get('GioiTinh'), Quyen=thongTinDK.get('Quyen'), Khoa=thongTinDK.get('Khoa'))
            nguoiDungDk.save()
        except Exception as insertErr:
            resp = {"code": 404}
            resp['msg'] = str(insertErr)
            return HttpResponse(json.dumps(resp))
        resp = {"code": 200}
        resp['msg'] = "success"
        return HttpResponse(json.dumps(resp))
# Dang Xuat
def dangxuat(request):
    del request.session['DaDangNhap']
    del request.session['TenDangNhap']
    del request.session['Quyen']
    del request.session['ID']
    return redirect('/')

# SinhVien
