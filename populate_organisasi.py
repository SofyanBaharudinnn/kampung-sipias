import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import StrukturOrganisasi

# Reset existing records
StrukturOrganisasi.objects.all().delete()

data = [
    # Top Leader
    {"urutan": 1, "nama": "IMAM SAPI’I", "jabatan": "KEPALA KAMPUNG"},
    
    # Sekretaris
    {"urutan": 2, "nama": "HATTA-IBRAHIM", "jabatan": "SEKRETARIS KAMPUNG"},
    
    # Urusan (Kaur)
    {"urutan": 3, "nama": "SUJIMAN", "jabatan": "KEPALA URUSAN TATA USAHA DAN UMUM"},
    {"urutan": 4, "nama": "TANI PURNAMASARI", "jabatan": "KEPALA URUSAN KEUANGAN"},
    {"urutan": 5, "nama": "PURWANTO", "jabatan": "KEPALA URUSAN PERENCANAAN"},
    
    # Seksi (Kasi)
    {"urutan": 6, "nama": "NURKHOLIS", "jabatan": "KEPALA SEKSI PEMERINTAHAN"},
    {"urutan": 7, "nama": "MAMAD", "jabatan": "KEPALA SEKSI KESEJAHTERAAN"},
    {"urutan": 8, "nama": "ERNAWATI", "jabatan": "KEPALA SEKSI PELAYANAN"},
    
    # RW 01 & RT
    {"urutan": 9, "nama": "SYAHRUL", "jabatan": "KETUA RW.01"},
    {"urutan": 10, "nama": "SUPRATMIN", "jabatan": "KETUA RT.01"},
    {"urutan": 11, "nama": "HASAN ASNAWI", "jabatan": "KETUA RT.02"},
    {"urutan": 12, "nama": "KABID IRIANTO", "jabatan": "KETUA RT.03"},
    
    # RW 02 & RT
    {"urutan": 13, "nama": "WAKIDI", "jabatan": "KETUA RW.02"},
    {"urutan": 14, "nama": "KUSNADI", "jabatan": "KETUA RT.04"},
    {"urutan": 15, "nama": "WAHKID", "jabatan": "KETUA RT.05"},
]

for item in data:
    StrukturOrganisasi.objects.create(
        nama=item["nama"],
        jabatan=item["jabatan"],
        jenis="pemerintah",
        urutan=item["urutan"],
        aktif=True
    )

print("SUCCESSFULLY POPULATED STRUKTUR ORGANISASI KAMPUNG SIPIAS!")
