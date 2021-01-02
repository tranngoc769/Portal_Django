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
                "Khoa": thongTinDangKi[8].value,
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

    function kiemTraFormSuaNguoiDung() {
        var thongTinDangKi = $('#form_sua_nguoi_dung').serializeArray();
        var thongBaoLoi = ""; // Chuỗi thông báo khi có lỗi
        var dayDuThongTin = true;
        if (thongTinDangKi[0].value == "") {
            thongBaoLoi += "Chưa nhập tên đầy đủ\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[1].value == "") {
            thongBaoLoi += "Chưa nhập SDT\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[2].value == "") {
            thongBaoLoi += "Chưa nhập email\n";;
            dayDuThongTin = false
        };
        if (thongTinDangKi[4].value == "") {
            thongBaoLoi += "Chưa nhập ngày sinh\n";;
            dayDuThongTin = false
        };
        if (document.getElementById("choPhepDoiMk").checked == true && thongTinDangKi[6].value == "") {
            thongBaoLoi += "Chưa nhập mật khẩu\n";;
            dayDuThongTin = false
        }
        if (dayDuThongTin == false) {
            // Nếu có một trong các lỗi
            alert(thongBaoLoi); // thông báo
            return false;
        };
        if (document.getElementById("choPhepDoiMk").checked == false) {
            thongTinDangKi[6].value = "";
        }
        thongTinJSON = {
                "HoTen": thongTinDangKi[0].value,
                "SDT": thongTinDangKi[1].value,
                "Email": thongTinDangKi[2].value,
                "GioiTinh": thongTinDangKi[3].value,
                "NgaySinh": thongTinDangKi[4].value,
                "MatKhau": thongTinDangKi[6].value,
                "Quyen": thongTinDangKi[5].value,
                "Khoa": thongTinDangKi[8].value
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
                    window.location.replace('/')
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
    $("#themNguoidungBtn").on("click", function() {
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
    $("#SuaNguoiDungBtn").on("click", function() {
        var dayDuThongTin = kiemTraFormSuaNguoiDung();
        if (dayDuThongTin == false) return; // Nếu thiếu thông tin --> Ngừng, không gửi đơn đăng ký
        console.log(JSON.stringify(dayDuThongTin))
        var nguoiDungID = $(this).attr('nguoidungID');
        $.ajax({
            type: "POST",
            url: `/admin/sua_nguoidung/${nguoiDungID}`,
            data: JSON.stringify(dayDuThongTin),
            success: function(resp) {
                ketqua = JSON.parse(resp)
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
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
                ketqua = JSON.parse(resp)
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

    $("#importExcel").on("change", function(e) {
        var loai = $(this).attr('mask')
        var a = $("#importExcel")[0].files;
        if (a.length > 0) {
            console.log("co file")
            var form = $('form')[0];
            var formData = new FormData(form);
            file = a[0]
            formData.append('file', file);
            $.ajax({
                type: "POST",
                enctype: 'multipart/form-data',
                url: "/admin/import/" + loai,
                data: formData,
                processData: false,
                contentType: false,
                cache: false,
                success: function(data) {
                    noti = JSON.parse(data);
                    if (noti.code == 200) {
                        alert("Success");
                    } else {
                        alert("Lỗi")
                    }
                    window.location.reload();
                },
                error: function(e) {
                    alert('Lỗi')
                }
            });
        } else {
            console.log("no file")
        }
    });

    $("#themloaihoatdong").on("click", function(e) {
        $.ajax({
            type: "POST",
            url: `/admin/loaihd/`,
            data: JSON.stringify({ "Ten": $("#tenloaihoatdong")[0].value }),
            success: function(resp) {
                ketqua = JSON.parse(resp)
                if (ketqua.code != 200) { // Có lỗi
                    alert(ketqua.msg)
                } else {
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
    $("#diemDanh").on("click", function(e) {
        var hid = $(this).attr('hd');
        var obj = $('#dssv tbody tr').map(function() {
            var $row = $(this);
            // 1 2   3       4       5      6
            //0  ID	Họ Tên	MSSV	Điểm	Kì
            var t1 = $row.find(':nth-child(1)')[2].checked;
            var t2 = $row.find(':nth-child(2)').text();
            var t4 = $row.find(':nth-child(3)').text();
            var t5 = $row.find(':nth-child(5)').text();
            var t6 = $row.find(':nth-child(6)').text();
            return {
                dadiemdanh: t1,
                id: t2,
                diem: t4,
                hoatdongid: hid,
                diem: t5,
                ki: t6,
            };
        }).get();
        $.ajax({
            type: "POST",
            url: "/admin/hoatdong/diemdanh/",
            data: JSON.stringify(obj),
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
        });
    });
    $("#chontatca").on("click", function(e) {
        console.log("Chon tat ca");
        var listCheckbox = $(".custom-control-input");
        for (var i = 0; i < listCheckbox.length; i++) {
            listCheckbox[i].checked = true;
        }
    });
    $("#huychontatca").on("click", function(e) {
        console.log("Huy chon tat ca");
        var listCheckbox = $(".custom-control-input");
        for (var i = 0; i < listCheckbox.length; i++) {
            listCheckbox[i].checked = false;
        }
    });
    $("#importExcel_a").on("click", function(e) {
        console.log("oke")
        e.preventDefault();
        $("#importExcel:hidden").trigger('click');
        // $.ajax({
        //     type: "POST",
        //     url: "/admin/them_nguoidung/",
        //     data: JSON.stringify(dayDuThongTin),
        //     success: function(resp) {
        //         ketqua = JSON.parse(resp)
        //         if (ketqua.code != 200) { // Có lỗi
        //             alert(ketqua.msg)
        //         } else {
        //             // Đăng ký thành công, chuyển sang trang đăng nhập
        //             alert(ketqua.msg)
        //             window.location.reload()
        //         }
        //     },
        //     error: function(resp) {
        //         console.log("errr");
        //         console.log(resp);
        //     }
    });
})(window.jQuery);