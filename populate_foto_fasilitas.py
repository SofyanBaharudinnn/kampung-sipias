import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import FotoFasilitas, ProfilKampung
from galeri.models import FotoGaleri

profil = ProfilKampung.objects.first()

# Populate sample entries for each category if none exist
sample_photos = FotoGaleri.objects.all()

if sample_photos.exists():
    p_list = list(sample_photos)
    
    # Kesehatan
    if not FotoFasilitas.objects.filter(kategori='kesehatan').exists():
        if profil and profil.foto_fasilitas_kesehatan:
            FotoFasilitas.objects.create(kategori='kesehatan', judul='Gedung Pustu Kampung', foto=profil.foto_fasilitas_kesehatan.name)
        if len(p_list) > 0:
            FotoFasilitas.objects.create(kategori='kesehatan', judul='Pelayanan Posyandu Balita & Lansia', foto=p_list[0].foto.name)

    # Pendidikan
    if not FotoFasilitas.objects.filter(kategori='pendidikan').exists():
        if len(p_list) > 0:
            FotoFasilitas.objects.create(kategori='pendidikan', judul='Sekolah Dasar Kampung Sipias', foto=p_list[0].foto.name)
        if len(p_list) > 1:
            FotoFasilitas.objects.create(kategori='pendidikan', judul='Gedung PAUD Pembina', foto=p_list[1].foto.name)

    # Ibadah
    if not FotoFasilitas.objects.filter(kategori='ibadah').exists():
        if len(p_list) > 1:
            FotoFasilitas.objects.create(kategori='ibadah', judul='Masjid Kampung Sipias', foto=p_list[1].foto.name)
        if len(p_list) > 0:
            FotoFasilitas.objects.create(kategori='ibadah', judul='Kegiatan Keagamaan Warga', foto=p_list[0].foto.name)

    # Umum
    if not FotoFasilitas.objects.filter(kategori='umum').exists():
        if len(p_list) > 0:
            FotoFasilitas.objects.create(kategori='umum', judul='Balai Kampung & Lapangan', foto=p_list[0].foto.name)
        if len(p_list) > 1:
            FotoFasilitas.objects.create(kategori='umum', judul='Kedai & Pos Kamling', foto=p_list[1].foto.name)

print("FOTO FASILITAS SAMPLES CREATED SUCCESSFULLY!")
