<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-3xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Keamanan</h1>
        
        <div class="space-y-8">
            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800">
                <h2 class="text-2xl font-bold text-white mb-4">Enkripsi Data</h2>
                <p class="text-gray-400">
                    Semua data yang dikirimkan antara browser Anda dan server kami dienkripsi menggunakan standar industri Transport Layer Security (TLS).
                    Data sensitif seperti password disimpan dalam bentuk hash yang tidak dapat dibalik menggunakan algoritma bcrypt/Argon2.
                </p>
            </div>

            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800">
                <h2 class="text-2xl font-bold text-white mb-4">Infrastruktur</h2>
                <p class="text-gray-400">
                    Server kami di-hosting di pusat data yang memiliki sertifikasi ISO 27001 dan SOC 2, dengan perlindungan fisik dan jaringan berlapis.
                </p>
            </div>

            <div class="bg-[#1A1A2E] p-8 rounded-xl border border-gray-800">
                <h2 class="text-2xl font-bold text-white mb-4">Pelaporan Kerentanan</h2>
                <p class="text-gray-400">
                    Jika Anda yakin telah menemukan kerentanan keamanan di FireVision, harap segera hubungi kami di <a href="mailto:security@firevision.id" class="text-[#6C4DFF]">security@firevision.id</a>.
                </p>
            </div>
        </div>
    </div>
</template>
