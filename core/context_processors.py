from core.models import ProfilKampung

def profil_context(request):
    """
    Context processor agar `profil` selalu tersedia secara global
    di semua halaman website (termasuk berita, galeri, dll).
    """
    try:
        profil = ProfilKampung.objects.first()
    except Exception:
        profil = None
    return {
        'profil': profil
    }
