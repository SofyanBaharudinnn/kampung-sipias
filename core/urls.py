# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('profil/', views.profil_kampung, name='profil'),
    path('sejarah/', views.sejarah, name='sejarah'),
    path('visi-misi/', views.visi_misi, name='visi_misi'),
    path('peta/', views.peta_wilayah, name='peta'),
    path('fasilitas/', views.fasilitas, name='fasilitas'),
    path('pemerintahan/', views.pemerintahan, name='pemerintahan'),
    path('kontak/', views.kontak, name='kontak'),
]
