<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-5xl mx-auto w-full text-center">
        <div class="flex justify-start max-w-4xl mx-auto w-full">
            <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
                Kembali
            </button>
        </div>
        <h1 class="text-5xl font-bold mb-6 bg-gradient-to-r from-white to-[#6C4DFF] bg-clip-text text-transparent">Komunitas FireVision</h1>
        <p class="text-xl text-gray-400 max-w-2xl mx-auto mb-16">
            Bergabunglah dengan ribuan developer, engineer keselamatan, dan pengguna FireVision lainnya untuk berdiskusi dan berbagi ide.
        </p>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto text-left">
            <!-- Discord -->
            <div class="bg-[#5865F2] hover:bg-[#4752C4] transition-colors p-8 rounded-2xl relative overflow-hidden group cursor-pointer">
                <div class="relative z-10">
                    <h2 class="text-3xl font-bold text-white mb-2">Discord</h2>
                    <p class="text-white/80 mb-8">Chat langsung dengan developer, dapatkan bantuan instan, dan ikut serta dalam event mingguan.</p>
                    <button class="bg-white text-[#5865F2] font-bold py-2 px-6 rounded-lg group-hover:bg-gray-100 transition-colors">
                        Join Server
                    </button>
                </div>
            </div>

            <!-- GitHub -->
            <div class="bg-[#24292e] hover:bg-[#1b1f23] transition-colors p-8 rounded-2xl relative overflow-hidden group cursor-pointer">
                <div class="relative z-10">
                    <h2 class="text-3xl font-bold text-white mb-2">GitHub</h2>
                    <p class="text-white/80 mb-8">Laporkan bug, request fitur, atau berkontribusi langsung ke kode sumber open source kami.</p>
                    <a href="https://github.com/Faissalll/FireVision" target="_blank" rel="noopener noreferrer" class="inline-block bg-white text-black font-bold py-2 px-6 rounded-lg group-hover:bg-gray-100 transition-colors">
                        Lihat Repo
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>
