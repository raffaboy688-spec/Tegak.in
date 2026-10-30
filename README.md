# Judul & Deskripsi

Nama produk digital yang kami buat adalah **Tegak.in**. Tegak.in adalah sebuah aplikasi deteksi cerdas yang dirancang khusus untuk mengatasi masalah sindrom *Tech Neck*, postur tubuh yang buruk, serta kelelahan saat menatap layar komputer dalam waktu lama. Banyak orang sering kali tidak sadar ketika tubuh mereka perlahan membungkuk atau mata mulai terpejam akibat hilangnya fokus dan rasa kantuk. Untuk menyelesaikan masalah tersebut, aplikasi ini memantau posisi mata dan postur tulang punggung pengguna secara *real-time*, lalu secara otomatis memberikan intervensi instan berupa alarm suara nyaring dan peringatan visual merah di layar agar pengguna segera kembali duduk tegak dan terbangun.

Produk ini secara khusus menargetkan para pekerja kantoran, pekerja jarak jauh (*remote workers*), mahasiswa, programmer, dan kreator konten yang rutinitasnya mengharuskan mereka duduk diam di depan laptop selama berjam-jam. Selain itu, Tegak.in juga sangat ideal bagi siapa saja yang ingin menerapkan teknik sesi kerja fokus terstruktur, seperti metode Pomodoro, karena sistemnya memungkinkan pengguna untuk mengatur durasi sesi produktivitas sambil secara aktif menjaga kesehatan tulang belakang dan tingkat konsentrasi mereka.

---

# Teknologi yang Digunakan

Dari segi teknologi, aplikasi Tegak.in dibangun sepenuhnya menggunakan bahasa pemrograman **Python**. Dalam proses pengembangannya, aplikasi ini sangat mengandalkan beberapa pustaka (*library*) utama, yaitu:

* **OpenCV (`cv2`)**: Untuk mengakses kamera dan memproses tangkapan layar secara *real-time*.
* **MediaPipe**: Pustaka buatan Google untuk menjalankan model kecerdasan buatan (AI) yang mendeteksi titik presisi pada wajah (*Face Mesh*) dan tulang tubuh (*Pose*).
* **NumPy**: Untuk komputasi matematis seperti perhitungan rasio bukaan mata (*Eye Aspect Ratio*).
* **Modul bawaan Python**: Termasuk `threading` agar kamera tidak *lag* saat alarm berbunyi, `time` untuk menghitung durasi sesi, dan `winsound` khusus untuk memicu suara nyaring di sistem operasi Windows.

Terkait platform publikasi, kode sumber ini tidak di-*hosting* di platform web, melainkan dirancang sebagai aplikasi desktop berbasis antarmuka baris perintah (CLI/Terminal). Program ini ditujukan untuk dieksekusi secara lokal langsung di sistem operasi perangkat pengguna, baik itu Windows, macOS, maupun Linux, yang sudah terinstal Python beserta pustaka-pustaka pendukungnya.

---

# Pemanfaatan AI

* **Alat AI yang digunakan:** Google Gemini
* **Contoh perintah (prompt) utama yang digunakan saat mengembangkan produk:**
  > *"Berikan saya ide tentang masalah sehari - hari yang sering terjadi di kalangan gen z yang dapat diselesaikan dengan sebuah pemrograman python cli yang berbasis ai dan berupa open CV"*
* **Penyesuaian/perbaikan mandiri yang dilakukan peserta terhadap saran kode dari AI:** 
  Melakukan perbaikan mengenai suara notifikasi pelanggaran pengguna yang sebelumnya volumenya kurang keras menjadi lebih keras, serta menambahkan fitur peringatan warna merah di layar kamera.

---

# Panduan Penggunaan

**1. Membuka Aplikasi dan Menu Utama**
Saat program pertama kali dijalankan melalui terminal atau *command prompt* (dengan perintah `python nama_file.py`), pengguna akan disambut oleh antarmuka teks (CLI) yang menampilkan menu utama. Pengguna cukup mengetikkan angka `1` hingga `5` dan menekan `Enter` untuk bernavigasi. Pilihan yang tersedia meliputi memulai sesi, membaca penjelasan program, melihat latar belakang masalah, membaca panduan *shortcut*, atau keluar dari aplikasi.

**2. Mengatur Sesi Fokus**
Jika pengguna memilih angka `1` (Mulai Sesi), program akan meminta beberapa pengaturan awal:
* **Durasi Sesi:** Pengguna dapat mengetikkan angka untuk menentukan berapa menit sesi akan berlangsung (misalnya `25` untuk 25 menit yang merupakan waktu *default* metode Pomodoro).
* **Tampilan Kamera:** Pengguna dapat memilih untuk menampilkan jendela kamera secara visual dengan mengetik `y` (ya) atau menyembunyikannya dengan mengetik `n` (tidak).
* **Ukuran Jendela:** Pengguna bisa menyesuaikan ukuran jendela kamera yang muncul di layar, yaitu `1` untuk ukuran normal, `2` untuk lebih kecil, atau `3` untuk ukuran yang lebih besar. Setelah itu, AI akan mulai aktif dalam 3 detik.

**3. Kontrol Saat Aplikasi Berjalan (Shortcut)**
Selama durasi sesi berjalan, pengguna dapat mengontrol aplikasi langsung melalui tombol pada *keyboard* (baik diketik di terminal maupun saat jendela kamera sedang aktif). Tombol-tombol tersebut adalah:
* `[ p ]` : Untuk melakukan *Pause* (menonaktifkan deteksi AI sementara waktu) atau *Resume* (melanjutkan deteksi).
* `[ h ]` : Untuk menyembunyikan atau memunculkan kembali jendela kamera tanpa menghentikan sesi.
* `[ + ]` atau `[ = ]` : Untuk memperbesar ukuran jendela kamera (*zoom in*).
* `[ - ]` : Untuk memperkecil ukuran jendela kamera (*zoom out*).
* `[ q ]` : Untuk menghentikan sesi secara paksa dan keluar dari program.

**4. Merespons Peringatan (Alarm)**
Selama sesi berjalan, pengguna cukup bekerja seperti biasa di depan layar. Jika AI mendeteksi kepala pengguna terlalu menunduk (membungkuk), program akan membunyikan alarm peringatan dan menampilkan teks kuning **"TEGAKKAN PUNGGUNG!"**. Namun, jika AI mendeteksi mata pengguna terpejam dalam waktu tertentu (mengantuk), alarm yang lebih nyaring akan berbunyi diiringi layar yang berkedip merah dengan peringatan **"BANGUN!!!"**. Pengguna hanya perlu memperbaiki postur duduk atau membuka mata untuk menghentikan alarm tersebut. Program akan otomatis berhenti dan kembali ke menu utama setelah durasi waktu sesi habis.

---

# Identitas Pengembang

* **Nama:** 
  1. M. Raihan Kautsar Adiraffa
  2. Kelvin Sutirta Augusto Wijaya
* **Kelas:** XI (11)
* **Jurusan:** Teknik Komputer dan Jaringan
* **Sekolah:** SMK Negeri 1 Turen
