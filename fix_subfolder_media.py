import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

def fix_berita_subfolders():
    print("=== Fixing Berita Subfolder Paths in Database ===")
    for b in Berita.objects.all():
        if b.gambar and b.gambar.name:
            if not b.gambar.name.startswith('berita/'):
                old_name = b.gambar.name
                new_name = f"berita/{old_name}"
                b.gambar.name = new_name
                b.save()
                print(f"[FIXED] Berita #{b.id}: '{old_name}' -> '{new_name}'")

if __name__ == '__main__':
    fix_berita_subfolders()
