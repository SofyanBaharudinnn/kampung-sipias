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
        "Sitemap: https://kampungsipias.pythonanywhere.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """View untuk sitemap XML agar Google mudah mengindeks semua halaman"""
    from django.http import HttpResponse
    domain = "https://kampungsipias.pythonanywhere.com"
    urls = [
        "",
        "/profil/",
        "/sejarah/",
        "/visi-misi/",
        "/peta/",
        "/fasilitas/",
        "/pemerintahan/",
        "/kontak/",
        "/berita/",
        "/galeri/",
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for u in urls:
        xml.append(f'  <url><loc>{domain}{u}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    xml.append('</urlset>')
    return HttpResponse("\n".join(xml), content_type="application/xml")


def google_verification(request):
    """View verifikasi kepemilikan Google Search Console"""
    from django.http import HttpResponse
    return HttpResponse("google-site-verification: googled34dee6d910c2bc4.html", content_type="text/html")


def debug_media(request):
    """View debug untuk mengecek ketersediaan folder & file media di PythonAnywhere"""
    import os
    from django.conf import settings
    from django.http import HttpResponse

    media_dir = str(settings.MEDIA_ROOT)
    output = [f"<h3>MEDIA_ROOT: <code>{media_dir}</code></h3>", f"<p>Folder Exists: <b>{os.path.exists(media_dir)}</b></p>", "<hr><h4>DAFTAR FILE MEDIA SAAAT INI:</h4><ul>"]

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
from django.http import FileResponse, Http404

def custom_media_serve(request, path):
    """Serving media files reliably on PythonAnywhere with fallback to default sample image if missing"""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(file_path):
        # Fallback 1: check static/images for exact filename match
        fallback1 = os.path.join(settings.BASE_DIR, 'static', 'images', os.path.basename(path))
        if os.path.exists(fallback1):
            file_path = fallback1
        else:
            # Fallback 2: check if any default sample image exists
            hero_fallback = os.path.join(settings.BASE_DIR, 'static', 'images', 'gotong_royong.jpg')
            if not os.path.exists(hero_fallback):
                hero_fallback = os.path.join(settings.BASE_DIR, 'static', 'images', 'hero_bg_kampung.jpg')
            if os.path.exists(hero_fallback):
                file_path = hero_fallback
            else:
                raise Http404("File media tidak ditemukan.")

    content_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(open(file_path, 'rb'), content_type=content_type or 'image/jpeg')


