from django.db import models

class AlbumGaleri(models.Model):
    """Album untuk mengelompokkan foto"""
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True)
    tanggal = models.DateField(auto_now_add=True)
    sampul = models.ImageField(upload_to='galeri/sampul/', blank=True, null=True, verbose_name='Foto Sampul Album')

    class Meta:
        ordering = ['-tanggal']
        verbose_name = 'Album Galeri'
        verbose_name_plural = 'Album Galeri'

    def __str__(self):
        return self.nama


class FotoGaleri(models.Model):
    """Model untuk foto dalam galeri"""
    album = models.ForeignKey(AlbumGaleri, on_delete=models.CASCADE, related_name='foto', blank=True, null=True)
    judul = models.CharField(max_length=200)
    keterangan = models.TextField(blank=True)
    foto = models.ImageField(upload_to='galeri/foto/')
    tanggal = models.DateTimeField(auto_now_add=True)
    unggulan = models.BooleanField(default=False, verbose_name='Tampil di Beranda')

    class Meta:
        ordering = ['-tanggal']
        verbose_name = 'Foto Galeri'
        verbose_name_plural = 'Foto Galeri'

    def __str__(self):
        return self.judul
