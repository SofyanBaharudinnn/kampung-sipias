import os
import re
import uuid
import time
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Register HEIC opener for iPhone images
HAS_HEIF = False
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    HAS_HEIF = True
except Exception:
    HAS_HEIF = False


def sanitize_filename(filename, forced_ext=None):
    """
    Sanitasi nama file agar aman untuk Nginx & Web Server:
    - Menghapus karakter khusus seperti &, ?, #, %, spasi, dll.
    - Mengganti spasi & simbol dengan underscore (_)
    """
    name, ext = os.path.splitext(filename)
    if forced_ext:
        ext = forced_ext
    else:
        ext = ext.lower()
        if not ext:
            ext = '.jpg'

    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')

    if not clean_name:
        clean_name = "foto"

    unique_suffix = f"{int(time.time())}_{uuid.uuid4().hex[:6]}"
    return f"{clean_name[:40]}_{unique_suffix}{ext}"


@receiver(pre_save)
def process_uploaded_images(sender, instance, **kwargs):
    """
    Signal handler untuk:
    1. Membersihkan nama file (menghapus & dan spasi agar tidak 404 di Nginx).
    2. Auto-rotate gambar sesuai EXIF orientasi HP.
    3. Konversi HEIC/HEIF dari iPhone menjadi JPEG standar.
    """
    if sender._meta.app_label in ['contenttypes', 'auth', 'sessions', 'admin']:
        return

    for field in instance._meta.fields:
        if isinstance(field, ImageField):
            image_file = getattr(instance, field.name, None)
            if image_file and hasattr(image_file, 'file') and image_file.name:
                filename = os.path.basename(image_file.name)
                ext = os.path.splitext(filename)[1].lower()

                try:
                    image_file.open('rb')
                    img = Image.open(image_file)

                    # Auto rotate berdasarkan EXIF HP
                    try:
                        img = ImageOps.exif_transpose(img)
                    except Exception:
                        pass

                    # Konversi HEIC/HEIF atau RGBA/P/CMYK ke RGB JPG standar
                    if ext in ['.heic', '.heif'] or img.mode in ('RGBA', 'P', 'CMYK'):
                        if img.mode != 'RGB':
                            img = img.convert('RGB')
                        buffer = BytesIO()
                        img.save(buffer, format='JPEG', quality=88, optimize=True)
                        new_name = sanitize_filename(filename, forced_ext='.jpg')
                        setattr(instance, field.name, ContentFile(buffer.getvalue(), name=new_name))
                    else:
                        new_name = sanitize_filename(filename)
                        image_file.name = new_name
                except Exception as e:
                    target_ext = '.jpg' if ext in ['.heic', '.heif'] else ext
                    new_name = sanitize_filename(filename, forced_ext=target_ext)
                    image_file.name = new_name
