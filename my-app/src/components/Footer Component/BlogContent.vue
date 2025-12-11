<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-6xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Blog FireVision</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <!-- Dummy Blog Post 1 -->
            <div class="bg-[#1A1A2E] rounded-xl overflow-hidden border border-gray-800 hover:border-[#6C4DFF] transition-colors group cursor-pointer">
                <div class="h-48 bg-gray-700 flex items-center justify-center">
                    <span class="text-gray-500">Gambar Artikel</span>
                </div>
                <div class="p-6">
                    <span class="text-[#6C4DFF] text-xs font-bold uppercase tracking-wider">Teknologi</span>
                    <h2 class="text-xl font-bold mt-2 mb-3 group-hover:text-[#6C4DFF] transition-colors">Masa Depan Deteksi Kebakaran dengan AI</h2>
                    <p class="text-gray-400 text-sm line-clamp-3">
                        Bagaimana algoritma deep learning mengubah cara kita memantau keselamatan gedung secara real-time.
                    </p>
                    <div class="mt-4 text-xs text-gray-500">12 Des 2025 • 5 menit baca</div>
                </div>
            </div>

                <!-- Dummy Blog Post 2 -->
                <div class="bg-[#1A1A2E] rounded-xl overflow-hidden border border-gray-800 hover:border-[#6C4DFF] transition-colors group cursor-pointer">
                <div class="h-48 bg-gray-700 flex items-center justify-center">
                    <span class="text-gray-500">Gambar Artikel</span>
                </div>
                <div class="p-6">
                    <span class="text-[#6C4DFF] text-xs font-bold uppercase tracking-wider">Studi Kasus</span>
                    <h2 class="text-xl font-bold mt-2 mb-3 group-hover:text-[#6C4DFF] transition-colors">Implementasi di Pabrik Otomotif Terbesar</h2>
                    <p class="text-gray-400 text-sm line-clamp-3">
                        Pelajari bagaimana FireVision mengurangi risiko kebakaran hingga 99% di fasilitas produksi seluas 5 hektar.
                    </p>
                    <div class="mt-4 text-xs text-gray-500">10 Des 2025 • 8 menit baca</div>
                </div>
            </div>

                <!-- Dummy Blog Post 3 -->
                <div class="bg-[#1A1A2E] rounded-xl overflow-hidden border border-gray-800 hover:border-[#6C4DFF] transition-colors group cursor-pointer">
                <div class="h-48 bg-gray-700 flex items-center justify-center">
                    <span class="text-gray-500">Gambar Artikel</span>
                </div>
                <div class="p-6">
                    <span class="text-[#6C4DFF] text-xs font-bold uppercase tracking-wider">Tips</span>
                    <h2 class="text-xl font-bold mt-2 mb-3 group-hover:text-[#6C4DFF] transition-colors">5 Tanda Dini Kebakaran Listrik</h2>
                    <p class="text-gray-400 text-sm line-clamp-3">
                        Kenali tanda-tanda halus sebelum api membesar. Panduan lengkap untuk manajer fasilitas.
                    </p>
                    <div class="mt-4 text-xs text-gray-500">05 Des 2025 • 4 menit baca</div>
                </div>
            </div>
        </div>
    </div>
</template>
