from django.urls import path
from . import admin_views

app_name = 'core'

urlpatterns = [
    path('login/', admin_views.admin_login, name='admin_login'),
    path('logout/', admin_views.admin_logout, name='admin_logout'),
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    # Berita
    path('berita/', admin_views.admin_berita_list, name='admin_berita_list'),
    path('berita/tambah/', admin_views.admin_berita_tambah, name='admin_berita_tambah'),
    path('berita/edit/<int:pk>/', admin_views.admin_berita_edit, name='admin_berita_edit'),
    path('berita/hapus/<int:pk>/', admin_views.admin_berita_hapus, name='admin_berita_hapus'),
    path('berita/gambar-hapus/<int:pk>/', admin_views.admin_berita_gambar_hapus, name='admin_berita_gambar_hapus'),
    path('berita/foto-hapus/<int:foto_pk>/', admin_views.admin_berita_foto_hapus, name='admin_berita_foto_hapus'),
    # Galeri
    path('galeri/', admin_views.admin_galeri_list, name='admin_galeri_list'),
    path('galeri/upload/', admin_views.admin_galeri_upload, name='admin_galeri_upload'),
    path('galeri/edit/<int:pk>/', admin_views.admin_galeri_edit, name='admin_galeri_edit'),
    path('galeri/hapus/<int:pk>/', admin_views.admin_galeri_hapus, name='admin_galeri_hapus'),
    # Pesan
    path('pesan/', admin_views.admin_pesan_list, name='admin_pesan_list'),
    path('pesan/<int:pk>/', admin_views.admin_pesan_detail, name='admin_pesan_detail'),
    # Profil
    path('profil/', admin_views.admin_profil_edit, name='admin_profil_edit'),
    path('profil/hapus-foto/<str:field_name>/', admin_views.admin_profil_hapus_foto, name='admin_profil_hapus_foto'),
    # Fasilitas
    path('fasilitas/', admin_views.admin_fasilitas_list, name='admin_fasilitas_list'),
    path('fasilitas/upload/', admin_views.admin_fasilitas_upload, name='admin_fasilitas_upload'),
    path('fasilitas/edit/<int:pk>/', admin_views.admin_fasilitas_edit, name='admin_fasilitas_edit'),
    path('fasilitas/hapus/<int:pk>/', admin_views.admin_fasilitas_hapus, name='admin_fasilitas_hapus'),
]
