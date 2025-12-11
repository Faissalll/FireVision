<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Karir di FireVision</h1>
        
        <p class="text-gray-300 mb-10 text-lg">
            Bergabunglah dengan tim kami untuk membangun masa depan keselamatan cerdas. Kami mencari para pemimpi dan pembuat perubahan.
        </p>

        <div class="space-y-4">
            <!-- Job Card 1 -->
            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800 flex justify-between items-center group hover:border-[#6C4DFF] transition-all">
                <div>
                    <h3 class="text-xl font-bold text-white group-hover:text-[#6C4DFF] transition-colors">Senior AI Engineer</h3>
                    <p class="text-gray-400 text-sm mt-1">Remote / Balikpapan • Full-time</p>
                </div>
                <button class="px-4 py-2 bg-[#2D2D44] rounded-lg text-sm text-white group-hover:bg-[#6C4DFF] transition-colors">
                    Lamar Sekarang
                </button>
            </div>

            <!-- Job Card 2 -->
            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800 flex justify-between items-center group hover:border-[#6C4DFF] transition-all">
                <div>
                    <h3 class="text-xl font-bold text-white group-hover:text-[#6C4DFF] transition-colors">Frontend Developer (Vue.js)</h3>
                    <p class="text-gray-400 text-sm mt-1">Balikpapan • Hybrid</p>
                </div>
                <button class="px-4 py-2 bg-[#2D2D44] rounded-lg text-sm text-white group-hover:bg-[#6C4DFF] transition-colors">
                    Lamar Sekarang
                </button>
            </div>

            <!-- Job Card 3 -->
            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800 flex justify-between items-center group hover:border-[#6C4DFF] transition-all">
                <div>
                    <h3 class="text-xl font-bold text-white group-hover:text-[#6C4DFF] transition-colors">Growth Marketing Manager</h3>
                    <p class="text-gray-400 text-sm mt-1">Remote • Contract</p>
                </div>
                <button class="px-4 py-2 bg-[#2D2D44] rounded-lg text-sm text-white group-hover:bg-[#6C4DFF] transition-colors">
                    Lamar Sekarang
                </button>
            </div>
        </div>
        
        <div class="mt-12 text-center text-gray-500">
            <p>Tidak menemukan posisi yang cocok? Kirim CV Anda ke <a href="mailto:careers@firevision.id" class="text-[#6C4DFF]">careers@firevision.id</a></p>
        </div>
    </div>
</template>
