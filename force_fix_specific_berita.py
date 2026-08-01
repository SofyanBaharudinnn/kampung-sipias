import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita
from django.core.files.base import ContentFile

base_dir = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(base_dir, 'static', 'images')

def fix_all_broken_berita():
    items = Berita.objects.all()
    print(f"Total berita ditemukan: {items.count()}")

    sample_images = ['gotong_royong.jpg', 'hero_bg_kampung.jpg', 'foto_udara_kampung.jpg']

    for idx, b in enumerate(items):
        sample_name = sample_images[idx % len(sample_images)]
        sample_img_path = os.path.join(static_img_dir, sample_name)

        if os.path.exists(sample_img_path):
            with open(sample_img_path, 'rb') as f:
                new_name = f"berita/berita_fixed_{b.id}_{sample_name}"
                b.gambar.save(new_name, ContentFile(f.read()), save=True)
                print(f"[BERHASIL] Foto Berita #{b.id} '{b.judul}' -> {b.gambar.name}")

if __name__ == '__main__':
    fix_all_broken_berita()
