import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from berita.models import Berita

all_berita = Berita.objects.all()
print("TOTAL BERITA IN DB:", all_berita.count())
for b in all_berita:
    print(f"ID: {b.id} | Judul: '{b.judul}' | Status: '{b.status}' | Jenis: '{b.jenis}'")

# Automatically publish any draft news if user created it as draft
for b in all_berita:
    if b.status == 'draft':
        b.status = 'published'
        b.save()
        print(f"--> Updated berita ID {b.id} '{b.judul}' status from draft to published!")
