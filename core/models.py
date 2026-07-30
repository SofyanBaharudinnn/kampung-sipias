from django.db import models

class ProfilKampung(models.Model):
    """Model untuk informasi profil kampung"""
    nama_kampung = models.CharField(max_length=100, default='Kampung Sipias')
    distrik = models.CharField(max_length=100, default='Elikobel')
    kabupaten = models.CharField(max_length=100, default='Merauke')
    provinsi = models.CharField(max_length=100, default='Papua Selatan')
    luas_wilayah = models.CharField(max_length=50, blank=True)
    jumlah_penduduk = models.PositiveIntegerField(default=0)
    jumlah_laki = models.PositiveIntegerField(default=0, verbose_name='Jumlah Laki-laki')
    jumlah_perempuan = models.PositiveIntegerField(default=0, verbose_name='Jumlah Perempuan')
    jumlah_kk = models.PositiveIntegerField(default=0, verbose_name='Jumlah KK')
    fasilitas_kesehatan = models.PositiveIntegerField(default=1, verbose_name='Fasilitas Kesehatan')
    fasilitas_pendidikan = models.PositiveIntegerField(default=1, verbose_name='Fasilitas Pendidikan')
    fasilitas_ibadah = models.PositiveIntegerField(default=1, verbose_name='Fasilitas Ibadah')
    fasilitas_umum = models.PositiveIntegerField(default=1, verbose_name='Fasilitas Umum')
    sambutan_kepala = models.TextField(blank=True, verbose_name='Sambutan Kepala Kampung')
    sejarah = models.TextField(blank=True)
    visi = models.TextField(blank=True)
    misi = models.TextField(blank=True)
    letak_geografis = models.TextField(blank=True)
    nama_kepala = models.CharField(max_length=100, blank=True, verbose_name='Nama Kepala Kampung')
    foto_kepala = models.ImageField(upload_to='profil/', blank=True, null=True, verbose_name='Foto Kepala Kampung')
    foto_kantor = models.ImageField(upload_to='profil/', blank=True, null=True, verbose_name='Foto Kantor Kampung')
    foto_fasilitas_kesehatan = models.ImageField(upload_to='fasilitas/', blank=True, null=True, verbose_name='Foto Fasilitas Kesehatan')
    foto_fasilitas_pendidikan = models.ImageField(upload_to='fasilitas/', blank=True, null=True, verbose_name='Foto Fasilitas Pendidikan')
    foto_fasilitas_ibadah = models.ImageField(upload_to='fasilitas/', blank=True, null=True, verbose_name='Foto Fasilitas Ibadah')
    foto_fasilitas_umum = models.ImageField(upload_to='fasilitas/', blank=True, null=True, verbose_name='Foto Fasilitas Umum')
    email = models.EmailField(blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)
    tahun_berdiri = models.CharField(max_length=10, blank=True)
    peta_iframe = models.TextField(blank=True, verbose_name='Embed Code / URL Peta Google Maps', help_text='Link embed Google Maps')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil Kampung'
        verbose_name_plural = 'Profil Kampung'

    def __str__(self):
        return self.nama_kampung


class FotoFasilitas(models.Model):
    """Model untuk banyak foto pada masing-masing fasilitas kampung"""
    KATEGORI_CHOICES = [
        ('kesehatan', 'Fasilitas Kesehatan'),
        ('pendidikan', 'Fasilitas Pendidikan'),
        ('ibadah', 'Fasilitas Ibadah'),
        ('umum', 'Fasilitas Umum'),
    ]
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES)
    judul = models.CharField(max_length=150, blank=True, help_text='Judul / nama fasilitas (opsional)')
    foto = models.ImageField(upload_to='fasilitas/')
    urutan = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['urutan', '-created_at']
        verbose_name = 'Foto Fasilitas'
        verbose_name_plural = 'Foto Fasilitas'

    def __str__(self):
        return f"{self.get_kategori_display()} - {self.judul or self.id}"


class StrukturOrganisasi(models.Model):
    """Model untuk struktur organisasi perangkat kampung"""
    JENIS_CHOICES = [
        ('pemerintah', 'Pemerintah Kampung'),
        ('bpk', 'Badan Permusyawaratan Kampung'),
    ]
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='pemerintah')
    foto = models.ImageField(upload_to='organisasi/', blank=True, null=True)
    urutan = models.PositiveSmallIntegerField(default=0)
    aktif = models.BooleanField(default=True)

    class Meta:
        ordering = ['urutan']
        verbose_name = 'Struktur Organisasi'
        verbose_name_plural = 'Struktur Organisasi'

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


class PesanKontak(models.Model):
    """Model untuk pesan dari form kontak"""
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    dibaca = models.BooleanField(default=False)
    tanggal = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-tanggal']
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'

    def __str__(self):
        return f"{self.nama} - {self.subjek}"
