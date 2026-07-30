import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import ProfilKampung

profil, _ = ProfilKampung.objects.get_or_create(id=1)
profil.jumlah_penduduk = 641
profil.jumlah_kk = 205
profil.jumlah_laki = 354
profil.jumlah_perempuan = 287
profil.save()

print("BERHASIL DIPERBARUI:")
print(f"  Jumlah Penduduk : {profil.jumlah_penduduk} jiwa")
print(f"  Jumlah KK       : {profil.jumlah_kk} KK")
print(f"  Laki-laki       : {profil.jumlah_laki}")
print(f"  Perempuan       : {profil.jumlah_perempuan}")
