from django.contrib import admin
from .models import AlbumGaleri, FotoGaleri

@admin.register(AlbumGaleri)
class AlbumGaleriAdmin(admin.ModelAdmin):
    list_display = ['nama', 'tanggal']

@admin.register(FotoGaleri)
class FotoGaleriAdmin(admin.ModelAdmin):
    list_display = ['judul', 'album', 'tanggal', 'unggulan']
    list_filter = ['unggulan', 'album']
    list_editable = ['unggulan']
