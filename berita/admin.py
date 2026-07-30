from django.contrib import admin
from .models import Berita, KategoriBerita

@admin.register(KategoriBerita)
class KategoriBeritaAdmin(admin.ModelAdmin):
    list_display = ['nama', 'slug']
    prepopulated_fields = {'slug': ('nama',)}

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ['judul', 'jenis', 'status', 'penulis', 'tanggal_publish', 'views', 'unggulan']
    list_filter = ['status', 'jenis', 'unggulan']
    search_fields = ['judul', 'konten']
    prepopulated_fields = {'slug': ('judul',)}
    list_editable = ['status', 'unggulan']
