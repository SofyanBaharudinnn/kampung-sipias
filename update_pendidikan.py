import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import ProfilKampung

profil, _ = ProfilKampung.objects.get_or_create(id=1)
profil.fasilitas_pendidikan = 3
profil.save()

print("SUCCESSFULLY UPDATED FASILITAS PENDIDIKAN TO 3")
