import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from PIL import Image
from berita.models import Berita, FotoBerita
from galeri.models import FotoGaleri
from django.core.files.base import ContentFile

base_dir = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(base_dir, 'static', 'images')

def is_image_valid(file_path):
    """Cek apakah file foto benar-benar valid dan bisa dibaca oleh Pillow (bukan file HEIC/rusak)."""
    if not file_path or not os.path.exists(file_path):
        return False
    if os.path.getsize(file_path) < 100:
        return False
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def fix_all_broken_images(force=False):
    print("=== Periksa dan Perbaiki Foto Berita & Galeri di Database ===")
    sample_images = ['gotong_royong.jpg', 'hero_bg_kampung.jpg', 'foto_udara_kampung.jpg']

    # 1. PERBAIKI BERITA
    berita_list = Berita.objects.all()
    print(f"Total berita ditemukan: {berita_list.count()}")
    for idx, b in enumerate(berita_list):
        is_broken = force
        if not is_broken:
            if not b.gambar or not b.gambar.name:
                is_broken = True
            else:
                name_lower = b.gambar.name.lower()
                if name_lower.endswith('.heic') or name_lower.endswith('.heif'):
                    is_broken = True
                else:
                    try:
                        if not is_image_valid(b.gambar.path):
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
                print(f"[OK] Foto Berita #{b.id} '{b.judul}' -> Berhasil Diperbarui: {b.gambar.name}")

    # 2. PERBAIKI GALERI
    galeri_list = FotoGaleri.objects.all()
    print(f"\nTotal foto galeri ditemukan: {galeri_list.count()}")
    for idx, g in enumerate(galeri_list):
        is_broken = force
        if not is_broken:
            if not g.foto or not g.foto.name:
                is_broken = True
            else:
                name_lower = g.foto.name.lower()
                if name_lower.endswith('.heic') or name_lower.endswith('.heif'):
                    is_broken = True
                else:
                    try:
                        if not is_image_valid(g.foto.path):
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
                print(f"[OK] Foto Galeri #{g.id} '{g.judul}' -> Berhasil Diperbarui: {g.foto.name}")

    print("\n[OK] Pembersihan database selesai!")

if __name__ == '__main__':
    force_flag = '--force' in sys.argv or '-f' in sys.argv
    fix_all_broken_images(force=force_flag)
