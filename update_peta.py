import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import ProfilKampung

p = ProfilKampung.objects.first()
if p:
    p.peta_iframe = '<iframe src="https://maps.google.com/maps?q=Sipias,+Distrik+Elikobel,+Kabupaten+Merauke,+Papua+Selatan&t=&z=12&ie=UTF8&iwloc=&output=embed" width="100%" height="500" style="border:0; width:100%; height:100%;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
    p.save()
    print("SAVED PETA IFRAME SUCCESSFULLY!")
