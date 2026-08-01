"""URL configuration for kampung_sipias project."""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from core import views as core_views

urlpatterns = [
    path('googled34dee6d910c2bc4.html', core_views.google_verification),
    path('robots.txt', core_views.robots_txt),
    path('sitemap.xml', core_views.sitemap_xml),
    path('django-admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', include('core.urls')),
    path('berita/', include('berita.urls')),
    path('galeri/', include('galeri.urls')),
    path('admin-panel/', include(('core.admin_urls', 'core'), namespace='admin_panel')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
