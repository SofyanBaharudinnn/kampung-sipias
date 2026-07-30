import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

updated = Berita.objects.all().update(unggulan=True)
print(f"SUCCESSFULLY UPDATED {updated} BERITA RECORDS TO UNGGULAN = TRUE")
