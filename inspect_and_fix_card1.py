import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

def inspect_all():
    print("=" * 60)
    print("INSPECTING ALL BERITA ITEMS IN DATABASE")
    print("=" * 60)
    for b in Berita.objects.all().order_by('-id'):
        print(f"ID: {b.id}")
        print(f"Judul: {b.judul}")
        if b.gambar:
            print(f"Gambar Name: {b.gambar.name}")
            print(f"Gambar URL:  {b.gambar.url}")
            try:
                path = b.gambar.path
                print(f"Gambar Path: {path}")
                print(f"File Exists: {os.path.exists(path)}")
                if os.path.exists(path):
                    print(f"File Size:   {os.path.getsize(path)} bytes")
            except Exception as e:
                print(f"Path Error:  {e}")
        else:
            print("Gambar: None")
        print("-" * 60)

if __name__ == '__main__':
    inspect_all()
