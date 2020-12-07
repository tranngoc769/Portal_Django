(function($) {
    // Hàm : kiểm tra thông tin đăng ký có đầy đủ?
    // Kết quả trả về : bool hoặc mảng các thông tin đăng nhập
    function kiemTraFormDangKy() {
        var thongTinDangKi = $('#form_dangki').serializeArray();
        var thongBaoLoi = ""; // Chuỗi thông báo khi có lỗi
        var dayDuThongTin = true;
        // 0: {name: "fullname", value: ""} 1: {name: "username", value: ""}  2: {name: "phone", value: ""}  3: {name: "email", value: "sdasd@"} 4: {name: "gender", value: "0"}
        // 5: {name: "dob", value: ""} 6: {name: "password", value: ""} 7: {name: "repassword", value: ""}
        // nếu đầy đủ
        if (thongTinDangKi[0].value == "") {
            thongBaoLoi += "Chưa nhập tên đầy đủ\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[1].value == "") {
            thongBaoLoi += "Chưa nhập MSSV\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[2].value == "") {
            thongBaoLoi += "Chưa nhập SDT\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[3].value == "") {
            thongBaoLoi += "Chưa nhập email\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[5].value == "") {
            thongBaoLoi += "Chưa nhập ngày sinh\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[6].value == "") {
            thongBaoLoi += "Chưa nhập mật khẩu\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[7].value != thongTinDangKi[6].value) {
            thongBaoLoi += "Mật khẩu không khớp\n";;
            dayDuThongTin = false
        };
        if (dayDuThongTin == false) {
            // Nếu có một trong các lỗi
            alert(thongBaoLoi); // thông báo
            return false;
        };
        thongTinJSON = {
                "HoTen": thongTinDangKi[0].value,
                "TenNguoiDung": thongTinDangKi[1].value,
                "SDT": thongTinDangKi[2].value,
                "Email": thongTinDangKi[3].value,
                "GioiTinh": thongTinDangKi[4].value,
                "NgaySinh": thongTinDangKi[5].value,
                "MatKhau": thongTinDangKi[6].value,
                "Quyen": 3
            }
            // Nếu đầy đủ, trả về json thông tin
        return thongTinJSON;
    }

    function kiemTraFormThemTaiKhoan() {
        var thongTinDangKi = $('#form_them_nguoi_dung').serializeArray();
        var thongBaoLoi = ""; // Chuỗi thông báo khi có lỗi
        var dayDuThongTin = true;
        // 0: {name: "fullname", value: ""} 1: {name: "username", value: ""}  2: {name: "phone", value: ""}  3: {name: "email", value: "sdasd@"} 4: {name: "gender", value: "0"}
        // 5: {name: "dob", value: ""} 6: {name: "password", value: ""} 7: {name: "repassword", value: ""}
        // nếu đầy đủ
        if (thongTinDangKi[0].value == "") {
            thongBaoLoi += "Chưa nhập tên đầy đủ\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[1].value == "") {
            thongBaoLoi += "Chưa nhập MSSV\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[2].value == "") {
            thongBaoLoi += "Chưa nhập SDT\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[3].value == "") {
            thongBaoLoi += "Chưa nhập email\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[5].value == "") {
            thongBaoLoi += "Chưa nhập ngày sinh\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[7].value == "") {
            thongBaoLoi += "Chưa nhập mật khẩu\n";;
            dayDuThongTin = false
        };
        if (dayDuThongTin == false) {
            // Nếu có một trong các lỗi
            alert(thongBaoLoi); // thông báo
            return false;
        };
        thongTinJSON = {
                "HoTen": thongTinDangKi[0].value,
                "TenNguoiDung": thongTinDangKi[1].value,
                "SDT": thongTinDangKi[2].value,
                "Email": thongTinDangKi[3].value,
                "GioiTinh": thongTinDangKi[4].value,
                "NgaySinh": thongTinDangKi[5].value,
                "MatKhau": thongTinDangKi[7].value,
                "Quyen": thongTinDangKi[6].value
            }
            // Nếu đầy đủ, trả về json thông tin
        return thongTinJSON;
    }
    console.log("ready")
    $("#dangnhapBtn").on("click", function() {
        var TenDangNhap = $("#dn_username").val(); // jquery lấy value của thẻ input id = dn_username;
        var MatKhau = $("#dn_password").val(); // jquery lấy value của thẻ input id = dn_username;
        if (TenDangNhap == "" || MatKhau == "") {
            alert("Nhập đầy đủ tên đăng nhập và mật khẩu");
            return; // Dừng
        }
        // Nếu nhập đủ 
        // Gửi request đên api của server 
        var thongTinDN = JSON.stringify({ "TenDangNhap": TenDangNhap, "MatKhau": MatKhau })
        console.log(thongTinDN)
        $.ajax({
            type: "POST",
            url: "/dangnhap/",
            data: thongTinDN,
            success: function(resp) {
                ketqua = JSON.parse(resp)
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
                    // Đăng nhập thành công
                    // window.location.replace('../dangnhap')
                }
            },
            error: function(resp) {
                console.log("errr");
                console.log(code);
                console.log(data);
            }
        })
    })

    $("#dangkiBtn").on("click", function() {
        var dayDuThongTin = kiemTraFormDangKy();
        if (dayDuThongTin == false) return; // Nếu thiếu thông tin --> Ngừng, không gửi đơn đăng ký
        console.log(JSON.stringify(dayDuThongTin))
        $.ajax({
            type: "POST",
            url: "/dangki/",
            data: JSON.stringify(dayDuThongTin),
            success: function(resp) {
                ketqua = JSON.parse(resp)
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
                    // Đăng ký thành công, chuyển sang trang đăng nhập
                    window.location.replace('../dangnhap')
                }
            },
            error: function(resp) {
                console.log("errr");
                console.log(code);
                console.log(data);
            }
        })
    })
    $("#themNguoiDungBtn").on("click", function() {
        var dayDuThongTin = kiemTraFormThemTaiKhoan();
        if (dayDuThongTin == false) return; // Nếu thiếu thông tin --> Ngừng, không gửi đơn đăng ký
        console.log(JSON.stringify(dayDuThongTin))
        $.ajax({
            type: "POST",
            url: "/admin/them_nguoidung/",
            data: JSON.stringify(dayDuThongTin),
            success: function(resp) {
                ketqua = JSON.parse(resp)
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
                    // Đăng ký thành công, chuyển sang trang đăng nhập
                    alert(ketqua.msg)
                    window.location.reload()
                }
            },
            error: function(resp) {
                console.log("errr");
                console.log(resp);
            }
        })
    });
    // Sự kiện click trên nút xóa người dùng
    $(document).on('click', '.delete-user', function() { // Sự kiện kích hoạt khi một thẻ có class delete-user được click
        var nguoiDungID = $(this).attr('nguoiDungID'); // Lấy nguoidungID từ thuộc tính nguoiDungID của thẻ
        $.ajax({
            type: "POST",
            url: `/admin/xoa_nguoidung/${nguoiDungID}`, // Gửi post request đến url để xóa user
            success: function(resp) {
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
                    alert("Xóa người dùng thành công")
                    window.location.reload()
                }
            },
            error: function(resp) {
                console.log("errr");
                console.log(resp);
            }
        })
    })
})(window.jQuery);