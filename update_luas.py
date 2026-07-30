import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import ProfilKampung

profil, _ = ProfilKampung.objects.get_or_create(id=1)
profil.luas_wilayah = "11,33 km²"
profil.save()

print("SUCCESSFULLY UPDATED LUAS WILAYAH TO 11,33 km²")
