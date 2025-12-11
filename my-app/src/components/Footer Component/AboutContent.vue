<template>
    <div class="flex-grow pt-24 pb-12 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto w-full">
        <button @click="$router.back()" class="flex items-center gap-2 text-gray-400 hover:text-white mb-8 transition-colors group">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="group-hover:-translate-x-1 transition-transform"><path d="m15 18-6-6 6-6"/></svg>
            Kembali
        </button>
        <h1 class="text-4xl font-bold mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Tentang FireVision</h1>
        
        <div class="space-y-6 text-gray-300 leading-relaxed">
            <p>
                FireVision adalah pelopor dalam teknologi deteksi kebakaran berbasis kecerdasan buatan (AI). 
                Misi kami adalah menyelamatkan nyawa dan aset berharga dengan memberikan peringatan dini yang tercepat dan terakurat di dunia.
            </p>
            <h2 class="text-2xl font-semibold text-white mt-8 mb-4">Visi Kami</h2>
            <p>
                Menciptakan dunia yang bebas dari bencana kebakaran yang tidak terdeteksi, di mana setiap gedung, hutan, dan fasilitas industri dilindungi oleh mata cerdas yang tidak pernah tidur.
            </p>
            <h2 class="text-2xl font-semibold text-white mt-8 mb-4">Teknologi</h2>
            <p>
                Kami menggabungkan Computer Vision mutakhir dengan sensor IoT untuk mendeteksi api dan asap dalam hitungan detik—jauh lebih cepat daripada detektor asap tradisional.
            </p>
        </div>
    </div>
</template>
