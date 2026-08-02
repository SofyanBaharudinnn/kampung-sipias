import os
import stat
import django
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

print("=" * 60)
print("DIAGNOSTIK GAMBAR BERITA")
print("=" * 60)

def get_file_info(path):
    if not os.path.exists(path):
        return "Not found"
    try:
        info = os.stat(path)
        mode = info.st_mode
        perms = stat.filemode(mode)
        uid = info.st_uid
        gid = info.st_gid
        return f"Perms: {perms} | UID: {uid} | GID: {gid} | Size: {info.st_size / (1024*1024):.2f} MB"
    except Exception as e:
        return f"Error: {e}"

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
            print(f"  File Info:      {get_file_info(path)}")
            if os.path.exists(path):
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
    print("-" * 60)


