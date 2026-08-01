import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

def reset_berita_photos():
    print("=== Clearing Auto-Assigned Sample Photos ===")
    for b in Berita.objects.all():
        if b.gambar and ('fixed' in b.gambar.name or 'sample' in b.gambar.name):
            try:
                b.gambar.delete(save=False)
            except Exception:
                pass
            b.gambar = None
            b.save()
            print(f"[RESET] Cleared auto-assigned photo for Berita #{b.id}: '{b.judul}'")

if __name__ == '__main__':
    reset_berita_photos()
