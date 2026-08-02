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

# Dynamically register pillow_heif for HEIC files
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except Exception:
    pass


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
    3. Konversi HEIC/HEIF dari iPhone dan RGBA/PNG menjadi JPEG standar.
    4. Reset stream position (seek 0) agar simpan utuh.
    """
    if sender._meta.app_label in ['contenttypes', 'auth', 'sessions', 'admin']:
        return

    for field in instance._meta.fields:
        if isinstance(field, ImageField):
            image_file = getattr(instance, field.name, None)
            if image_file and hasattr(image_file, 'file') and image_file.name:
                # Reset stream pointer
                try:
                    if hasattr(image_file, 'seek'):
                        image_file.seek(0)
                except Exception:
                    pass

                filename = os.path.basename(image_file.name)
                ext = os.path.splitext(filename)[1].lower()
                is_heic = ext in ['.heic', '.heif']

                try:
                    # Registrasi pillow_heif jika belum
                    try:
                        import pillow_heif
                        pillow_heif.register_heif_opener()
                    except Exception:
                        pass

                    img = None
                    if is_heic:
                        try:
                            import pillow_heif
                            image_file.seek(0)
                            heif_obj = pillow_heif.open_heif(image_file.read())
                            img = Image.frombytes(
                                heif_obj.mode,
                                heif_obj.size,
                                heif_obj.data,
                                "raw",
                            )
                        except Exception as heic_err:
                            print(f"[HEIC Open Error]: {heic_err}")
                            if hasattr(image_file, 'seek'):
                                image_file.seek(0)

                    if img is None:
                        if hasattr(image_file, 'seek'):
                            image_file.seek(0)
                        img = Image.open(image_file)

                    # Auto rotate EXIF orientasi HP
                    try:
                        img = ImageOps.exif_transpose(img)
                    except Exception:
                        pass

                    # Tangani transparansi RGBA/LA/P dengan latar belakang putih
                    if img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info):
                        alpha = img.convert('RGBA').split()[-1]
                        bg = Image.new('RGB', img.size, (255, 255, 255))
                        bg.paste(img.convert('RGB'), mask=alpha)
                        img = bg
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')

                    # Resize gambar jika dimensi melebihi 1200px (mencegah disk quota exceeded)
                    max_dim = 1200
                    if img.width > max_dim or img.height > max_dim:
                        try:
                            resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
                        except AttributeError:
                            resample_filter = getattr(Image, 'ANTIALIAS', Image.BICUBIC)
                        img.thumbnail((max_dim, max_dim), resample_filter)

                    # Simpan sebagai JPEG terkompresi
                    buffer = BytesIO()
                    img.save(buffer, format='JPEG', quality=80, optimize=True)
                    buffer.seek(0)

                    # Dapatkan folder upload_to agar file disimpan di folder subdirektori yang benar
                    upload_to = field.upload_to
                    if callable(upload_to):
                        try:
                            upload_to = upload_to(instance, filename)
                        except Exception:
                            upload_to = ""
                    
                    new_name = sanitize_filename(filename, forced_ext='.jpg')
                    upload_to_str = str(upload_to).strip('/')
                    if upload_to_str:
                        new_name = f"{upload_to_str}/{new_name}"

                    setattr(instance, field.name, ContentFile(buffer.getvalue(), name=new_name))

                except Exception as e:
                    print(f"[Image Conversion Exception] {filename}: {e}")
                    # Jika gagal, tetap gunakan sanitize dengan subfolder
                    upload_to = field.upload_to
                    if callable(upload_to):
                        try:
                            upload_to = upload_to(instance, filename)
                        except Exception:
                            upload_to = ""
                    new_name = sanitize_filename(filename)
                    upload_to_str = str(upload_to).strip('/')
                    if upload_to_str:
                        new_name = f"{upload_to_str}/{new_name}"
                    image_file.name = new_name
                    if hasattr(image_file, 'seek'):
                        try:
                            image_file.seek(0)
                        except Exception:
                            pass
