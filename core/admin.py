# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import ProfilKampung, StrukturOrganisasi, PesanKontak

@admin.register(ProfilKampung)
class ProfilKampungAdmin(admin.ModelAdmin):
    list_display = ['nama_kampung', 'distrik', 'kabupaten', 'jumlah_penduduk', 'updated_at']

@admin.register(StrukturOrganisasi)
class StrukturOrganisasiAdmin(admin.ModelAdmin):
    list_display = ['nama', 'jabatan', 'jenis', 'urutan', 'aktif']
    list_filter = ['jenis', 'aktif']
    list_editable = ['urutan', 'aktif']

@admin.register(PesanKontak)
class PesanKontakAdmin(admin.ModelAdmin):
    list_display = ['nama', 'email', 'subjek', 'tanggal', 'dibaca']
    list_filter = ['dibaca']
    readonly_fields = ['nama', 'email', 'subjek', 'pesan', 'tanggal']
