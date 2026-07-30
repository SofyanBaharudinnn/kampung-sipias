from django.shortcuts import render, get_object_or_404
from berita.models import Berita, KategoriBerita


def daftar_berita(request):
    """Halaman daftar semua berita"""
    berita_list = Berita.objects.filter(status='published')
    jenis = request.GET.get('jenis', '')
    if jenis:
        berita_list = berita_list.filter(jenis=jenis)
    kategori_list = KategoriBerita.objects.all()
    context = {
        'berita_list': berita_list,
        'kategori_list': kategori_list,
        'jenis_aktif': jenis,
        'page_title': 'Berita & Pengumuman',
    }
    return render(request, 'berita/daftar.html', context)


def detail_berita(request, slug):
    """Halaman detail satu berita"""
    berita = get_object_or_404(Berita, slug=slug, status='published')
    # Increment view counter
    berita.views += 1
    berita.save(update_fields=['views'])
    berita_terkait = Berita.objects.filter(
        status='published', jenis=berita.jenis
    ).exclude(id=berita.id)[:3]
    foto_tambahan = berita.foto_tambahan.all()
    context = {
        'berita': berita,
        'berita_terkait': berita_terkait,
        'foto_tambahan': foto_tambahan,
        'page_title': berita.judul,
    }
    return render(request, 'berita/detail.html', context)
