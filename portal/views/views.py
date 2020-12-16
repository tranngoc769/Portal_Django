from django.shortcuts import render, redirect
from django.http import HttpResponse
from portal.models import NGUOIDUNG
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from portal.models import  *
import  hashlib
import json
from . import chucnang as ChucNang
def kiemTraCookie(request):
      print(request)
def dsDetai(request):
      return render(request,'portal/sinhvien/dsDetai.html')
# Create your views here.
# def dangnhap(request):
#       test = NGUOIDUNG()
#       data = NGUOIDUNG.objects.all()
#       print(data)
#       if request.method =="GET":
#             return render(request,"portal/dangnhap.html")
#       else:
#             return HttpResponse("Method not permission")
def index(request):
      quyen = request.session.get('Quyen')
      if (quyen == 1):
            # admin 
            return redirect('/admin')
      if (quyen == 2):
            return redirect('/gv')
      if (quyen == 3):
            # Sinh vien
            thongbaoSQL = "SELECT * from portal_thongbao ORDER BY NgayThongBao DESC";
            hoatDongSQL = """
            SELECT
                  portal_hoatdong.IdHoatDong,
                  portal_hoatdong.IdUser,
                  portal_hoatdong.ChiTiet,
                  portal_hoatdong.NgayBD,
                  portal_hoatdong.NgayKT,
                  portal_hoatdong.SoLuong,
                  portal_hoatdong.IdDiaDiem,
                  portal_hoatdong.DiemRL,
                  portal_hoatdong.HoatDong,
                  portal_hoatdong.DaDangKi,
                  portal_hoatdong.DangThucHien,
                  portal_nguoidung.IdUser,
                  portal_nguoidung.HoTen
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
            return render(request, 'portal/sinhvien/trangchu.html', {"ThongBao": dsThongBao['data'], "HoatDong" : dsHoatDong['data']})
# Router /dangnhap
@csrf_exempt #Tránh lỗi--CSRF token missing or incorrect
def dangnhap(request):
      if request.method =="GET":
            return render(request,'portal/dangnhap.html')
      if request.method == "POST":
            thongTinDN = json.loads(request.body) #Lấy dữ liệu đăng nhập dưới dạng Objects
            tenDangNhap = thongTinDN['TenDangNhap']
            matKhau = thongTinDN['MatKhau']
            maHoaMatKhau = hashlib.md5(matKhau.encode()).hexdigest() # Mã hóa mật khẩu md5
            resp = {"code" : 200, "msg" : "Đăng nhập thành công"} # Biến kết quả (Json), mặc định là thành công, xuống dưới kiểm tra có lỗi thì update, khỏi phải tạo biến mới
            try:
                  query_NguoiDung = NGUOIDUNG.objects.filter(TenNguoiDung = tenDangNhap, MatKhau = maHoaMatKhau)
                  if (len(query_NguoiDung) < 1): #Bé hơn 1 là ko có tài khoản có TenNguoiDung và MatKhau
                        resp["code"] = 404
                        resp['msg'] = "Tài khoản hoặc mật khẩu không đúng"
                  else:
                        # Thành công --> gán session 
                        request.session['DaDangNhap'] =  True
                        request.session['TenDangNhap'] = tenDangNhap
                        request.session['Quyen'] = query_NguoiDung[0].Quyen # [0] vì chỉ có 1 nguoidung duy nhất (theo TenDangNhap)
            except Exception as query_erro:
                  #   Có lỗi --> không có tài khoản 
                  resp["code"] = 404
                  resp['msg'] = str(query_erro)
            # Trả về kết quả json (nếu không có lỗi gì+query có thông tin thì resp mặc định như khi khai báo do không bị update, ngược lại thì có code 404 và msg theo 2 trường hợp kia)
            return HttpResponse(json.dumps(resp, ensure_ascii=False))
# Router /dangki
@csrf_exempt #Tránh lỗi--CSRF token missing or incorrect
def dangki(request):
      if request.method =="GET":
            sql = "SELECT * FROM portal_khoa"
            dsKhoa = ChucNang.TruyVanDuLieu(sql)
            return render(request,'portal/dangki.html', dsKhoa)
      if request.method == "POST":
            thongTinDK = json.loads(request.body) #Lấy dữ liệu đăng ký dưới dạng Objects
            # 'SDT': '123', 'Email': '1234@gmail.com', 'GioiTinh': '0', 'NgaySinh': '2020-12-10', 'MatKhau': 'password', 'Quyen': 3}
            maHoaMatKhau = hashlib.md5(thongTinDK.get('MatKhau').encode()).hexdigest() # Mã hóa mật khẩu md5
            # Các thao tác validate ở đây
            try:
                  nguoiDungDk = NGUOIDUNG(TenNguoiDung = thongTinDK.get('TenNguoiDung'), HoTen= thongTinDK.get('HoTen'),SDT = thongTinDK.get('SDT'), MatKhau= maHoaMatKhau,Email = thongTinDK.get('Email'), NgaySinh= thongTinDK.get('NgaySinh'), GioiTinh= thongTinDK.get('GioiTinh'),Quyen = thongTinDK.get('Quyen'), Khoa = thongTinDK.get('Khoa'))
                  nguoiDungDk.save()
            except Exception as insertErr:
                  resp = {"code" : 404}
                  resp['msg'] = str(insertErr)
                  return HttpResponse(json.dumps(resp))
            resp = {"code" : 200}
            resp['msg'] = "success"
            return HttpResponse(json.dumps(resp))

# Dang Xuat
def dangxuat(request):
      del request.session['DaDangNhap'] 
      del request.session['TenDangNhap']
      del request.session['Quyen']
      return redirect('/')

# SinhVien