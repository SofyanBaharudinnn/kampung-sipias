import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kampung_sipias.settings')
django.setup()

from core.models import ProfilKampung

sejarah_text = """Kampung Sipias adalah kampung bekas Unit Pemukiman Transmigrasi, UPT Bupul I yang berdiri pada tahun 1991, di bawah pimpinan KUPT Drs. Sutrisno dengan jumlah Penempatan 300 KK yang berasal dari Jawa Timur, Jawa Tengah, Jawa Barat, Madura, dan Trans Lokal. Bersamaan dengan penempatan terjadi kemarau panjang selama 9 bulan sehingga mengakibatkan rawan air.

Nama UPT Bupul I berubah nama dari UPT Bupul I menjadi Sipias pada tahun 1991 kata “Sipias” diambil dari bahasa Yeinan, yang artinya “Kemenangan”. Pada tahun 1996 terjadi perubahan jumlah kepala keluarga karena pada saat itu dibuka perusahaan Korindo sehingga warga banyak meninggalkan kampung dan menuju ke wilayah Distrik Jair. Pada tahun 1993 di adakan penunjukan kepala kampung secara aklamasi pertama dan yang terpilih adalah Supardi, namun jabatannya hanya berlangsung selama 1 tahun dan selanjutnya dijabat oleh Alimun pada tahun 1994 sampai tahun 1996 akhir jabatan.

Proses pembangunan Kampung Sipias dari awal tahun hingga ketahun selanjutnya secara perlahan, mata pencaharian penduduk sebagain besar adalah petani dengan mengolah tanah miliknya sendiri yang merupakan tanah jatah transmigrasi, lahan pekarangan 2.500 m², lahan usaha I 7.500 m² dan lahan usaha II 10.000 m². Jumlah kepala keluarga di Kampung Sipias saat ini berjumlah 142 kepala keluarga jumlah tersebut berubah dari 300 kepala keluarga karena tahun 1991 terjadi warga meninggalkan kampung karena tidak kerasan dan permasalahan ekonomi dan yang meninggalkan kampung pertama kali sebanyak 30 kepala keluarga.

Pada tahun 1996-1998 pembentukan panitia kepala kampung Sipias pertama divinitip dan terpilih oleh masyarakat, dan di jabat oleh Alimun, namun berlangsung hanya 2 tahun, Karena satu dan lain hal jabatan kepala kampung di lanjutkan oleh pejabat sementara (PJS) oleh Supri sampai tahun 2001. Karena masa jabatan sudah selesai diadakan pemilihan panitia kepala kampung yang kedua, dan terpilih oleh masyarakat adalah Santoso, dan menjabat dari tahun 2002 sampai tahun 2008 Karena masa jabatan belum habis dan di lanjutkan PJS kepala kampung yaitu Supardi pada tahun 2008 sampai 2009, karena masa jabatan habis, pada tahun 2009 dilakukan pembentukan panitia pemilihan kepala kampung kembali dan yang terpilih oleh masyarakat adalah Santoso. pada Tahun 2009 setelah pelantikan kepala kampung yang terpilih di adakan serah terima dari PJS kampung lama oleh Supardi kepada Kepala kampug yang terpilih oleh masyarakat yaitu Santoso dan di saksikan kepala Distrik, Kapolsek Bupul tokoh masyrakat dan tokoh Agama sampai tahun 2014, pada tanggal 26 Mei tahun 2015 diselenggarakan pemilihan kepala kampung Sipias untuk periode 2015-2021 dan yang terpilih adalah Pak Budiono. Kemudian pada tanggal 22 februari tahun 2022 diselenggarakan pemilihan kepala kampung Sipias untuk periode 2022-2028 dan yang terpilih adalah Pak Imam Sapi’i"""

profil, _ = ProfilKampung.objects.get_or_create(id=1)
profil.sejarah = sejarah_text
profil.tahun_berdiri = "1991"
profil.jumlah_kk = 142
profil.nama_kepala = "Pak Imam Sapi’i"
profil.save()

print("SUCCESSFULLY UPDATED SEJARAH KAMPUNG SIPIAS!")
