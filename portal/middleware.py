from django.shortcuts import render, redirect
# Cấu trúc copy trên google, chỉnh sửa hàm __call__ (hàm thực thi middleware)
class KiemTraQuyen:
      def __init__(self, get_response):
            self.get_response = get_response
      def __call__(self, request):
            daDangNhap = request.session.get('DaDangNhap')
            response = self.get_response(request)
            if ('dangnhap' in request.path or 'dangki' in request.path):
                  if (daDangNhap):
                        return redirect('/trangchu')
                  return response
            if (daDangNhap!=True):
                  return redirect('/dangnhap')
            return response
            # return redirect('/dangki')
      def process_exception(self, request, exception):
            pass
      def process_template_response(self, request, response):
            pass