<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-3xl font-bold mb-8 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Kepatuhan & Sertifikasi</h1>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800 flex items-start gap-4">
                <div class="bg-green-500/20 p-3 rounded-lg text-green-400 font-bold">GDPR</div>
                <div>
                    <h3 class="text-white font-bold mb-1">General Data Protection Regulation</h3>
                    <p class="text-sm text-gray-400">Kami patuh sepenuhnya terhadap regulasi perlindungan data Uni Eropa.</p>
                </div>
            </div>

            <div class="bg-[#1A1A2E] p-6 rounded-xl border border-gray-800 flex items-start gap-4">
                <div class="bg-blue-500/20 p-3 rounded-lg text-blue-400 font-bold">ISO</div>
                <div>
                    <h3 class="text-white font-bold mb-1">ISO 27001</h3>
                    <p class="text-sm text-gray-400">Sistem Manajemen Keamanan Informasi kami telah tersertifikasi.</p>
                </div>
            </div>
        </div>
    </div>
</template>
