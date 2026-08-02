import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita, FotoBerita
from galeri.models import FotoGaleri, AlbumGaleri
from core.models import FotoFasilitas, ProfilKampung

def fix_field(instance, field_name, expected_prefix):
    field_val = getattr(instance, field_name)
    if not field_val:
        return False
        
    name = field_val.name
    # Jika path tidak dimulai dengan prefix yang diharapkan dan tidak kosong
    if name and not name.startswith(expected_prefix) and not name.startswith('media/'):
        old_name = name
        new_name = f"{expected_prefix.strip('/')}/{name.lstrip('/')}"
        
        # Cek jika file fisik ada di media/ tetapi di database tidak ada prefixnya
        # Pindahkan file fisik jika perlu
        old_physical_path = os.path.join(django.conf.settings.MEDIA_ROOT, old_name)
        new_physical_path = os.path.join(django.conf.settings.MEDIA_ROOT, new_name)
        
        if os.path.exists(old_physical_path):
            os.makedirs(os.path.dirname(new_physical_path), exist_ok=True)
            try:
                os.rename(old_physical_path, new_physical_path)
                print(f"Moved file: {old_name} -> {new_name}")
            except Exception as e:
                print(f"Error moving file: {e}")
                
        # Update database record
        field_val.name = new_name
        instance.save(update_fields=[field_name])
        print(f"Updated DB {instance.__class__.__name__} (ID {instance.id}): {old_name} -> {new_name}")
        return True
    return False

print("=" * 60)
print("FIXING LIVE DATABASE IMAGE PATHS")
print("=" * 60)

# 1. Berita (gambar -> berita/)
print("Fixing Berita...")
for b in Berita.objects.all():
    fix_field(b, 'gambar', 'berita/')

# 2. FotoBerita (foto -> berita/gallery/)
print("Fixing FotoBerita...")
for fb in FotoBerita.objects.all():
    fix_field(fb, 'foto', 'berita/gallery/')

# 3. FotoGaleri (foto -> galeri/foto/)
print("Fixing FotoGaleri...")
for fg in FotoGaleri.objects.all():
    fix_field(fg, 'foto', 'galeri/foto/')

# 4. AlbumGaleri (sampul -> galeri/sampul/)
print("Fixing AlbumGaleri...")
for alb in AlbumGaleri.objects.all():
    fix_field(alb, 'sampul', 'galeri/sampul/')

# 5. FotoFasilitas (foto -> fasilitas/)
print("Fixing FotoFasilitas...")
for ff in FotoFasilitas.objects.all():
    fix_field(ff, 'foto', 'fasilitas/')

# 6. ProfilKampung
print("Fixing ProfilKampung...")
for pk in ProfilKampung.objects.all():
    fix_field(pk, 'foto_kepala', 'profil/')
    fix_field(pk, 'foto_kantor', 'profil/')
    fix_field(pk, 'foto_fasilitas_kesehatan', 'profil/')
    fix_field(pk, 'foto_fasilitas_pendidikan', 'profil/')
    fix_field(pk, 'foto_fasilitas_ibadah', 'profil/')
    fix_field(pk, 'foto_fasilitas_umum', 'profil/')

print("=" * 60)
print("Database fix completed!")
print("=" * 60)
