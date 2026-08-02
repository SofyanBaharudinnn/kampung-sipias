import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita, FotoBerita

print("=" * 60)
print("DIAGNOSTIK GAMBAR BERITA")
print("=" * 60)

all_berita = Berita.objects.all().order_by('-id')[:5]
for b in all_berita:
    print(f"ID: {b.id}")
    print(f"Judul: {b.judul}")
    print(f"Status: {b.status}")
    if b.gambar:
        print(f"  Database Field: {b.gambar.name}")
        print(f"  URL:            {b.gambar.url}")
        try:
            print(f"  Path:           {b.gambar.path}")
            print(f"  Exists on Disk: {os.path.exists(b.gambar.path)}")
            if os.path.exists(b.gambar.path):
                print(f"  Size:           {os.path.getsize(b.gambar.path) / (1024*1024):.2f} MB")
        except Exception as e:
            print(f"  Path Error:     {e}")
    else:
        print("  Database Field: None/Kosong")
        
    # Cek foto tambahan
    fotos = b.foto_tambahan.all()
    print(f"  Foto Tambahan ({fotos.count()} file):")
    for idx, f in enumerate(fotos):
        print(f"    - Foto #{idx+1}: {f.foto.name}")
        try:
            print(f"      Exists on Disk: {os.path.exists(f.foto.path)}")
        except Exception as e:
            print(f"      Path Error:     {e}")
    print("-" * 60)
