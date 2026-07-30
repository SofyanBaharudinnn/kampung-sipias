from django.urls import path
from . import views

app_name = 'berita'

urlpatterns = [
    path('', views.daftar_berita, name='daftar'),
    path('<slug:slug>/', views.detail_berita, name='detail'),
]
