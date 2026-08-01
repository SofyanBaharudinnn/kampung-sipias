"""
Admin panel views untuk mengelola konten website Kampung Sipias
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.text import slugify
from django.utils import timezone
from .models import ProfilKampung, StrukturOrganisasi, PesanKontak, FotoFasilitas
from berita.models import Berita, KategoriBerita, FotoBerita
from galeri.models import AlbumGaleri, FotoGaleri
import uuid


def get_profil():
    profil, _ = ProfilKampung.objects.get_or_create(id=1)
    return profil


# ===================== AUTH =====================

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_panel:admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_panel:admin_dashboard')
        else:
            messages.error(request, 'Username atau password salah, atau akun tidak memiliki akses admin.')
    return render(request, 'admin_panel/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_panel:admin_login')


# ===================== DASHBOARD =====================

@login_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    context = {
        'total_berita': Berita.objects.filter(status='published').count(),
        'total_draft': Berita.objects.filter(status='draft').count(),
        'total_foto': FotoGaleri.objects.count(),
        'total_pesan': PesanKontak.objects.filter(dibaca=False).count(),
        'berita_terbaru': Berita.objects.order_by('-tanggal_publish')[:5],
        'pesan_terbaru': PesanKontak.objects.filter(dibaca=False)[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)


# ===================== BERITA =====================

@login_required(login_url='/admin-panel/login/')
def admin_berita_list(request):
    berita_list = Berita.objects.all().order_by('-tanggal_publish')
    return render(request, 'admin_panel/berita_list.html', {'berita_list': berita_list})


@login_required(login_url='/admin-panel/login/')
def admin_berita_tambah(request):
    kategori_list = KategoriBerita.objects.all()
    if request.method == 'POST':
        judul = request.POST.get('judul', '').strip()
        konten = request.POST.get('konten', '').strip()
        ringkasan = request.POST.get('ringkasan', '').strip()
        jenis = request.POST.get('jenis', 'berita')
        status = request.POST.get('status', 'draft')
        penulis = request.POST.get('penulis', 'Admin Kampung Sipias')
        unggulan = True
        gambar = request.FILES.get('gambar')

        if judul and konten:
            # Generate unique slug
            base_slug = slugify(judul)
            slug = base_slug
            counter = 1
            while Berita.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            berita = Berita.objects.create(
                judul=judul, slug=slug, konten=konten,
                ringkasan=ringkasan, jenis=jenis, status=status,
                penulis=penulis, unggulan=unggulan
            )
            if gambar:
                berita.gambar = gambar
                berita.save()
            # Simpan foto-foto tambahan
            for f in request.FILES.getlist('foto_tambahan'):
                FotoBerita.objects.create(berita=berita, foto=f)
            messages.success(request, f'Berita "{judul}" berhasil ditambahkan!')
            return redirect('admin_panel:admin_berita_list')
        else:
            messages.error(request, 'Judul dan konten berita wajib diisi.')

    return render(request, 'admin_panel/berita_form.html', {
        'kategori_list': kategori_list,
        'action': 'Tambah',
    })


@login_required(login_url='/admin-panel/login/')
def admin_berita_edit(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    kategori_list = KategoriBerita.objects.all()
    if request.method == 'POST':
        berita.judul = request.POST.get('judul', berita.judul).strip()
        berita.konten = request.POST.get('konten', berita.konten)
        berita.ringkasan = request.POST.get('ringkasan', '').strip()
        berita.jenis = request.POST.get('jenis', berita.jenis)
        berita.status = request.POST.get('status', berita.status)
        berita.penulis = request.POST.get('penulis', berita.penulis)
        berita.unggulan = True
        gambar = request.FILES.get('gambar')
        if gambar:
            berita.gambar = gambar
        berita.save()
        # Simpan foto-foto tambahan baru
        for f in request.FILES.getlist('foto_tambahan'):
            FotoBerita.objects.create(berita=berita, foto=f)
        messages.success(request, f'Berita "{berita.judul}" berhasil diperbarui!')
        return redirect('admin_panel:admin_berita_list')

    foto_tambahan_list = berita.foto_tambahan.all()
    return render(request, 'admin_panel/berita_form.html', {
        'berita': berita,
        'kategori_list': kategori_list,
        'action': 'Edit',
        'foto_tambahan_list': foto_tambahan_list,
    })


@login_required(login_url='/admin-panel/login/')
def admin_berita_hapus(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        judul = berita.judul
        berita.delete()
        messages.success(request, f'Berita "{judul}" berhasil dihapus.')
        return redirect('admin_panel:admin_berita_list')
    return render(request, 'admin_panel/konfirmasi_hapus.html', {'objek': berita, 'tipe': 'berita'})


@login_required(login_url='/admin-panel/login/')
def admin_berita_foto_hapus(request, foto_pk):
    """Hapus satu foto tambahan dari artikel berita"""
    foto = get_object_or_404(FotoBerita, pk=foto_pk)
    berita_pk = foto.berita_id
    if request.method == 'POST':
        foto.foto.delete(save=False)
        foto.delete()
        messages.success(request, 'Foto berhasil dihapus.')
    return redirect('admin_panel:admin_berita_edit', pk=berita_pk)


# ===================== GALERI =====================

import os
import re
import time
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile


def prepare_uploaded_image(image_file):
    """
    Memproses dan mengkonversi file gambar yang diupload:
    1. Sanitasi nama file (hapus spasi, &, simbol khusus).
    2. Konversi format HEIC (iPhone) / RGBA / PNG ke JPEG standar RGB.
    3. Auto-rotate EXIF HP.
    """
    if not image_file or not hasattr(image_file, 'name'):
        return image_file, None

    filename = os.path.basename(image_file.name)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    clean_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    clean_name = re.sub(r'_+', '_', clean_name).strip('_')
    if not clean_name:
        clean_name = "foto"

    unique_filename = f"{clean_name[:35]}_{int(time.time())}_{uuid.uuid4().hex[:4]}.jpg"

    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
    except Exception:
        pass

    try:
        if hasattr(image_file, 'seek'):
            image_file.seek(0)

        img = None
        is_heic = ext in ['.heic', '.heif']

        if is_heic:
            try:
                import pillow_heif
                image_file.seek(0)
                heif_obj = pillow_heif.open_heif(image_file.read())
                img = Image.frombytes(
                    heif_obj.mode,
                    heif_obj.size,
                    heif_obj.data,
                    "raw",
                )
            except Exception as heic_err:
                print(f"[HEIC Open Error]: {heic_err}")
                if hasattr(image_file, 'seek'):
                    image_file.seek(0)

        if img is None:
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            img = Image.open(image_file)

        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass

        if img.mode in ('RGBA', 'LA', 'PA') or (img.mode == 'P' and 'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            bg = Image.new('RGB', img.size, (255, 255, 255))
            bg.paste(img.convert('RGB'), mask=alpha)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=88, optimize=True)
        buffer.seek(0)

        return ContentFile(buffer.getvalue(), name=unique_filename), None

    except Exception as e:
        error_msg = f"File foto '{filename}' tidak dapat diproses ({e}). Harap upload foto berformat JPG atau PNG biasa."
        return None, error_msg


@login_required(login_url='/admin-panel/login/')
def admin_galeri_list(request):
    foto_list = FotoGaleri.objects.all().order_by('-tanggal')
    album_list = AlbumGaleri.objects.all()
    return render(request, 'admin_panel/galeri_list.html', {
        'foto_list': foto_list,
        'album_list': album_list,
    })


@login_required(login_url='/admin-panel/login/')
def admin_galeri_upload(request):
    album_list = AlbumGaleri.objects.all()
    if request.method == 'POST':
        judul = request.POST.get('judul', '').strip()
        keterangan = request.POST.get('keterangan', '').strip()
        album_id = request.POST.get('album', '')
        unggulan = request.POST.get('unggulan') == 'on'
        raw_foto = request.FILES.get('foto')

        if judul and raw_foto:
            processed_foto, err_msg = prepare_uploaded_image(raw_foto)
            if err_msg:
                messages.error(request, err_msg)
                return render(request, 'admin_panel/galeri_upload.html', {'album_list': album_list})

            foto_obj = FotoGaleri.objects.create(
                judul=judul, keterangan=keterangan,
                foto=processed_foto, unggulan=unggulan
            )
            if album_id:
                foto_obj.album_id = int(album_id)
                foto_obj.save()
            messages.success(request, f'Foto "{judul}" berhasil diupload!')
            return redirect('admin_panel:admin_galeri_list')
        else:
            messages.error(request, 'Judul dan file foto wajib diisi.')

    return render(request, 'admin_panel/galeri_upload.html', {'album_list': album_list})


@login_required(login_url='/admin-panel/login/')
def admin_galeri_edit(request, pk):
    foto_obj = get_object_or_404(FotoGaleri, pk=pk)
    album_list = AlbumGaleri.objects.all()
    if request.method == 'POST':
        judul = request.POST.get('judul', '').strip()
        keterangan = request.POST.get('keterangan', '').strip()
        album_id = request.POST.get('album', '')
        unggulan = request.POST.get('unggulan') == 'on'
        raw_foto = request.FILES.get('foto')

        if judul:
            foto_obj.judul = judul
            foto_obj.keterangan = keterangan
            foto_obj.unggulan = unggulan
            if album_id:
                foto_obj.album_id = int(album_id)
            else:
                foto_obj.album = None

            if raw_foto:
                processed_foto, err_msg = prepare_uploaded_image(raw_foto)
                if err_msg:
                    messages.error(request, err_msg)
                    return render(request, 'admin_panel/galeri_edit.html', {'foto': foto_obj, 'album_list': album_list})
                foto_obj.foto = processed_foto

            foto_obj.save()
            messages.success(request, f'Foto "{judul}" berhasil diperbarui!')
            return redirect('admin_panel:admin_galeri_list')
        else:
            messages.error(request, 'Judul foto wajib diisi.')

    return render(request, 'admin_panel/galeri_edit.html', {
        'foto': foto_obj,
        'album_list': album_list,
    })


@login_required(login_url='/admin-panel/login/')
def admin_galeri_hapus(request, pk):
    foto = get_object_or_404(FotoGaleri, pk=pk)
    if request.method == 'POST':
        judul = foto.judul
        foto.delete()
        messages.success(request, f'Foto "{judul}" berhasil dihapus.')
        return redirect('admin_panel:admin_galeri_list')
    return render(request, 'admin_panel/konfirmasi_hapus.html', {'objek': foto, 'tipe': 'foto'})


# ===================== PESAN KONTAK =====================

@login_required(login_url='/admin-panel/login/')
def admin_pesan_list(request):
    pesan_list = PesanKontak.objects.all().order_by('-tanggal')
    return render(request, 'admin_panel/pesan_list.html', {'pesan_list': pesan_list})


@login_required(login_url='/admin-panel/login/')
def admin_pesan_detail(request, pk):
    pesan = get_object_or_404(PesanKontak, pk=pk)
    pesan.dibaca = True
    pesan.save()
    return render(request, 'admin_panel/pesan_detail.html', {'pesan': pesan})


# ===================== PROFIL KAMPUNG =====================

@login_required(login_url='/admin-panel/login/')
def admin_profil_edit(request):
    profil = get_profil()
    if request.method == 'POST':
        profil.nama_kepala = request.POST.get('nama_kepala', '').strip()
        profil.sambutan_kepala = request.POST.get('sambutan_kepala', '').strip()
        profil.sejarah = request.POST.get('sejarah', '').strip()
        profil.visi = request.POST.get('visi', '').strip()
        profil.misi = request.POST.get('misi', '').strip()
        profil.letak_geografis = request.POST.get('letak_geografis', '').strip()
        profil.jumlah_penduduk = int(request.POST.get('jumlah_penduduk', 0) or 0)
        profil.jumlah_kk = int(request.POST.get('jumlah_kk', 0) or 0)
        profil.luas_wilayah = request.POST.get('luas_wilayah', '').strip()
        profil.email = request.POST.get('email', '').strip()
        profil.telepon = request.POST.get('telepon', '').strip()
        profil.alamat = request.POST.get('alamat', '').strip()
        profil.tahun_berdiri = request.POST.get('tahun_berdiri', '').strip()

        # Delete or Update Foto Kepala
        if request.POST.get('hapus_foto_kepala') == '1':
            if profil.foto_kepala:
                profil.foto_kepala.delete(save=False)
                profil.foto_kepala = None
        elif request.FILES.get('foto_kepala'):
            profil.foto_kepala = request.FILES.get('foto_kepala')

        # Delete or Update Foto Kantor
        if request.POST.get('hapus_foto_kantor') == '1':
            if profil.foto_kantor:
                profil.foto_kantor.delete(save=False)
                profil.foto_kantor = None
        elif request.FILES.get('foto_kantor'):
            profil.foto_kantor = request.FILES.get('foto_kantor')

        # Delete or Update Foto Fasilitas
        if request.POST.get('hapus_foto_fasilitas_kesehatan') == '1':
            if profil.foto_fasilitas_kesehatan:
                profil.foto_fasilitas_kesehatan.delete(save=False)
                profil.foto_fasilitas_kesehatan = None
        elif request.FILES.get('foto_fasilitas_kesehatan'):
            profil.foto_fasilitas_kesehatan = request.FILES.get('foto_fasilitas_kesehatan')

        if request.POST.get('hapus_foto_fasilitas_pendidikan') == '1':
            if profil.foto_fasilitas_pendidikan:
                profil.foto_fasilitas_pendidikan.delete(save=False)
                profil.foto_fasilitas_pendidikan = None
        elif request.FILES.get('foto_fasilitas_pendidikan'):
            profil.foto_fasilitas_pendidikan = request.FILES.get('foto_fasilitas_pendidikan')

        if request.POST.get('hapus_foto_fasilitas_ibadah') == '1':
            if profil.foto_fasilitas_ibadah:
                profil.foto_fasilitas_ibadah.delete(save=False)
                profil.foto_fasilitas_ibadah = None
        elif request.FILES.get('foto_fasilitas_ibadah'):
            profil.foto_fasilitas_ibadah = request.FILES.get('foto_fasilitas_ibadah')

        if request.POST.get('hapus_foto_fasilitas_umum') == '1':
            if profil.foto_fasilitas_umum:
                profil.foto_fasilitas_umum.delete(save=False)
                profil.foto_fasilitas_umum = None
        elif request.FILES.get('foto_fasilitas_umum'):
            profil.foto_fasilitas_umum = request.FILES.get('foto_fasilitas_umum')

        profil.save()
        messages.success(request, 'Profil kampung berhasil diperbarui!')
        return redirect('admin_panel:admin_profil_edit')

    return render(request, 'admin_panel/profil_edit.html', {'profil': profil})


@login_required(login_url='/admin-panel/login/')
def admin_profil_hapus_foto(request, field_name):
    profil = get_profil()
    allowed_fields = [
        'foto_kepala', 'foto_kantor', 
        'foto_fasilitas_kesehatan', 'foto_fasilitas_pendidikan', 
        'foto_fasilitas_ibadah', 'foto_fasilitas_umum'
    ]
    if field_name in allowed_fields:
        foto_field = getattr(profil, field_name, None)
        if foto_field:
            foto_field.delete(save=False)
            setattr(profil, field_name, None)
            profil.save()
            messages.success(request, 'Foto berhasil dihapus secara langsung!')
    return redirect('admin_panel:admin_profil_edit')


# ===================== FOTO FASILITAS =====================

@login_required(login_url='/admin-panel/login/')
def admin_fasilitas_list(request):
    foto_list = FotoFasilitas.objects.all()
    return render(request, 'admin_panel/fasilitas_list.html', {'foto_list': foto_list})


@login_required(login_url='/admin-panel/login/')
def admin_fasilitas_upload(request):
    if request.method == 'POST':
        kategori = request.POST.get('kategori')
        judul = request.POST.get('judul', '').strip()
        fotos = request.FILES.getlist('foto')

        if kategori and fotos:
            for f in fotos:
                FotoFasilitas.objects.create(
                    kategori=kategori,
                    judul=judul,
                    foto=f
                )
            messages.success(request, f'{len(fotos)} Foto fasilitas berhasil diunggah!')
            return redirect('admin_panel:admin_fasilitas_list')
        else:
            messages.error(request, 'Kategori dan file foto wajib dipilih.')

    return render(request, 'admin_panel/fasilitas_upload.html')


@login_required(login_url='/admin-panel/login/')
def admin_fasilitas_edit(request, pk):
    foto = get_object_or_404(FotoFasilitas, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action', 'update_info')

        if action == 'tambah_foto':
            # Tambah foto baru ke kategori yang sama (TIDAK menghapus foto lama)
            judul_baru = request.POST.get('judul_baru', '').strip()
            kategori = request.POST.get('kategori', foto.kategori)
            foto_baru = request.FILES.get('foto_baru')
            if foto_baru:
                FotoFasilitas.objects.create(
                    kategori=kategori,
                    judul=judul_baru,
                    foto=foto_baru
                )
                messages.success(request, 'Foto baru berhasil ditambahkan! Foto sebelumnya tetap tersimpan.')
            else:
                messages.error(request, 'Pilih file foto terlebih dahulu.')
        else:
            # Update info: judul & kategori saja (foto lama tetap)
            judul = request.POST.get('judul', '').strip()
            kategori = request.POST.get('kategori', '').strip()
            if judul:
                foto.judul = judul
            if kategori:
                foto.kategori = kategori
            foto.save()
            messages.success(request, 'Info foto berhasil diperbarui!')

        return redirect('admin_panel:admin_fasilitas_list')

    return render(request, 'admin_panel/fasilitas_edit.html', {
        'foto': foto,
        'kategori_choices': FotoFasilitas.KATEGORI_CHOICES
    })


@login_required(login_url='/admin-panel/login/')
def admin_fasilitas_hapus(request, pk):
    foto = get_object_or_404(FotoFasilitas, pk=pk)
    if request.method == 'POST':
        foto.delete()
        messages.success(request, 'Foto fasilitas berhasil dihapus.')
        return redirect('admin_panel:admin_fasilitas_list')
    return render(request, 'admin_panel/konfirmasi_hapus.html', {'objek': foto, 'tipe': 'foto fasilitas'})

