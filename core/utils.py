import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import ImageField
from django.db.models.signals import pre_save
from django.dispatch import receiver

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass


@receiver(pre_save)
def auto_convert_heic_to_jpg(sender, instance, **kwargs):
    """
    Signal handler untuk otomatis mengkonversi file foto berformat HEIC/HEIF (dari iPhone)
    menjadi format JPEG standar saat model disimpan ke database.
    """
    # Abaikan model internal Django jika ada
    if sender._meta.app_label in ['contenttypes', 'auth', 'sessions', 'admin']:
        return

    for field in instance._meta.fields:
        if isinstance(field, ImageField):
            image_file = getattr(instance, field.name, None)
            if image_file and hasattr(image_file, 'file') and image_file.name:
                ext = os.path.splitext(image_file.name)[1].lower()
                if ext in ['.heic', '.heif']:
                    try:
                        image_file.open('rb')
                        img = Image.open(image_file)
                        img = img.convert('RGB')

                        buffer = BytesIO()
                        img.save(buffer, format='JPEG', quality=90)

                        base_filename = os.path.splitext(os.path.basename(image_file.name))[0]
                        new_filename = f"{base_filename}.jpg"

                        content = ContentFile(buffer.getvalue(), name=new_filename)
                        setattr(instance, field.name, content)
                    except Exception as e:
                        print(f"[HEIC Auto-Converter Error] Gagal mengonversi {image_file.name}: {e}")
