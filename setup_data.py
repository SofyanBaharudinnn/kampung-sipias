"""
Script untuk membuat superuser dan data sample awal untuk Website Kampung Sipias.
Jalankan: python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import ProfilKampung, StrukturOrganisasi
from berita.models import Berita, KategoriBerita

print("🌿 Setup Website Kampung Sipias...")

# ===== SUPERUSER =====
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@kampungsipias.id',
        password='sipias2024',
        first_name='Admin',
        last_name='Kampung Sipias'
    )
    print("✅ Superuser dibuat: username='admin', password='sipias2024'")
else:
    print("ℹ️  Superuser 'admin' sudah ada.")

# ===== PROFIL KAMPUNG =====
profil, created = ProfilKampung.objects.get_or_create(id=1)
if created or not profil.sejarah:
    profil.nama_kampung = 'Kampung Sipias'
    profil.distrik = 'Elikobel'
    profil.kabupaten = 'Merauke'
    profil.provinsi = 'Papua Selatan'
    profil.nama_kepala = 'Kepala Kampung Sipias'
    profil.jumlah_penduduk = 450
    profil.jumlah_kk = 120
    profil.luas_wilayah = '85 km²'
    profil.tahun_berdiri = '1975'
    profil.telepon = '+62 xxx-xxxx-xxxx'
    profil.email = 'kampungsipias@gmail.com'
    profil.alamat = 'Kampung Sipias, Distrik Elikobel, Kabupaten Merauke, Papua Selatan'
    profil.sambutan_kepala = (
        "Assalamu'alaikum Warahmatullahi Wabarakatuh dan Salam Sejahtera untuk kita semua. "
        "Selamat datang di website resmi Kampung Sipias. Kami berkomitmen untuk terus meningkatkan "
        "pelayanan kepada masyarakat dan membangun kampung kita bersama menuju yang lebih baik. "
        "Website ini hadir sebagai jembatan informasi antara pemerintah kampung dengan seluruh masyarakat "
        "Kampung Sipias dan pihak-pihak yang ingin mengenal lebih jauh kampung kami. "
        "Semoga dengan adanya website ini, transparansi dan keterbukaan informasi dapat terus kami jaga "
        "demi kemajuan Kampung Sipias yang kita cintai bersama."
    )
    profil.sejarah = (
        "Kampung Sipias merupakan salah satu kampung yang berada di Distrik Elikobel, Kabupaten Merauke, "
        "Provinsi Papua Selatan. Kampung ini telah berdiri sejak lama dan menjadi bagian tak terpisahkan "
        "dari sejarah dan budaya masyarakat di wilayah Merauke bagian selatan.\n\n"
        "Masyarakat Kampung Sipias hidup dalam keharmonisan dengan mengedepankan nilai-nilai kearifan lokal "
        "yang telah diwariskan secara turun-temurun. Kehidupan masyarakat yang bergantung pada alam sekitar "
        "menjadikan kampung ini memiliki lingkungan yang masih asri dan terjaga kelestariannya.\n\n"
        "Seiring berjalannya waktu, Kampung Sipias terus berkembang dengan berbagai program pembangunan "
        "yang bertujuan untuk meningkatkan kesejahteraan masyarakat dan kualitas hidup warga kampung."
    )
    profil.visi = (
        "Terwujudnya Kampung Sipias yang Mandiri, Sejahtera, dan Berbudaya berdasarkan nilai-nilai "
        "kearifan lokal dan pembangunan yang berkelanjutan."
    )
    profil.misi = (
        "1. Meningkatkan kualitas pelayanan pemerintahan yang transparan dan akuntabel.\n"
        "2. Mengembangkan potensi sumber daya alam secara berkelanjutan.\n"
        "3. Meningkatkan kesejahteraan masyarakat melalui pemberdayaan ekonomi lokal.\n"
        "4. Melestarikan budaya dan kearifan lokal masyarakat Kampung Sipias.\n"
        "5. Meningkatkan akses pendidikan dan kesehatan bagi seluruh warga kampung."
    )
    profil.letak_geografis = (
        "Kampung Sipias secara administratif berada di bawah Distrik Elikobel, Kabupaten Merauke, "
        "Provinsi Papua Selatan. Kampung ini terletak di wilayah selatan Papua yang berbatasan langsung "
        "dengan wilayah-wilayah kampung lainnya di Distrik Elikobel.\n\n"
        "Wilayah Kampung Sipias sebagian besar terdiri dari lahan pertanian, hutan, dan kawasan yang "
        "masih terjaga kealamiannya. Kondisi geografis ini menjadikan Kampung Sipias memiliki potensi "
        "sumber daya alam yang cukup besar untuk dikembangkan bagi kesejahteraan masyarakat."
    )
    profil.save()
    print("✅ Profil kampung berhasil dibuat/diperbarui.")

# ===== STRUKTUR ORGANISASI =====
if StrukturOrganisasi.objects.count() == 0:
    struktur_data = [
        {'nama': profil.nama_kepala, 'jabatan': 'Kepala Kampung', 'jenis': 'pemerintah', 'urutan': 1},
        {'nama': 'Sekretaris Kampung', 'jabatan': 'Sekretaris Kampung', 'jenis': 'pemerintah', 'urutan': 2},
        {'nama': 'Bendahara Kampung', 'jabatan': 'Bendahara', 'jenis': 'pemerintah', 'urutan': 3},
        {'nama': 'Kepala Urusan Pemerintahan', 'jabatan': 'Kaur Pemerintahan', 'jenis': 'pemerintah', 'urutan': 4},
        {'nama': 'Kepala Urusan Pembangunan', 'jabatan': 'Kaur Pembangunan', 'jenis': 'pemerintah', 'urutan': 5},
        {'nama': 'Ketua BPK', 'jabatan': 'Ketua BPK', 'jenis': 'bpk', 'urutan': 1},
        {'nama': 'Wakil Ketua BPK', 'jabatan': 'Wakil Ketua BPK', 'jenis': 'bpk', 'urutan': 2},
    ]
    for data in struktur_data:
        StrukturOrganisasi.objects.create(**data)
    print("✅ Struktur organisasi berhasil dibuat.")

# ===== KATEGORI BERITA =====
if KategoriBerita.objects.count() == 0:
    kategori_data = [
        {'nama': 'Pembangunan', 'slug': 'pembangunan'},
        {'nama': 'Sosial Budaya', 'slug': 'sosial-budaya'},
        {'nama': 'Kesehatan', 'slug': 'kesehatan'},
        {'nama': 'Pendidikan', 'slug': 'pendidikan'},
    ]
    for data in kategori_data:
        KategoriBerita.objects.create(**data)
    print("✅ Kategori berita berhasil dibuat.")

# ===== BERITA SAMPLE =====
if Berita.objects.count() == 0:
    berita_data = [
        {
            'judul': 'Selamat Datang di Website Resmi Kampung Sipias',
            'slug': 'selamat-datang-website-kampung-sipias',
            'jenis': 'pengumuman',
            'status': 'published',
            'ringkasan': 'Website resmi Kampung Sipias kini telah diluncurkan untuk memberikan informasi terkini kepada masyarakat.',
            'konten': '<p>Dengan penuh rasa syukur, kami mengumumkan bahwa <strong>Website Resmi Kampung Sipias</strong> telah resmi diluncurkan.</p><p>Melalui website ini, kami berkomitmen untuk menyampaikan informasi terkini mengenai kegiatan dan perkembangan Kampung Sipias kepada seluruh masyarakat.</p><p>Semoga website ini bermanfaat bagi semua pihak. Terima kasih atas perhatian dan dukungannya.</p>',
            'penulis': 'Admin Kampung Sipias',
            'unggulan': True,
        },
        {
            'judul': 'Kegiatan Gotong Royong Bersih Kampung',
            'slug': 'kegiatan-gotong-royong-bersih-kampung',
            'jenis': 'kegiatan',
            'status': 'published',
            'ringkasan': 'Masyarakat Kampung Sipias bersama-sama melaksanakan kegiatan gotong royong membersihkan lingkungan kampung.',
            'konten': '<p>Dalam rangka menjaga kebersihan dan keindahan lingkungan, masyarakat <strong>Kampung Sipias</strong> bersama perangkat kampung melaksanakan kegiatan gotong royong membersihkan kampung.</p><p>Kegiatan ini diikuti oleh seluruh warga kampung dari berbagai kalangan usia. Semangat kebersamaan dan kekeluargaan sangat terasa dalam kegiatan ini.</p><p>Gotong royong merupakan tradisi leluhur yang harus terus kita jaga dan lestarikan sebagai cerminan nilai-nilai kebersamaan masyarakat kampung.</p>',
            'penulis': 'Admin Kampung Sipias',
            'unggulan': False,
        },
        {
            'judul': 'Pengumuman Jadwal Pelayanan Administrasi Kampung',
            'slug': 'pengumuman-jadwal-pelayanan-administrasi',
            'jenis': 'pengumuman',
            'status': 'published',
            'ringkasan': 'Informasi jadwal pelayanan administrasi kantor Kampung Sipias untuk keperluan masyarakat.',
            'konten': '<p>Diberitahukan kepada seluruh masyarakat Kampung Sipias bahwa jadwal pelayanan administrasi kampung adalah sebagai berikut:</p><ul><li><strong>Senin – Jumat:</strong> Pukul 08.00 – 16.00 WIT</li><li><strong>Sabtu – Minggu:</strong> Libur</li></ul><p>Pelayanan meliputi:</p><ul><li>Surat Keterangan Domisili</li><li>Surat Keterangan Tidak Mampu</li><li>Surat Pengantar Berbagai Keperluan</li><li>Administrasi Kependudukan</li></ul><p>Untuk informasi lebih lanjut, silakan hubungi kantor kampung pada jam pelayanan.</p>',
            'penulis': 'Admin Kampung Sipias',
            'unggulan': True,
        },
    ]
    for data in berita_data:
        Berita.objects.create(**data)
    print("✅ Berita sample berhasil dibuat (3 berita).")

print("\n" + "="*50)
print("🎉 SETUP SELESAI! Website Kampung Sipias siap digunakan.")
print("="*50)
print("\n📌 INFORMASI LOGIN:")
print("   URL Admin Panel : http://127.0.0.1:8000/admin-panel/")
print("   Username        : admin")
print("   Password        : sipias2024")
print("\n📌 UNTUK MENJALANKAN SERVER:")
print("   .\\venv\\Scripts\\python manage.py runserver")
print("\n🌐 Buka browser: http://127.0.0.1:8000")
print("="*50)
