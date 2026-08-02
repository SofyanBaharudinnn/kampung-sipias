import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita, FotoBerita
from PIL import Image

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
            path = b.gambar.path
            print(f"  Path:           {path}")
            exists = os.path.exists(path)
            print(f"  Exists on Disk: {exists}")
            if exists:
                size_mb = os.path.getsize(path) / (1024*1024)
                print(f"  Size:           {size_mb:.2f} MB")
                try:
                    with Image.open(path) as img:
                        img.verify()
                    print("  Pillow Verify:  VALID")
                except Exception as img_err:
                    print(f"  Pillow Verify:  CORRUPTED ({img_err})")
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
            fpath = f.foto.path
            print(f"      Exists on Disk: {os.path.exists(fpath)}")
            if os.path.exists(fpath):
                try:
                    with Image.open(fpath) as img:
                        img.verify()
                    print("      Pillow Verify:  VALID")
                except Exception as img_err:
                    print(f"      Pillow Verify:  CORRUPTED ({img_err})")
        except Exception as e:
            print(f"      Path Error:     {e}")
    print("-" * 60)

