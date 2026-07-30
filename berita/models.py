from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class KategoriBerita(models.Model):
    """Kategori untuk berita"""
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Kategori Berita'
        verbose_name_plural = 'Kategori Berita'

    def __str__(self):
        return self.nama


class Berita(models.Model):
    """Model untuk berita dan pengumuman kampung"""
    JENIS_CHOICES = [
        ('berita', 'Berita'),
        ('pengumuman', 'Pengumuman'),
        ('kegiatan', 'Kegiatan'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Dipublikasikan'),
    ]

    judul = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, max_length=300)
    kategori = models.ForeignKey(KategoriBerita, on_delete=models.SET_NULL, null=True, blank=True)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='berita')
    ringkasan = models.TextField(max_length=500, blank=True, verbose_name='Ringkasan / Excerpt')
    konten = CKEditor5Field(verbose_name='Konten Berita', config_name='extends')
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True, verbose_name='Gambar Utama')
    penulis = models.CharField(max_length=100, default='Admin Kampung Sipias')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    tanggal_publish = models.DateTimeField(auto_now_add=True)
    tanggal_update = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    unggulan = models.BooleanField(default=True, verbose_name='Jadikan Unggulan')

    class Meta:
        ordering = ['-tanggal_publish']
        verbose_name = 'Berita'
        verbose_name_plural = 'Berita & Pengumuman'

    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('berita:detail', kwargs={'slug': self.slug})


class FotoBerita(models.Model):
    """Model untuk foto tambahan (galeri) pada setiap artikel berita/kegiatan/pengumuman"""
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='foto_tambahan')
    foto = models.ImageField(upload_to='berita/gallery/')
    keterangan = models.CharField(max_length=200, blank=True, verbose_name='Keterangan Foto')
    urutan = models.PositiveSmallIntegerField(default=0, verbose_name='Urutan Tampil')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['urutan', 'id']
        verbose_name = 'Foto Berita'
        verbose_name_plural = 'Foto Berita'

    def __str__(self):
        return f"Foto #{self.id} — {self.berita.judul[:40]}"
