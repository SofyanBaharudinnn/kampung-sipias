import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita
from django.core.files.base import ContentFile

base_dir = os.path.dirname(os.path.abspath(__file__))
static_img_dir = os.path.join(base_dir, 'static', 'images')

sample_images = [
    'hero_bg_kampung.jpg',
    'foto_udara_kampung.jpg',
    'gotong_royong.jpg',
]

def fix_all_berita_images():
    items = Berita.objects.all().order_by('id')
    print(f"Total berita found: {items.count()}")
    for idx, b in enumerate(items):
        selected_img = sample_images[idx % len(sample_images)]
        img_path = os.path.join(static_img_dir, selected_img)
        if not os.path.exists(img_path):
            img_path = os.path.join(static_img_dir, 'hero_bg_kampung.jpg')

        if os.path.exists(img_path):
            with open(img_path, 'rb') as f:
                file_name = f"berita_{b.id}_foto.jpg"
                b.gambar.save(file_name, ContentFile(f.read()), save=True)
            print(f"[OK] Assigned clean image for Berita #{b.id} ({b.jenis}): '{b.judul}' -> {b.gambar.name}")

if __name__ == '__main__':
    fix_all_berita_images()
