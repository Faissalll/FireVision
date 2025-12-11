<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-3xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Kebijakan Privasi</h1>
        
        <div class="prose prose-invert prose-lg max-w-none text-gray-300">
            <p>Terakhir diperbarui: 12 Desember 2025</p>
            
            <h3>1. Pengumpulan Informasi</h3>
            <p>
                Kami mengumpulkan informasi yang Anda berikan secara langsung kepada kami, seperti saat Anda membuat akun, memperbarui profil, atau berkomunikasi dengan layanan pelanggan kami.
                Jenis informasi yang kami kumpulkan meliputi nama, alamat email, dan kredensial login.
            </p>

            <h3>2. Data Video dan Deteksi</h3>
            <p>
                FireVision memproses aktivitas video secara lokal (on-premise) atau di cloud tergantung konfigurasi Anda. Kami <strong>tidak</strong> menyimpan rekaman video Anda di server kami kecuali jika Anda secara eksplisit mengaktifkan penyimpanan cloud untuk insiden (alarm).
                Metadata deteksi (waktu, jenis objek, tingkat kepercayaan) disimpan untuk keperluan riwayat dan analitik.
            </p>

            <h3>3. Keamanan Data</h3>
            <p>
                Kami menerapkan langkah-langkah keamanan teknis dan organisasional yang dirancang untuk melindungi data Anda dari akses, pengungkapan, penggunaan, dan modifikasi yang tidak sah.
            </p>
        </div>
    </div>
</template>
