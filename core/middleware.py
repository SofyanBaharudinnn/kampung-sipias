"""
SEO Middleware untuk Kampung Sipias.
Menambahkan header X-Robots-Tag agar Googlebot tahu halaman boleh diindeks.
"""


class SEORobotsMiddleware:
    """
    Middleware yang menambahkan X-Robots-Tag header ke setiap response.
    Memastikan Googlebot mengindeks semua halaman publik.
    Admin panel di-exclude (noindex).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Jangan index halaman admin
        if request.path.startswith('/admin-panel/') or request.path.startswith('/django-admin/'):
            response['X-Robots-Tag'] = 'noindex, nofollow'
        else:
            response['X-Robots-Tag'] = 'index, follow'

        return response
