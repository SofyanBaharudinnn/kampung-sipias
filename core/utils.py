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

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


def sanitize_filename(filename):
    """
    Sanitasi nama file agar aman untuk Nginx & Web Server:
    - Menghapus karakter khusus seperti &, ?, #, %, spasi, dll.
    - Mengganti spasi & simbol dengan underscore (_)
    """
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    if not ext:
        ext = '.jpg'

    # Hapus karakter non-alphanumeric selain strip (-) dan underscore (_)
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
    3. Konversi HEIC/HEIF dan RGBA jika diperlukan.
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

                    # Konversi HEIC/HEIF atau RGBA jika perlu
                    if ext in ['.heic', '.heif'] or img.mode in ('P', 'CMYK'):
                        if ext in ['.heic', '.heif']:
                            ext = '.jpg'
                        img = img.convert('RGB')
                        buffer = BytesIO()
                        img.save(buffer, format='JPEG', quality=88, optimize=True)
                        new_name = sanitize_filename(filename)
                        if not new_name.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            new_name = os.path.splitext(new_name)[0] + '.jpg'
                        setattr(instance, field.name, ContentFile(buffer.getvalue(), name=new_name))
                    else:
                        new_name = sanitize_filename(filename)
                        image_file.name = new_name
                except Exception as e:
                    new_name = sanitize_filename(filename)
                    image_file.name = new_name
