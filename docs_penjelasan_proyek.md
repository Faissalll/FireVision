# FireVision: Dokumentasi Proyek & Strategi Testing

## 1. Apa itu FireVision?
**FireVision** adalah sistem deteksi dini kebakaran berbasis **Artificial Intelligence (AI)** dan **Computer Vision**. Aplikasi ini mengubah kamera pengawas (CCTV/Webcam/HP) biasa menjadi alat pendeteksi cerdas yang dapat mengenali api secara real-time.

**Fitur Utama:**
*   **Real-time Detection**: Menggunakan model Deep Learning (YOLOv8) untuk mendeteksi api dalam hitungan milidetik.
*   **Multi-Camera Support**: Memantau hingga 4 kamera sekaligus dalam satu dashboard.
*   **Smart Alerts (Notifikasi Cerdas)**: 
    *   **Telegram**: Mengirim foto kejadian + Nama Kamera (misal: "Kamera Gudang").
    *   **SMS/WhatsApp**: Notifikasi darurat langsung ke HP (via Fonnte API).
    *   **Browser/System Notification**: Popup peringatan di Windows/HP meskipun browser sedang diminimize.
    *   **Audio Alarm**: Suara sirene otomatis berbunyi saat api terdeteksi.
*   **SaaS Payment Gateway**: Sistem berlangganan dummy/simulasi (Siap integrasi Midtrans).

## 2. Mengapa Membuat Aplikasi Ini? (Latar Belakang)
Masalah utama dari detektor asap tradisional (Smoke Detector) adalah:
1.  **Lambat**: Harus menunggu asap mengepul tebal hingga mencapai langit-langit.
2.  **Lokal**: Alarm berbunyi di lokasi, tapi jika gedung kosong, tidak ada yang tahu.
3.  **Tidak Visual**: Kita tidak tahu seberapa besar apinya tanpa datang ke lokasi.

**Solusi FireVision:**
*   Mendeteksi **cahaya/bentuk api** visual (lebih cepat dari asap).
*   Memberikan **bukti visual** langsung ke HP pemilik.
*   Bisa dipasang di area terbuka (outdoor) di mana smoke detector tidak berguna.

## 3. Demo Aplikasi
Langkah-langkah untuk mendemokan proyek ini:

1.  **Halaman Utama (Landing Page)**: Tunjukkan desain modern dan penjelasan fitur.
2.  **Login/Register**: Masuk sebagai user `asep1`.
3.  **Menu Demo (Deteksi)**:
    *   Buka halaman Demo atau Multi-Camera.
    *   Nyalakan kamera (Webcam atau IP Cam).
    *   Nyalakan korek api atau tunjukkan video api di HP ke arah kamera.
    *   **Hasil Visual**: Kotak merah muncul di sekeliling api.
    *   **Hasil Audio**: Suara sirene berbunyi kencang.
    *   **Hasil Sistem**: Notifikasi Windows muncul di pojok kanan bawah ("🔥 PERINGATAN API!").
4.  **Cek HP (Notifikasi)**: 
    *   Buka Telegram: Pesan masuk "🔥 FireVision Alert (Kamera 1) — Api terdeteksi!" beserta fotonya.
5.  **Upgrade Plan**: Tunjukkan halaman Pricing, klik langganan, dan muncul popup pembayaran simulasi.

## 4. Alur Proses Kode (Flowchart Sederhana)

### A. Frontend (Vue.js)
1.  **Capture**: Mengambil gambar dari webcam user.
2.  **Send**: Mengirim gambar ke Backend (`/api/start-detection`).
3.  **Receive**: Menerima koordinat kotak api (bounding box).
4.  **Alert Logic**:
    *   Jika api terdeteksi -> Mainkan Audio Alarm.
    *   Trigger `Notification API` (Browser Popup).

### B. Backend (Python Flask + YOLO)
1.  **Receive**: Menerima request start session dengan `camera_name`.
2.  **Process (`detect_fire`)**:
    *   Gambar dimasukkan ke model AI (`best.pt`).
    *   Jika confidence > threshold -> **KEBAKARAN**.
3.  **Notification Logic**:
    *   Cek apakah notifikasi sudah dikirim? (Agar tidak spam).
    *   Jika belum -> Kirim ke **Telegram Bot** & **Fonnte (SMS)** menggunakan `camera_name`.
4.  **Security**:
    *   Koneksi Database menggunakan user khusus `firevision_user` (Bukan root).

---

## 5. Testing (Pengujian)

Dalam pengembangan software, ada dua metode pengujian utama yang diminta dosen Anda:

### A. White Box Testing (Pengujian Kotak Putih)
**Definisi**: Pengujian yang dilakukan dengan **melihat struktur kode internal**. Kita tahu bagaimana kode bekerja, logikanya, percabangannya (`if-else`), dan loop-nya.

**Contoh Kasus di FireVision:**
1.  **Unit Testing Fungsi `detect_fire`**:
    *   *Skenario*: Kita set `sensitivity = 100` (sangat rendah).
    *   *Analisis Kode*: Verifikasi apakah variabel `conf_threshold` terhitung benar dan logika `if confidence > conf_threshold` tereksekusi.
2.  **Security Testing Database**:
    *   *Skenario*: Coba connect database pakai user `root`.
    *   *Hasil*: Gagal (karena di `.env` sudah diubah ke `firevision_user`). Ini membuktikan hardening security berhasil.

### B. Black Box Testing (Pengujian Kotak Hitam)
**Definisi**: Pengujian yang dilakukan **tanpa melihat kode**. Kita hanya peduli **Input** dan **Output**. Kita bertindak seolah-olah kita adalah pengguna biasa.

**Contoh Kasus di FireVision:**
1.  **Uji Notifikasi Browser**:
    *   *Input*: Minimize browser, lalu nyalakan api di depan kamera.
    *   *Output Harapan*: Popup notifikasi Windows muncul "Api terdeteksi di Kamera 1!".
2.  **Uji Multi-Kamera**:
    *   *Input*: Nyalakan Kamera 1 dan Kamera 2. Api hanya ada di Kamera 2.
    *   *Output Harapan*: Notifikasi Telegram harus spesifik menyebut "Kamera 2", bukan Kamera 1.
3.  **Uji Login**:
    *   *Input*: Username "asep1", Password salah.
    *   *Output Harapan*: Pesan error muncul, tidak bisa masuk dashboard.

---

**Ringkasan untuk Dosen:**
*   **White Box**: "Saya memeriksa logika backend, memastikan thread kamera aman dan database menggunakan kredensial terbatas."
*   **Black Box**: "Saya tes fitur notifikasi dengan meminimize browser, dan sistem tetap memberi peringatan. Fitur berjalan sesuai kebutuhan user."
