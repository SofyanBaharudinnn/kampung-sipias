import os
import django
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita, FotoBerita
from galeri.models import FotoGaleri

def compress_file(path, max_dim=1200, quality=80):
    if not path or not os.path.exists(path):
        return False
    try:
        size_before = os.path.getsize(path)
        if size_before < 300 * 1024:  # Lewati jika sudah kurang dari 300KB
            return False
            
        img = Image.open(path)
        
        # Auto rotate EXIF orientasi
        try:
            from PIL import ImageOps
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        # Convert to RGB
        if img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img.convert('RGB'), mask=alpha)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # Resize jika terlalu besar
        if img.width > max_dim or img.height > max_dim:
            try:
                resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
            except AttributeError:
                resample_filter = getattr(Image, 'ANTIALIAS', Image.BICUBIC)
            img.thumbnail((max_dim, max_dim), resample_filter)

        img.save(path, format='JPEG', quality=quality, optimize=True)
        size_after = os.path.getsize(path)
        print(f"Compressed {os.path.basename(path)}: {size_before/(1024*1024):.2f}MB -> {size_after/(1024*1024):.2f}MB")
        return True
    except Exception as e:
        print(f"Error compressing {path}: {e}")
        return False

print("=" * 60)
print("COMPRESSING EXISTING IMAGES ON SERVER")
print("=" * 60)

# Compress all Berita images
print("Processing Berita...")
for b in Berita.objects.all():
    if b.gambar:
        compress_file(b.gambar.path)

# Compress all FotoBerita images
print("Processing FotoBerita...")
for fb in FotoBerita.objects.all():
    if fb.foto:
        compress_file(fb.foto.path)

# Compress all FotoGaleri images
print("Processing FotoGaleri...")
for fg in FotoGaleri.objects.all():
    if fg.foto:
        compress_file(fg.foto.path)

print("=" * 60)
print("Finished compressing all images!")
print("=" * 60)
