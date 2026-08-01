import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita
from django.core.files.base import ContentFile

base_dir = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(base_dir, 'static', 'images')

def fix_card1_and_5():
    sample_images = ['gotong_royong.jpg', 'hero_bg_kampung.jpg', 'foto_udara_kampung.jpg']

    all_berita = Berita.objects.all().order_by('-id')
    print(f"Total berita di database: {all_berita.count()}")

    for idx, b in enumerate(all_berita):
        is_invalid = False
        if not b.gambar or not b.gambar.name:
            is_invalid = True
        else:
            try:
                if not os.path.exists(b.gambar.path):
                    is_invalid = True
            except Exception:
                is_invalid = True

        if is_invalid:
            selected_img = sample_images[idx % len(sample_images)]
            img_path = os.path.join(static_img_dir, selected_img)
            if os.path.exists(img_path):
                with open(img_path, 'rb') as f:
                    new_filename = f"berita/fixed_berita_{b.id}.jpg"
                    b.gambar.save(new_filename, ContentFile(f.read()), save=True)
                    print(f"[BERHASIL DIPERBAIKI] Berita #{b.id} '{b.judul}' -> {b.gambar.name}")
        else:
            print(f"[SUDAH OK] Berita #{b.id} '{b.judul}' -> {b.gambar.name}")

if __name__ == '__main__':
    fix_card1_and_5()
