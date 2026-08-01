import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita, FotoBerita
from galeri.models import FotoGaleri
from django.core.files.base import ContentFile

base_dir = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(base_dir, 'static', 'images')

def fix_all_broken_images():
    print("=== Checking all Berita in Database ===")
    berita_list = Berita.objects.all()
    sample_images = ['gotong_royong.jpg', 'hero_bg_kampung.jpg', 'foto_udara_kampung.jpg']

    for idx, b in enumerate(berita_list):
        is_broken = False
        if not b.gambar or not b.gambar.name:
            is_broken = True
        else:
            name_lower = b.gambar.name.lower()
            if name_lower.endswith('.heic') or name_lower.endswith('.heif'):
                is_broken = True
            else:
                try:
                    if not os.path.exists(b.gambar.path) or os.path.getsize(b.gambar.path) < 100:
                        is_broken = True
                except Exception:
                    is_broken = True

        if is_broken:
            selected_img = sample_images[idx % len(sample_images)]
            img_path = os.path.join(static_img_dir, selected_img)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    new_filename = f"berita_fixed_{b.id}_{selected_img}"
                    b.gambar.save(new_filename, ContentFile(f.read()), save=True)
                print(f"[FIXED] Berita '{b.judul}' -> {b.gambar.name}")

    print("\n=== Checking all FotoGaleri in Database ===")
    galeri_list = FotoGaleri.objects.all()
    for idx, g in enumerate(galeri_list):
        is_broken = False
        if not g.foto or not g.foto.name:
            is_broken = True
        else:
            name_lower = g.foto.name.lower()
            if name_lower.endswith('.heic') or name_lower.endswith('.heif'):
                is_broken = True
            else:
                try:
                    if not os.path.exists(g.foto.path) or os.path.getsize(g.foto.path) < 100:
                        is_broken = True
                except Exception:
                    is_broken = True

        if is_broken:
            selected_img = sample_images[idx % len(sample_images)]
            img_path = os.path.join(static_img_dir, selected_img)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    new_filename = f"galeri_fixed_{g.id}_{selected_img}"
                    g.foto.save(new_filename, ContentFile(f.read()), save=True)
                print(f"[FIXED] Galeri '{g.judul}' -> {g.foto.name}")

if __name__ == '__main__':
    fix_all_broken_images()
