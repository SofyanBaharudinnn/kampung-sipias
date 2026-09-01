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


def breadcrumb_context(request):
    """
    Context processor yang otomatis menghasilkan data BreadcrumbList
    JSON-LD berdasarkan path halaman saat ini.
    Membantu Google menampilkan breadcrumb di hasil pencarian.
    """
    import json
    domain = "https://kampungsipias.pythonanywhere.com"
    path = request.path

    # Mapping path ke label yang SEO-friendly
    breadcrumb_map = {
        '/': ('Beranda', ''),
        '/profil/': ('Profil Kampung', '/profil/'),
        '/sejarah/': ('Sejarah Kampung', '/sejarah/'),
        '/visi-misi/': ('Visi & Misi', '/visi-misi/'),
        '/peta/': ('Peta Wilayah', '/peta/'),
        '/fasilitas/': ('Fasilitas Kampung', '/fasilitas/'),
        '/pemerintahan/': ('Struktur Organisasi', '/pemerintahan/'),
        '/kontak/': ('Kontak', '/kontak/'),
        '/berita/': ('Berita & Pengumuman', '/berita/'),
        '/galeri/': ('Galeri Foto', '/galeri/'),
    }

    breadcrumbs = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Beranda",
            "item": domain + "/"
        }
    ]

    # Halaman statis
    if path in breadcrumb_map and path != '/':
        label, url = breadcrumb_map[path]
        breadcrumbs.append({
            "@type": "ListItem",
            "position": 2,
            "name": label,
            "item": domain + url
        })
    # Halaman detail berita: /berita/slug/
    elif path.startswith('/berita/') and path != '/berita/':
        breadcrumbs.append({
            "@type": "ListItem",
            "position": 2,
            "name": "Berita & Pengumuman",
            "item": domain + "/berita/"
        })
        # Position 3 akan diisi oleh judul berita di template detail

    breadcrumb_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": breadcrumbs
    }, ensure_ascii=False)

    return {
        'breadcrumb_jsonld': breadcrumb_jsonld,
        'breadcrumb_items': breadcrumbs,
    }

