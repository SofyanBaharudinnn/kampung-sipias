from django.shortcuts import render
from .models import AlbumGaleri, FotoGaleri


def galeri_view(request):
    """Halaman galeri foto"""
    album_list = AlbumGaleri.objects.all()
    foto_list = FotoGaleri.objects.all()
    album_id = request.GET.get('album', '')
    if album_id:
        foto_list = foto_list.filter(album_id=album_id)
    context = {
        'album_list': album_list,
        'foto_list': foto_list,
        'album_aktif': album_id,
        'page_title': 'Galeri Foto',
    }
    return render(request, 'galeri/galeri.html', context)
