from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json
# Hàm để truy vấn dữ liệu bằng query sql
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
def UpdateDuLieu(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)