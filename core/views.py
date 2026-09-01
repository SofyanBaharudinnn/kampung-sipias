# pyrefly: ignore [missing-import]
from django.shortcuts import render, get_object_or_404, redirect
# pyrefly: ignore [missing-import]
from django.contrib import messages
from .models import ProfilKampung, StrukturOrganisasi, PesanKontak, FotoFasilitas
from berita.models import Berita
from galeri.models import FotoGaleri


def get_profil():
    """Helper untuk mengambil profil kampung"""
    profil, _ = ProfilKampung.objects.get_or_create(id=1)
    return profil


def get_foto_fasilitas_dict():
    return {
        'foto_kesehatan': FotoFasilitas.objects.filter(kategori='kesehatan'),
        'foto_pendidikan': FotoFasilitas.objects.filter(kategori='pendidikan'),
        'foto_ibadah': FotoFasilitas.objects.filter(kategori='ibadah'),
        'foto_umum': FotoFasilitas.objects.filter(kategori='umum'),
    }


def landing(request):
    """Halaman utama / landing page"""
    profil = get_profil()
    berita_terbaru = Berita.objects.filter(status='published').order_by('-tanggal_publish')[:3]
    foto_unggulan = FotoGaleri.objects.filter(unggulan=True)[:6]
    context = {
        'profil': profil,
        'berita_terbaru': berita_terbaru,
        'foto_unggulan': foto_unggulan,
        'page_title': 'Beranda',
        **get_foto_fasilitas_dict(),
    }
    # Render landing page
    return render(request, 'core/landing.html', context)


def profil_kampung(request):
    """Halaman profil kampung"""
    profil = get_profil()
    context = {
        'profil': profil,
        'page_title': 'Profil Kampung',
    }
    return render(request, 'core/profil.html', context)


def sejarah(request):
    """Halaman Sejarah Kampung"""
    profil = get_profil()
    context = {
        'profil': profil,
        'page_title': 'Sejarah Kampung',
    }
    return render(request, 'core/sejarah.html', context)


def visi_misi(request):
    """Halaman Visi & Misi kampung"""
    profil = get_profil()
    context = {
        'profil': profil,
        'page_title': 'Visi & Misi',
    }
    return render(request, 'core/visi_misi.html', context)


def peta_wilayah(request):
    """Halaman Peta Wilayah kampung"""
    profil = get_profil()
    context = {
        'profil': profil,
        'page_title': 'Peta Wilayah',
    }
    return render(request, 'core/peta.html', context)


def fasilitas(request):
    """Halaman Fasilitas Kampung"""
    profil = get_profil()
    context = {
        'profil': profil,
        'page_title': 'Fasilitas Kampung',
        **get_foto_fasilitas_dict(),
    }
    return render(request, 'core/fasilitas.html', context)


def pemerintahan(request):
    """Halaman struktur pemerintahan"""
    profil = get_profil()
    pemerintah = StrukturOrganisasi.objects.filter(jenis='pemerintah', aktif=True)
    bpk = StrukturOrganisasi.objects.filter(jenis='bpk', aktif=True)
    context = {
        'profil': profil,
        'pemerintah': pemerintah,
        'bpk': bpk,
        'page_title': 'Struktur Organisasi',
    }
    return render(request, 'core/pemerintahan.html', context)


def kontak(request):
    """Halaman kontak dengan form pesan"""
    profil = get_profil()
    if request.method == 'POST':
        nama = request.POST.get('nama', '').strip()
        email = request.POST.get('email', '').strip()
        subjek = request.POST.get('subjek', '').strip()
        pesan = request.POST.get('pesan', '').strip()
        if nama and email and subjek and pesan:
            PesanKontak.objects.create(
                nama=nama, email=email, subjek=subjek, pesan=pesan
            )
            messages.success(request, 'Pesan Anda berhasil terkirim! Kami akan segera menghubungi Anda.')
            return redirect('core:kontak')
        else:
            messages.error(request, 'Harap isi semua kolom yang tersedia.')
    context = {
        'profil': profil,
        'page_title': 'Kontak',
    }
    return render(request, 'core/kontak.html', context)


def robots_txt(request):
    """View untuk menyajikan robots.txt bagi Googlebot"""
    from django.http import HttpResponse
    lines = [
        "User-agent: *",
        "Disallow: /admin-panel/",
        "Disallow: /django-admin/",
        "Allow: /",
        "Sitemap: https://kampungsipias.my.id/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """View untuk sitemap XML dinamis agar Google mudah mengindeks semua halaman"""
    from django.http import HttpResponse
    from django.utils import timezone
    domain = "https://kampungsipias.my.id"
    today = timezone.now().strftime('%Y-%m-%d')

    # Halaman statis
    static_pages = [
        {"loc": "", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/profil/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/sejarah/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/visi-misi/", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/peta/", "priority": "0.7", "changefreq": "monthly"},
        {"loc": "/fasilitas/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/pemerintahan/", "priority": "0.8", "changefreq": "monthly"},
        {"loc": "/kontak/", "priority": "0.6", "changefreq": "monthly"},
        {"loc": "/berita/", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/galeri/", "priority": "0.7", "changefreq": "weekly"},
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in static_pages:
        xml.append(f'  <url>')
        xml.append(f'    <loc>{domain}{page["loc"]}</loc>')
        xml.append(f'    <lastmod>{today}</lastmod>')
        xml.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{page["priority"]}</priority>')
        xml.append(f'  </url>')

    # Halaman berita dinamis
    berita_list = Berita.objects.filter(status='published').order_by('-tanggal_publish')
    for berita in berita_list:
        lastmod = berita.tanggal_update.strftime('%Y-%m-%d') if berita.tanggal_update else today
        xml.append(f'  <url>')
        xml.append(f'    <loc>{domain}/berita/{berita.slug}/</loc>')
        xml.append(f'    <lastmod>{lastmod}</lastmod>')
        xml.append(f'    <changefreq>weekly</changefreq>')
        xml.append(f'    <priority>0.7</priority>')
        xml.append(f'  </url>')

    xml.append('</urlset>')
    return HttpResponse("\n".join(xml), content_type="application/xml")


def google_verification(request):
    """View verifikasi kepemilikan Google Search Console"""
    from django.http import HttpResponse
    return HttpResponse("google-site-verification: googled34dee6d910c2bc4.html", content_type="text/html")


def debug_media(request):
    """View debug untuk mengecek database dan folder & file media di PythonAnywhere"""
    import os
    from django.conf import settings
    from django.http import HttpResponse
    from django.db import connection
    from berita.models import Berita

    db_path = connection.settings_dict.get('NAME', 'Unknown')
    media_dir = str(settings.MEDIA_ROOT)
    
    output = [
        "<h3>DATABASE INFO</h3>",
        f"<p>Database Path in settings: <code>{db_path}</code></p>",
        f"<p>Database File Exists: <b>{os.path.exists(str(db_path))}</b></p>",
        "<hr><h3>BERITA IN LIVE DB:</h3><ul>"
    ]

    try:
        for b in Berita.objects.all().order_by('-id')[:5]:
            img_val = b.gambar.name if b.gambar else 'None'
            output.append(f"<li>ID: {b.id} | Slug: {b.slug} | Gambar Field: {img_val}</li>")
    except Exception as db_err:
        output.append(f"<li>Error querying database: {db_err}</li>")

    output.append("</ul><hr><h3>MEDIA_ROOT INFO</h3>")
    output.append(f"<p>MEDIA_ROOT Path: <code>{media_dir}</code></p>")
    output.append(f"<p>Folder Exists: <b>{os.path.exists(media_dir)}</b></p>")
    output.append("<hr><h4>DAFTAR FILE MEDIA SAAT INI:</h4><ul>")

    if os.path.exists(media_dir):
        count = 0
        for root, dirs, files in os.walk(media_dir):
            for f in files:
                filepath = os.path.join(root, f)
                rel_path = os.path.relpath(filepath, media_dir).replace('\\', '/')
                url_path = f"/uploads/{rel_path}"
                size_kb = round(os.path.getsize(filepath) / 1024, 1)
                output.append(f'<li><a href="{url_path}" target="_blank">{url_path}</a> ({size_kb} KB)</li>')
                count += 1
        if count == 0:
            output.append('<li><i>Folder media kosong. Belum ada file ter-upload di folder media server ini.</i></li>')
    output.append("</ul>")

    return HttpResponse("\n".join(output), content_type="text/html")


import mimetypes
from django.http import HttpResponse, Http404

def custom_media_serve(request, path):
    """Serving media & uploaded images reliably on PythonAnywhere uWSGI without broken images"""
    import os
    from django.conf import settings

    clean_path = str(path).lstrip('/')

    # 1. Try MEDIA_ROOT / clean_path (e.g. media/berita/foto.jpg)
    file_path = os.path.join(settings.MEDIA_ROOT, clean_path)

    # 2. Try MEDIA_ROOT / basename (e.g. media/foto.jpg)
    if not os.path.exists(file_path):
        file_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(clean_path))

    # 3. Try static/images / clean_path
    if not os.path.exists(file_path):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'images', clean_path)

    # 4. Try static/images / basename
    if not os.path.exists(file_path):
        file_path = os.path.join(settings.BASE_DIR, 'static', 'images', os.path.basename(clean_path))

    # 5. Fallback: Return standard sample image so frontend NEVER breaks
    if not os.path.exists(file_path):
        for sample in ['gotong_royong.jpg', 'hero_bg_kampung.jpg', 'foto_udara_kampung.jpg']:
            sample_path = os.path.join(settings.BASE_DIR, 'static', 'images', sample)
            if os.path.exists(sample_path):
                file_path = sample_path
                break

    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            c_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(content, content_type=c_type or 'image/jpeg')
            response['Cache-Control'] = 'public, max-age=86400'
            return response
        except Exception as e:
            print(f"[custom_media_serve Error]: {e}")

    raise Http404("File media tidak ditemukan.")


