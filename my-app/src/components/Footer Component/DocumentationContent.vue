<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Dokumentasi FireVision</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mt-10">
            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800 hover:border-[#6C4DFF] transition-colors cursor-pointer">
                <h2 class="text-2xl font-bold mb-4 text-white">Panduan Memulai</h2>
                <p class="text-gray-400 mb-4">Pelajari cara menginstal, mengonfigurasi, dan menyambungkan kamera pertama Anda ke sistem FireVision.</p>
                <span class="text-[#6C4DFF] font-semibold flex items-center gap-2">Baca Panduan <span class="text-xl">→</span></span>
            </div>

            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800 hover:border-[#6C4DFF] transition-colors cursor-pointer">
                <h2 class="text-2xl font-bold mb-4 text-white">Integrasi Kamera</h2>
                <p class="text-gray-400 mb-4">Panduan teknis untuk menghubungkan CCTV RTSP, Webcam, dan IP Camera pihak ketiga.</p>
                <span class="text-[#6C4DFF] font-semibold flex items-center gap-2">Lihat Daftar Perangkat <span class="text-xl">→</span></span>
            </div>

            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800 hover:border-[#6C4DFF] transition-colors cursor-pointer">
                <h2 class="text-2xl font-bold mb-4 text-white">Manajemen Notifikasi</h2>
                <p class="text-gray-400 mb-4">Cara mengatur peringatan Telegram, Email, dan SMS agar tim Anda selalu waspada.</p>
                <span class="text-[#6C4DFF] font-semibold flex items-center gap-2">Setup Notifikasi <span class="text-xl">→</span></span>
            </div>

            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800 hover:border-[#6C4DFF] transition-colors cursor-pointer">
                <h2 class="text-2xl font-bold mb-4 text-white">Troubleshooting</h2>
                <p class="text-gray-400 mb-4">Solusi untuk masalah umum seperti kamera offline, latensi tinggi, atau deteksi palsu.</p>
                <span class="text-[#6C4DFF] font-semibold flex items-center gap-2">Cari Solusi <span class="text-xl">→</span></span>
            </div>
        </div>
    </div>
</template>
