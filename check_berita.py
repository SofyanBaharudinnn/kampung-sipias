import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

print("=" * 60)
print("DAFTAR LENGKAP BERITA DI DATABASE")
print("=" * 60)

for b in Berita.objects.all().order_by('-id'):
    print(f"ID: {b.id}")
    print(f"Judul: {b.judul}")
    print(f"Slug:  {b.slug}")
    print(f"Status: {b.status}")
    if b.gambar:
        print(f"  Gambar Field: {b.gambar.name}")
        print(f"  Gambar URL:  {b.gambar.url}")
    else:
        print("  Gambar Field: None")
    print("-" * 60)



