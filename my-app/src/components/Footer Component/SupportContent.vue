<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Pusat Bantuan</h1>
        
        <div class="space-y-6">
            <!-- FAQ Item 1 -->
            <div class="bg-[#1A1A2E] rounded-xl border border-gray-800 p-6">
                <h3 class="text-xl font-bold text-white mb-2">Berapa banyak kamera yang bisa saya hubungkan?</h3>
                <p class="text-gray-400">Untuk paket Free, Anda dibatasi maksimal 2 kamera. Paket Premium mendukung kamera tanpa batas (unlimited) tergantung kapasitas hardware server Anda.</p>
            </div>

            <!-- FAQ Item 2 -->
            <div class="bg-[#1A1A2E] rounded-xl border border-gray-800 p-6">
                <h3 class="text-xl font-bold text-white mb-2">Apakah FireVision bisa berjalan offline?</h3>
                <p class="text-gray-400">Ya! Inti deteksi AI berjalan secara lokal di server Anda. Koneksi internet hanya diperlukan untuk mengirim notifikasi Telegram/Email atau akses jarak jauh.</p>
            </div>

            <!-- FAQ Item 3 -->
            <div class="bg-[#1A1A2E] rounded-xl border border-gray-800 p-6">
                <h3 class="text-xl font-bold text-white mb-2">Bagaimana cara mereset password saya?</h3>
                <p class="text-gray-400">Saat ini fitur reset password mandiri sedang dikembangkan. Silakan hubungi admin IT Anda untuk mereset kredensial database secara manual.</p>
            </div>

            <!-- FAQ Item 4 -->
            <div class="bg-[#1A1A2E] rounded-xl border border-gray-800 p-6">
                <h3 class="text-xl font-bold text-white mb-2">Kamera saya tidak terdeteksi, apa yang harus dilakukan?</h3>
                <p class="text-gray-400">Pastikan URL RTSP atau IP Camera Anda benar dan dapat diakses dari jaringan server. Coba buka URL tersebut di VLC Player untuk memverifikasi stream.</p>
            </div>
        </div>

        <div class="mt-12 bg-[#1A1A2E] border border-[#6C4DFF]/30 p-8 rounded-xl text-center">
            <h3 class="text-2xl font-bold text-white mb-2">Masih butuh bantuan?</h3>
            <p class="text-gray-400 mb-6">Tim support kami siap membantu Anda 24/7.</p>
            <button class="bg-[#6C4DFF] hover:bg-[#5a3fe0] text-white font-bold py-3 px-8 rounded-full transition-colors">
                Hubungi Support
            </button>
        </div>
    </div>
</template>
